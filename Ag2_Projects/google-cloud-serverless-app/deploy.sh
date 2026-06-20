#!/usr/bin/env bash
# =============================================================================
# deploy.sh
# One-shot deployment script for the serverless document processing pipeline.
#
# Prerequisites:
#   - gcloud CLI installed and authenticated  (gcloud auth login)
#   - Docker installed and running            (for Cloud Build)
#   - Billing enabled on the project
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration — edit these if needed
# ---------------------------------------------------------------------------
PROJECT_ID="divya-doc-pipeline"
REGION="us-central1"
BQ_LOCATION="US"

BUCKET_NAME="${PROJECT_ID}-doc-uploads"
PUBSUB_TOPIC="document-upload-events"
PUBSUB_SUB="doc-processor-push-sub"
SERVICE_NAME="doc-processor"
DATASET_ID="docpipeline_dataset"
TABLE_ID="document_metadata"

IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { echo -e "\n\033[1;34m▶ $*\033[0m"; }
ok()    { echo -e "\033[1;32m✔ $*\033[0m"; }
warn()  { echo -e "\033[1;33m⚠ $*\033[0m"; }

# ---------------------------------------------------------------------------
# Step 0 – Set active project
# ---------------------------------------------------------------------------
info "Setting active project to ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}"
ok "Project set"

# ---------------------------------------------------------------------------
# Step 1 – Enable required APIs
# ---------------------------------------------------------------------------
info "Enabling required GCP APIs (this may take a minute on first run)..."
gcloud services enable \
  storage.googleapis.com \
  pubsub.googleapis.com \
  run.googleapis.com \
  bigquery.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  --project="${PROJECT_ID}"
ok "APIs enabled"

# ---------------------------------------------------------------------------
# Step 2 – Cloud Storage bucket
# ---------------------------------------------------------------------------
info "Creating GCS bucket: gs://${BUCKET_NAME}"
if gsutil ls -b "gs://${BUCKET_NAME}" &>/dev/null; then
  warn "Bucket gs://${BUCKET_NAME} already exists — skipping creation"
else
  gsutil mb -p "${PROJECT_ID}" -l "${REGION}" "gs://${BUCKET_NAME}"
  ok "Bucket created"
fi

# ---------------------------------------------------------------------------
# Step 3 – Pub/Sub topic
# ---------------------------------------------------------------------------
info "Creating Pub/Sub topic: ${PUBSUB_TOPIC}"
if gcloud pubsub topics describe "${PUBSUB_TOPIC}" --project="${PROJECT_ID}" &>/dev/null; then
  warn "Topic ${PUBSUB_TOPIC} already exists — skipping"
else
  gcloud pubsub topics create "${PUBSUB_TOPIC}" --project="${PROJECT_ID}"
  ok "Topic created"
fi

# Grant GCS service account permission to publish to the topic
info "Granting GCS SA publish rights on topic..."
GCS_SA="$(gsutil kms serviceaccount -p "${PROJECT_ID}")"
gcloud pubsub topics add-iam-policy-binding "${PUBSUB_TOPIC}" \
  --member="serviceAccount:${GCS_SA}" \
  --role="roles/pubsub.publisher" \
  --project="${PROJECT_ID}"
ok "IAM binding added"

# Enable GCS → Pub/Sub notification on OBJECT_FINALIZE
info "Configuring GCS notification → ${PUBSUB_TOPIC}"
gsutil notification create \
  -t "projects/${PROJECT_ID}/topics/${PUBSUB_TOPIC}" \
  -f json \
  -e OBJECT_FINALIZE \
  "gs://${BUCKET_NAME}"
ok "GCS notification configured"

# ---------------------------------------------------------------------------
# Step 4 – BigQuery dataset and table
# ---------------------------------------------------------------------------
info "Creating BigQuery dataset: ${DATASET_ID}"
if bq ls --project_id="${PROJECT_ID}" "${DATASET_ID}" &>/dev/null; then
  warn "Dataset ${DATASET_ID} already exists — skipping"
else
  bq mk \
    --project_id="${PROJECT_ID}" \
    --location="${BQ_LOCATION}" \
    --dataset \
    "${DATASET_ID}"
  ok "Dataset created"
fi

info "Creating BigQuery table: ${TABLE_ID}"
SCHEMA='[
  {"name":"filename",               "type":"STRING",    "mode":"REQUIRED"},
  {"name":"date",                   "type":"TIMESTAMP", "mode":"REQUIRED"},
  {"name":"tags",                   "type":"STRING",    "mode":"REPEATED"},
  {"name":"word_count",             "type":"INTEGER",   "mode":"REQUIRED"},
  {"name":"file_size_bytes",        "type":"INTEGER",   "mode":"NULLABLE"},
  {"name":"content_type",           "type":"STRING",    "mode":"NULLABLE"},
  {"name":"source_bucket",          "type":"STRING",    "mode":"NULLABLE"},
  {"name":"processing_duration_ms", "type":"INTEGER",   "mode":"NULLABLE"},
  {"name":"confidence_score",       "type":"FLOAT",     "mode":"NULLABLE"}
]'

echo "${SCHEMA}" > /tmp/bq_schema.json

if bq show --project_id="${PROJECT_ID}" "${DATASET_ID}.${TABLE_ID}" &>/dev/null; then
  warn "Table ${TABLE_ID} already exists — skipping"
else
  bq mk \
    --project_id="${PROJECT_ID}" \
    --table \
    "${DATASET_ID}.${TABLE_ID}" \
    /tmp/bq_schema.json
  ok "Table created"
fi

# ---------------------------------------------------------------------------
# Step 5 – Build and push Docker image via Cloud Build
# ---------------------------------------------------------------------------
info "Building and pushing Docker image via Cloud Build..."
gcloud builds submit "processor/" \
  --tag="${IMAGE}" \
  --project="${PROJECT_ID}"
ok "Image built: ${IMAGE}"

# ---------------------------------------------------------------------------
# Step 6 – Deploy Cloud Run service
# ---------------------------------------------------------------------------
info "Deploying Cloud Run service: ${SERVICE_NAME}"
gcloud run deploy "${SERVICE_NAME}" \
  --image="${IMAGE}" \
  --platform=managed \
  --region="${REGION}" \
  --allow-unauthenticated \
  --set-env-vars="GCP_PROJECT_ID=${PROJECT_ID},BQ_DATASET=${DATASET_ID},BQ_TABLE=${TABLE_ID}" \
  --min-instances=0 \
  --max-instances=10 \
  --memory=512Mi \
  --cpu=1 \
  --timeout=60s \
  --project="${PROJECT_ID}"
ok "Cloud Run service deployed"

# Retrieve the service URL
SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" \
  --platform=managed --region="${REGION}" \
  --format='value(status.url)' \
  --project="${PROJECT_ID}")"
echo ""
echo "  Cloud Run URL: ${SERVICE_URL}"

# ---------------------------------------------------------------------------
# Step 7 – Pub/Sub push subscription (or update if exists)
# ---------------------------------------------------------------------------
PUSH_ENDPOINT="${SERVICE_URL}/process"

info "Creating Pub/Sub push subscription: ${PUBSUB_SUB}"
if gcloud pubsub subscriptions describe "${PUBSUB_SUB}" --project="${PROJECT_ID}" &>/dev/null; then
  warn "Subscription ${PUBSUB_SUB} exists — updating push endpoint..."
  gcloud pubsub subscriptions modify-push-config "${PUBSUB_SUB}" \
    --push-endpoint="${PUSH_ENDPOINT}" \
    --project="${PROJECT_ID}"
else
  gcloud pubsub subscriptions create "${PUBSUB_SUB}" \
    --topic="${PUBSUB_TOPIC}" \
    --push-endpoint="${PUSH_ENDPOINT}" \
    --ack-deadline=60 \
    --project="${PROJECT_ID}"
fi
ok "Push subscription configured → ${PUSH_ENDPOINT}"

# ---------------------------------------------------------------------------
# Done – print smoke-test instructions
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  ✅  Pipeline deployed successfully!"
echo "============================================================"
echo ""
echo "  Project  : ${PROJECT_ID}"
echo "  Bucket   : gs://${BUCKET_NAME}"
echo "  Topic    : ${PUBSUB_TOPIC}"
echo "  Service  : ${SERVICE_URL}"
echo "  BQ Table : ${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}"
echo ""
echo "------------------------------------------------------------"
echo "  SMOKE TEST"
echo "------------------------------------------------------------"
echo ""
echo "  1) Upload a test file:"
echo "     echo 'Hello world document' > /tmp/test_doc.txt"
echo "     gsutil cp /tmp/test_doc.txt gs://${BUCKET_NAME}/"
echo ""
echo "  2) Watch Cloud Run logs (within ~10s):"
echo "     gcloud run services logs read ${SERVICE_NAME} \\"
echo "       --region=${REGION} --limit=20"
echo ""
echo "  3) Query BigQuery:"
echo "     bq query --use_legacy_sql=false \\"
echo "       'SELECT filename, date, tags, word_count, confidence_score"
echo "        FROM \`${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\`"
echo "        ORDER BY date DESC LIMIT 10'"
echo ""
echo "  4) Manual Pub/Sub push test (direct HTTP):"
ENCODED=$(echo -n '{"bucket":"'"${BUCKET_NAME}"'","name":"manual_test.pdf","size":"204800","contentType":"application/pdf"}' | base64)
echo "     curl -s -X POST ${PUSH_ENDPOINT} \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"message\":{\"data\":\"${ENCODED}\",\"messageId\":\"test-1\"},\"subscription\":\"manual\"}'"
echo ""
