# Serverless Event-Driven Document Processing Pipeline on Google Cloud

A fully event-driven pipeline where file uploads to Cloud Storage automatically trigger simulated OCR processing via Pub/Sub and Cloud Run, with structured metadata streamed into BigQuery.

---

## Architecture Overview

```
User Upload
    │
    ▼
Cloud Storage Bucket (raw-uploads)
    │  [Pub/Sub Notification on object.finalize]
    ▼
Pub/Sub Topic (document-upload-events)
    │  [Push Subscription → HTTP POST]
    ▼
Cloud Run Service (doc-processor)
    │  [Simulated OCR + metadata extraction]
    ▼
BigQuery Table (document_metadata)
```

**Pub/Sub delivery mode:** Push subscription — Pub/Sub pushes an HTTP POST to the Cloud Run service's `/process` endpoint. This is recommended for Cloud Run because it's reactive (no idle polling), scales to zero between events, and integrates natively with IAM for auth. For this demo, the endpoint will allow unauthenticated requests.

---

## Key Design Decisions (from interview)

| Decision | Choice | Rationale |
|---|---|---|
| File types | All types | Simulated OCR applies uniformly |
| Pub/Sub delivery | Push subscription | Best fit for serverless reactive Cloud Run |
| OCR simulation | Metadata-only | Generates realistic fields, no content needed |
| Authentication | Unauthenticated | Dev/demo simplicity |
| IaC | Shell/gcloud scripts | Fast, readable, no Terraform overhead |
| Error handling | Basic try/except + Cloud Logging | Proportionate for a demo pipeline |
| Local testing | Deploy to GCP directly | No local emulator layer needed |

---

## BigQuery Schema

Table: `docpipeline_dataset.document_metadata`

| Field | Type | Description |
|---|---|---|
| `filename` | STRING | Original uploaded filename |
| `date` | TIMESTAMP | UTC processing timestamp |
| `tags` | ARRAY\<STRING\> | Auto-generated tags from extension/MIME type |
| `word_count` | INTEGER | Simulated word count |
| `file_size_bytes` | INTEGER | File size from GCS metadata |
| `content_type` | STRING | MIME type from GCS object |
| `source_bucket` | STRING | Originating GCS bucket name |
| `processing_duration_ms` | INTEGER | Time taken to process in ms |
| `confidence_score` | FLOAT | Simulated OCR confidence (0.0–1.0) |

---

## Proposed Changes

### Project Root

#### [NEW] `README.md`
High-level overview, architecture diagram (ASCII), setup instructions, and example BigQuery query.

#### [NEW] `deploy.sh`
One-shot `gcloud` CLI deployment script. Steps:
1. Enable required GCP APIs (`storage`, `pubsub`, `run`, `bigquery`)
2. Create GCS bucket with Pub/Sub notification on `OBJECT_FINALIZE`
3. Create Pub/Sub topic and push subscription (pointing to Cloud Run URL)
4. Create BigQuery dataset and table with full schema
5. Build and deploy the Cloud Run service

#### [NEW] `teardown.sh`
Clean-up script to delete all created GCP resources.

---

### Cloud Run Service — `processor/`

#### [NEW] `processor/main.py`
FastAPI application with two routes:
- `GET /health` — liveness probe
- `POST /process` — Pub/Sub push handler

Processing flow for `/process`:
1. Decode the base64-encoded Pub/Sub message data (contains GCS object notification JSON)
2. Extract `bucket`, `name`, `size`, `contentType` from the notification
3. Call `simulate_ocr()` to generate `word_count` and `confidence_score`
4. Generate `tags` from file extension and MIME type
5. Stream one row into BigQuery via the BigQuery client library
6. Return `HTTP 200` (tells Pub/Sub the message was processed successfully)

Error handling: `try/except` wraps the entire handler; unhandled exceptions return `HTTP 500` and log the full traceback to Cloud Logging (automatically captured by Cloud Run).

#### [NEW] `processor/ocr_simulator.py`
Pure-Python OCR simulation module:
- `simulate_ocr(filename, file_size_bytes, content_type) → dict`
  - `word_count`: deterministic based on `file_size_bytes` (size / 6, bounded to a realistic range)
  - `confidence_score`: seeded random float 0.70–0.99, deterministic per filename
  - `tags`: list derived from extension mapping + MIME category (e.g., `["pdf", "document", "text"]`)

#### [NEW] `processor/requirements.txt`
```
fastapi
uvicorn[standard]
google-cloud-bigquery
google-cloud-storage
```

#### [NEW] `processor/Dockerfile`
Multi-stage Python 3.12-slim image. Uses `uvicorn` as the ASGI server on port `8080` (Cloud Run default).

---

## Verification Plan

### Automated (Post-Deploy)
- `deploy.sh` prints a smoke-test `curl` command to manually push a fake Pub/Sub message to the `/process` endpoint and verify an `HTTP 200` response.

### GCP Console Verification
1. Upload a test file to the GCS bucket and confirm a Pub/Sub message is triggered (Pub/Sub metrics).
2. Check Cloud Run logs for the processing log entry.
3. Run this BigQuery query to confirm the row landed:
```sql
SELECT filename, date, tags, word_count, confidence_score
FROM `YOUR_PROJECT.docpipeline_dataset.document_metadata`
ORDER BY date DESC
LIMIT 10;
```

---

## Open Questions

> [!IMPORTANT]
> **GCP Project ID**: What is your GCP Project ID? The `deploy.sh` script will use `YOUR_PROJECT_ID` as a placeholder that you'll need to fill in, or you can tell me now and I'll hardcode it.

> [!NOTE]
> **GCP Region**: Defaults to `us-central1`. Let me know if you want a different region.

> [!NOTE]
> **BigQuery Dataset Location**: Defaults to `US` (multi-region). Change if needed for data residency.
