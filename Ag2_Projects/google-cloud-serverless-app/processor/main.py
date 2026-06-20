"""
main.py
-------
FastAPI Cloud Run service that acts as a Pub/Sub push subscription handler.

Routes
------
GET  /health   → liveness probe (Cloud Run health check)
POST /process  → Pub/Sub push endpoint; decodes GCS object notification,
                 runs simulated OCR, and streams metadata to BigQuery.
"""

import base64
import json
import logging
import os
import time
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request, Response
from google.cloud import bigquery

from ocr_simulator import simulate_ocr

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration (from environment variables set by Cloud Run / deploy.sh)
# ---------------------------------------------------------------------------
PROJECT_ID  = os.environ.get("GCP_PROJECT_ID", "daykgadkproj")
DATASET_ID  = os.environ.get("BQ_DATASET",     "docpipeline_dataset")
TABLE_ID    = os.environ.get("BQ_TABLE",        "document_metadata")

FULL_TABLE_REF = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# ---------------------------------------------------------------------------
# BigQuery client (module-level — reused across requests)
# ---------------------------------------------------------------------------
bq_client = bigquery.Client(project=PROJECT_ID)

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Document Processing Pipeline",
    description="Pub/Sub push handler: simulated OCR → BigQuery",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health", tags=["ops"])
def health():
    """Liveness probe for Cloud Run."""
    return {"status": "ok", "table": FULL_TABLE_REF}


@app.post("/process", tags=["pipeline"], status_code=200)
async def process_document(request: Request):
    """
    Pub/Sub push subscription handler.

    Pub/Sub sends a JSON envelope:
    {
      "message": {
        "data": "<base64-encoded GCS notification JSON>",
        "messageId": "...",
        ...
      },
      "subscription": "..."
    }

    The GCS notification JSON contains:
        bucket, name, size, contentType, timeCreated, ...
    """
    start_ms = time.monotonic() * 1000

    try:
        body = await request.json()
    except Exception as exc:
        log.error("Failed to parse request body: %s", exc)
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # --- Decode Pub/Sub message ---
    try:
        raw_data = body["message"]["data"]
        gcs_notification = json.loads(base64.b64decode(raw_data).decode("utf-8"))
    except (KeyError, ValueError, Exception) as exc:
        log.error("Could not decode Pub/Sub message: %s", exc)
        # Return 200 to prevent Pub/Sub infinite retry on a malformed message
        return Response(content="bad message format – ack'd to avoid retry", status_code=200)

    # --- Extract GCS object fields ---
    filename         = gcs_notification.get("name", "unknown")
    source_bucket    = gcs_notification.get("bucket", "unknown")
    file_size_bytes  = int(gcs_notification.get("size", 0))
    content_type     = gcs_notification.get("contentType", "application/octet-stream")

    log.info(
        "Processing: gs://%s/%s  size=%d  type=%s",
        source_bucket, filename, file_size_bytes, content_type,
    )

    # --- Simulated OCR ---
    try:
        ocr_result = simulate_ocr(
            filename=filename,
            file_size_bytes=file_size_bytes,
            content_type=content_type,
        )
    except Exception as exc:
        log.error("OCR simulation failed for %s: %s", filename, exc)
        raise HTTPException(status_code=500, detail="OCR simulation error")

    processing_duration_ms = int(time.monotonic() * 1000 - start_ms)

    # --- Build BigQuery row ---
    row = {
        "filename":               filename,
        "date":                   datetime.now(timezone.utc).isoformat(),
        "tags":                   ocr_result["tags"],
        "word_count":             ocr_result["word_count"],
        "file_size_bytes":        file_size_bytes,
        "content_type":           content_type,
        "source_bucket":          source_bucket,
        "processing_duration_ms": processing_duration_ms,
        "confidence_score":       ocr_result["confidence_score"],
    }

    # --- Stream row to BigQuery ---
    try:
        errors = bq_client.insert_rows_json(FULL_TABLE_REF, [row])
        if errors:
            log.error("BigQuery insert errors for %s: %s", filename, errors)
            raise HTTPException(status_code=500, detail=f"BigQuery insert failed: {errors}")
    except HTTPException:
        raise
    except Exception as exc:
        log.error("BigQuery client error for %s: %s", filename, exc)
        raise HTTPException(status_code=500, detail="BigQuery client error")

    log.info(
        "Stored metadata: filename=%s  words=%d  confidence=%.4f  duration_ms=%d",
        filename,
        ocr_result["word_count"],
        ocr_result["confidence_score"],
        processing_duration_ms,
    )

    return {
        "status":    "ok",
        "filename":  filename,
        "word_count": ocr_result["word_count"],
        "confidence": ocr_result["confidence_score"],
        "bq_table":  FULL_TABLE_REF,
    }
