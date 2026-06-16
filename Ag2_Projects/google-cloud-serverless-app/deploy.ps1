# =============================================================================
# deploy.ps1  -  PowerShell deployment for serverless document pipeline
# =============================================================================
$ErrorActionPreference = "Stop"

$SDK = "C:\Users\divya\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
function gcloud { & "$SDK\gcloud.cmd" @args }
function gsutil { & "$SDK\gsutil.cmd" @args }
function bq     { & "$SDK\bq.cmd"     @args }

$PROJECT_ID   = "daykgadkproj"
$REGION       = "us-central1"
$BQ_LOCATION  = "US"
$BUCKET_NAME  = "$PROJECT_ID-doc-uploads"
$PUBSUB_TOPIC = "document-upload-events"
$PUBSUB_SUB   = "doc-processor-push-sub"
$SERVICE_NAME = "doc-processor"
$DATASET_ID   = "docpipeline_dataset"
$TABLE_ID     = "document_metadata"
$IMAGE        = "gcr.io/$PROJECT_ID/$SERVICE_NAME`:latest"

$ROOT          = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROCESSOR_DIR = Join-Path $ROOT "processor"
$SCHEMA_FILE   = Join-Path $ROOT "bq_schema.json"

function info($m) { Write-Host "`n>> $m" -ForegroundColor Cyan }
function ok($m)   { Write-Host "OK $m"   -ForegroundColor Green }
function warn($m) { Write-Host "!! $m"   -ForegroundColor Yellow }

# ---------------------------------------------------------------------------
# 0. Set project
# ---------------------------------------------------------------------------
info "Setting project to $PROJECT_ID"
gcloud config set project $PROJECT_ID
ok "Project set"

# ---------------------------------------------------------------------------
# 1. Enable APIs
# ---------------------------------------------------------------------------
info "Enabling GCP APIs..."
gcloud services enable storage.googleapis.com pubsub.googleapis.com run.googleapis.com bigquery.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com --project $PROJECT_ID
ok "APIs enabled"

# ---------------------------------------------------------------------------
# 2. GCS bucket
# ---------------------------------------------------------------------------
info "Creating GCS bucket: gs://$BUCKET_NAME"
$out = gsutil ls -b "gs://$BUCKET_NAME" 2>&1
if ($LASTEXITCODE -eq 0) { warn "Bucket already exists - skipping" }
else {
    gsutil mb -p $PROJECT_ID -l $REGION "gs://$BUCKET_NAME"
    ok "Bucket created"
}

# ---------------------------------------------------------------------------
# 3. Pub/Sub topic + GCS notification
# ---------------------------------------------------------------------------
info "Creating Pub/Sub topic: $PUBSUB_TOPIC"
$out = gcloud pubsub topics describe $PUBSUB_TOPIC --project $PROJECT_ID 2>&1
if ($LASTEXITCODE -eq 0) { warn "Topic already exists - skipping" }
else {
    gcloud pubsub topics create $PUBSUB_TOPIC --project $PROJECT_ID
    ok "Topic created"
}

info "Granting GCS SA publish rights..."
$GCS_SA = (gsutil kms serviceaccount -p $PROJECT_ID 2>&1 | Select-String "@").ToString().Trim()
gcloud pubsub topics add-iam-policy-binding $PUBSUB_TOPIC --member "serviceAccount:$GCS_SA" --role roles/pubsub.publisher --project $PROJECT_ID
ok "IAM binding added for $GCS_SA"

info "Configuring GCS -> Pub/Sub notification"
gsutil notification create -t "projects/$PROJECT_ID/topics/$PUBSUB_TOPIC" -f json -e OBJECT_FINALIZE "gs://$BUCKET_NAME"
ok "GCS notification configured"

# ---------------------------------------------------------------------------
# 4. BigQuery dataset + table
# ---------------------------------------------------------------------------
info "Creating BigQuery dataset: $DATASET_ID"
$out = bq ls --project_id $PROJECT_ID $DATASET_ID 2>&1
if ($LASTEXITCODE -eq 0) { warn "Dataset already exists - skipping" }
else {
    bq mk --project_id $PROJECT_ID --location $BQ_LOCATION --dataset $DATASET_ID
    ok "Dataset created"
}

info "Creating BigQuery table: $TABLE_ID"
$out = bq show --project_id $PROJECT_ID "$DATASET_ID.$TABLE_ID" 2>&1
if ($LASTEXITCODE -eq 0) { warn "Table already exists - skipping" }
else {
    bq mk --project_id $PROJECT_ID --table "$DATASET_ID.$TABLE_ID" $SCHEMA_FILE
    ok "Table created"
}

# ---------------------------------------------------------------------------
# 5. Build Docker image via Cloud Build
# ---------------------------------------------------------------------------
info "Building Docker image via Cloud Build (may take 2-3 min)..."
gcloud builds submit $PROCESSOR_DIR --tag $IMAGE --project $PROJECT_ID
ok "Image built: $IMAGE"

# ---------------------------------------------------------------------------
# 6. Deploy Cloud Run service
# ---------------------------------------------------------------------------
info "Deploying Cloud Run service: $SERVICE_NAME"
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --set-env-vars "GCP_PROJECT_ID=$PROJECT_ID,BQ_DATASET=$DATASET_ID,BQ_TABLE=$TABLE_ID" `
    --min-instances 0 `
    --max-instances 10 `
    --memory 512Mi `
    --cpu 1 `
    --timeout 60s `
    --project $PROJECT_ID
ok "Cloud Run service deployed"

$SERVICE_URL = (gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format "value(status.url)" --project $PROJECT_ID 2>&1).ToString().Trim()
Write-Host "  Cloud Run URL: $SERVICE_URL" -ForegroundColor White

# ---------------------------------------------------------------------------
# 7. Pub/Sub push subscription
# ---------------------------------------------------------------------------
$PUSH_ENDPOINT = "$SERVICE_URL/process"
info "Configuring push subscription: $PUBSUB_SUB"
$out = gcloud pubsub subscriptions describe $PUBSUB_SUB --project $PROJECT_ID 2>&1
if ($LASTEXITCODE -eq 0) {
    warn "Subscription exists - updating push endpoint..."
    gcloud pubsub subscriptions modify-push-config $PUBSUB_SUB --push-endpoint $PUSH_ENDPOINT --project $PROJECT_ID
} else {
    gcloud pubsub subscriptions create $PUBSUB_SUB --topic $PUBSUB_TOPIC --push-endpoint $PUSH_ENDPOINT --ack-deadline 60 --project $PROJECT_ID
}
ok "Push subscription -> $PUSH_ENDPOINT"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  PIPELINE DEPLOYED SUCCESSFULLY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Project  : $PROJECT_ID"
Write-Host "  Bucket   : gs://$BUCKET_NAME"
Write-Host "  Service  : $SERVICE_URL"
Write-Host "  BQ Table : $PROJECT_ID.$DATASET_ID.$TABLE_ID"
Write-Host ""
Write-Host "--- SMOKE TEST ---"
Write-Host "1) Upload a file:"
Write-Host "   echo test | Out-File `$env:TEMP\test.txt; & '$SDK\gsutil.cmd' cp `$env:TEMP\test.txt gs://$BUCKET_NAME/"
Write-Host ""
Write-Host "2) Watch logs:"
Write-Host "   & '$SDK\gcloud.cmd' run services logs read $SERVICE_NAME --region $REGION --limit 20"
Write-Host ""
Write-Host "3) Query BigQuery:"
Write-Host "   & '$SDK\bq.cmd' query --use_legacy_sql=false 'SELECT filename,date,tags,word_count FROM ``$PROJECT_ID.$DATASET_ID.$TABLE_ID`` ORDER BY date DESC LIMIT 10'"
