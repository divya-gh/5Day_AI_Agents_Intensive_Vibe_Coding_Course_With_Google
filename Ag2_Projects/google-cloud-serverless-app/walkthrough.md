# Pipeline Walkthrough

All 7 files have been created. Here's what was built and how everything connects.

---

## Files Created

| File | Purpose |
|---|---|
| [README.md](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/README.md) | Architecture overview, quick-start, example queries |
| [deploy.sh](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/deploy.sh) | One-shot idempotent deployment of all GCP resources |
| [teardown.sh](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/teardown.sh) | Safe cleanup with confirmation prompt |
| [processor/main.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/processor/main.py) | FastAPI Cloud Run service (Pub/Sub push handler) |
| [processor/ocr_simulator.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/processor/ocr_simulator.py) | Deterministic OCR simulation engine |
| [processor/requirements.txt](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/processor/requirements.txt) | Pinned Python dependencies |
| [processor/Dockerfile](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Ag2_Projects/google-cloud-serverless-app/processor/Dockerfile) | Two-stage slim Python 3.12 image |

---

## End-to-End Data Flow

```
1. User uploads  →  gs://daykgadkproj-doc-uploads/<file>
2. GCS fires OBJECT_FINALIZE notification
3. Pub/Sub receives it on topic: document-upload-events
4. Push subscription POSTs to: https://<cloud-run-url>/process
5. main.py decodes the base64 GCS notification JSON
6. ocr_simulator.py generates:
     word_count         (file_size / bytes-per-word model)
     confidence_score   (seeded random 0.70–0.99)
     tags               (extension map + MIME category)
7. BigQuery row streamed into:
     daykgadkproj.docpipeline_dataset.document_metadata
8. HTTP 200 returned → Pub/Sub marks message acknowledged
```

---

## Deploy

```bash
# From a Linux/macOS shell (or WSL on Windows):
chmod +x deploy.sh teardown.sh
./deploy.sh
```

> [!IMPORTANT]
> On **Windows**, run `deploy.sh` inside **WSL** or **Git Bash** — it uses bash syntax and `gsutil`/`gcloud`/`bq` CLI tools.

---

## Smoke Test (copy-paste after deploy)

```bash
# 1. Upload a file
echo "Hello world" > /tmp/test.txt
gsutil cp /tmp/test.txt gs://daykgadkproj-doc-uploads/

# 2. Check logs (~10s later)
gcloud run services logs read doc-processor \
  --region=us-central1 --limit=20

# 3. Query the result
bq query --use_legacy_sql=false \
  'SELECT filename, tags, word_count, confidence_score
   FROM `daykgadkproj.docpipeline_dataset.document_metadata`
   ORDER BY date DESC LIMIT 5'
```

---

## Key Design Notes

- **Push vs Pull**: Push subscription chosen — Pub/Sub calls Cloud Run directly, enabling true scale-to-zero with no idle polling.
- **Idempotent deploy.sh**: Each step checks if the resource already exists before creating, so re-runs are safe.
- **Deterministic OCR**: `ocr_simulator.py` uses an MD5 seed from `filename + size`, so the same file always produces identical metadata — useful for testing idempotency.
- **ACK on bad messages**: Malformed Pub/Sub messages return `HTTP 200` (acknowledged) to prevent infinite retry loops while still logging the error.
- **Non-root container**: Dockerfile creates a dedicated `appuser` to follow least-privilege best practices.
