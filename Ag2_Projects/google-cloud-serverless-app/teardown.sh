#!/usr/bin/env bash
# =============================================================================
# teardown.sh
# Deletes all GCP resources created by deploy.sh.
#
# Usage:
#   chmod +x teardown.sh
#   ./teardown.sh
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration — must match deploy.sh
# ---------------------------------------------------------------------------
PROJECT_ID="daykgadkproj"
REGION="us-central1"

BUCKET_NAME="${PROJECT_ID}-doc-uploads"
PUBSUB_TOPIC="document-upload-events"
PUBSUB_SUB="doc-processor-push-sub"
SERVICE_NAME="doc-processor"
DATASET_ID="docpipeline_dataset"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { echo -e "\n\033[1;34m▶ $*\033[0m"; }
ok()    { echo -e "\033[1;32m✔ $*\033[0m"; }
warn()  { echo -e "\033[1;33m⚠ $*\033[0m"; }

echo ""
echo "============================================================"
warn "  This will PERMANENTLY DELETE all pipeline resources!"
echo "  Project : ${PROJECT_ID}"
echo "============================================================"
read -r -p "  Type 'yes' to continue: " CONFIRM
if [[ "${CONFIRM}" != "yes" ]]; then
  echo "Aborted."
  exit 0
fi

gcloud config set project "${PROJECT_ID}"

# ---------------------------------------------------------------------------
# Pub/Sub subscription
# ---------------------------------------------------------------------------
info "Deleting Pub/Sub subscription: ${PUBSUB_SUB}"
if gcloud pubsub subscriptions describe "${PUBSUB_SUB}" --project="${PROJECT_ID}" &>/dev/null; then
  gcloud pubsub subscriptions delete "${PUBSUB_SUB}" --project="${PROJECT_ID}" --quiet
  ok "Subscription deleted"
else
  warn "Subscription not found — skipping"
fi

# ---------------------------------------------------------------------------
# GCS notification (remove all notifications on the bucket)
# ---------------------------------------------------------------------------
info "Removing GCS notifications on gs://${BUCKET_NAME}"
if gsutil ls -b "gs://${BUCKET_NAME}" &>/dev/null; then
  gsutil notification delete "gs://${BUCKET_NAME}" 2>/dev/null || warn "No notifications found"
  ok "Notifications cleared"
else
  warn "Bucket not found — skipping notification removal"
fi

# ---------------------------------------------------------------------------
# Pub/Sub topic
# ---------------------------------------------------------------------------
info "Deleting Pub/Sub topic: ${PUBSUB_TOPIC}"
if gcloud pubsub topics describe "${PUBSUB_TOPIC}" --project="${PROJECT_ID}" &>/dev/null; then
  gcloud pubsub topics delete "${PUBSUB_TOPIC}" --project="${PROJECT_ID}" --quiet
  ok "Topic deleted"
else
  warn "Topic not found — skipping"
fi

# ---------------------------------------------------------------------------
# Cloud Run service
# ---------------------------------------------------------------------------
info "Deleting Cloud Run service: ${SERVICE_NAME}"
if gcloud run services describe "${SERVICE_NAME}" \
     --platform=managed --region="${REGION}" \
     --project="${PROJECT_ID}" &>/dev/null; then
  gcloud run services delete "${SERVICE_NAME}" \
    --platform=managed --region="${REGION}" \
    --project="${PROJECT_ID}" --quiet
  ok "Cloud Run service deleted"
else
  warn "Cloud Run service not found — skipping"
fi

# ---------------------------------------------------------------------------
# GCS bucket (force-delete all objects first)
# ---------------------------------------------------------------------------
info "Deleting GCS bucket: gs://${BUCKET_NAME}"
if gsutil ls -b "gs://${BUCKET_NAME}" &>/dev/null; then
  gsutil -m rm -r "gs://${BUCKET_NAME}" || true
  ok "Bucket deleted"
else
  warn "Bucket not found — skipping"
fi

# ---------------------------------------------------------------------------
# BigQuery dataset (delete all tables inside)
# ---------------------------------------------------------------------------
info "Deleting BigQuery dataset: ${DATASET_ID}"
if bq ls --project_id="${PROJECT_ID}" "${DATASET_ID}" &>/dev/null; then
  bq rm -r -f --project_id="${PROJECT_ID}" "${DATASET_ID}"
  ok "Dataset deleted"
else
  warn "Dataset not found — skipping"
fi

# ---------------------------------------------------------------------------
# Container Registry image (best-effort)
# ---------------------------------------------------------------------------
info "Deleting Container Registry image: ${IMAGE}"
gcloud container images delete "${IMAGE}:latest" \
  --project="${PROJECT_ID}" --quiet --force-delete-tags 2>/dev/null \
  && ok "Image deleted" \
  || warn "Image not found or already deleted"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  ✅  Teardown complete. All pipeline resources deleted."
echo "============================================================"
echo ""
