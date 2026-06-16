# Build and deploy to Google Cloud with Antigravity

##### Using Google Antigravity to design, build, and deploy a serverless, event‑driven document pipeline on Google Cloud:

- Files uploaded to Cloud Storage (GCS)
- Processed by a Python Cloud Run service using Gemini on Vertex AI
- Metadata streamed into BigQuery

## 2. Prerequisites
- Google Antigravity installed (desktop app)
- Google Cloud project with billing enabled
- gcloud CLI installed and authenticated

## What we learn : 

- How to use Antigravity for architectural planning and design.
- Generate infrastructure as code (shell scripts) with an AI agent.
- Build and deploy a Python based Cloud Run service.
- Integrate Gemini on Vertex AI for multimodal document analysis.
-Verify the end-to-end pipeline using Antigravity's Walkthrough artifact.

### Permissions to create:
- Cloud Storage buckets
- Cloud Run services
- BigQuery datasets/tables
- Pub/Sub topics (if used in the codelab)

----------------------------------------------------------------------------------

## 3. High‑level architecture

**We want to build a serverless and event-driven document pipeline that ingests files from Google Cloud Storage (GCS), processes them using Cloud Run and Gemini, and streams their metadata into BigQuery.**

- GCS bucket — user uploads documents (PDFs, images, etc.)
- Event trigger — upload event triggers Cloud Run (via Pub/Sub or direct event)
- Cloud Run service (Python) — calls Gemini on Vertex AI for multimodal analysis
- BigQuery — stores extracted metadata (title, entities, labels, etc.)
- Antigravity Walkthrough — used to validate the end‑to‑end pipeline

### Rough Diagram:
 
<img src="../Day_build_deply_agty_GCP.png" width="350" height="400">


##### Note: Antigravity can help us to figure out the architecture details as we go along. However, it helps to have an idea on what you want to build. The more detail you can provide, the better results you'll get from Antigravity in terms of architecture and code.

## Planning Architecture:

### Step 1 — Plan the architecture in Antigravity

- Open Antigravity.
- Create a new project for this pipeline.
- In the Agent / Chat panel, describe the target architecture, for example:

##### Prompt: 
- Type /grill-me and then enter the following prompt 

        **“Design a serverless document processing pipeline on Google Cloud. Use Cloud Storage for input, Cloud Run (Python) for processing with Gemini on Vertex AI, and BigQuery for metadata storage. Generate a high‑level architecture and list all required resources.”**

- The /grill-me command asks a number of follow up questions that you can try to answer to the best of your knowledge. It also suggests Recommended Answers and you can go with that if you'd like.
- Save the generated architecture diagram / notes as an Antigravity artifact (e.g., Architecture.md).

## Step 3 — Implement the Cloud Run Python service

When Antigravity asksquestions, select folllowing answers:

- “Generate a Python Cloud Run service that:
- Receives a GCS event (file path, bucket)
- Downloads the file
- Sends it to Gemini on Vertex AI for multimodal analysis
- Extracts metadata (title, summary, entities, labels, etc.)
- Writes a row into a BigQuery table.”

### Implementation Plan and Task List

Antigravity will now get to work and generate an `Implementation Plan.` It puts it up for your review by giving you a message similar to the one below:

### Implimentation_plan:
- click the Auxiliary Pane toggle in the top right window and view the Artifacts generated, which at this point is just the Implementation Plan.

## Step 4 = Antigravity builds your entire project automatically.

- Creates the folder
- Generates all code
- Writes deployment scripts
- Writes cleanup scripts
- Writes documentation
- Writes the Cloud Run service
- Writes the OCR simulator
- Writes the BigQuery schema
- Writes the Pub/Sub wiring
- Writes the Walkthrough

#### And then tells you:
 
 `“Run ./deploy.sh to deploy the pipeline.”`

## step 5. Deploy the application

**Type: “Run the deploy.sh for me”**

##### Antigravity:
- Asks permission
- Runs the script in the background
- Streams logs
- Deploys your entire pipeline
- Notifies you when done

------------------------------------------------------------------------------------------------
## Manual verification

1. Cloud Storage
Goal: Verify the bucket exists and check for uploaded files.

Navigate to Cloud Storage > Buckets.
Locate the bucket named document-processing-ingest-{project-id}.
Click on the bucket name to browse files.
Verify: You should see your uploaded files (e.g.,cloud_test_sample.txt).

<img src="../cloud_bucket.png" width="350" height="400">


2. Pub/Sub
Goal: Confirm the topic exists and has a push subscription.

Navigate to Pub/Sub > Topics.
Find document-uploads-topic.
Click on the topic ID.
Scroll down to the Subscriptions tab.
Verify: Ensure doc-uploads-sub is listed with "Push" delivery type.

<img src="../pubSub_topic.png" width="350" height="400">

3. Cloud Run
Goal: Check the service status and logs.

Navigate to Cloud Run.
Click on the service document-processor.
Verify:
Health: Green checkmark indicating the service is active.
Logs: Click the Logs tab. Look for entries like "Processing file: gs://..." and "Successfully inserted...".

<img src="../Cloud_run.png" width="350" height="400">

4. BigQuery
Goal: Validate the data is actually stored.

Navigate to BigQuery > SQL Workspace.
In the Explorer pane, expand your project > document_processing dataset.
Click on the processed_metadata table.
Click on the Query tab and retrieve all rows from the table via the SELECT * statement.
Verify: You should see rows containing filename, process_timestamp, tags, and word_count.

<img src="../bigquerry_table.png" width="350" height="400">


8. 8. Extend the application : No Quota

9. Run ./teardown.sh

$ ./teardown.sh

============================================================
⚠   This will PERMANENTLY DELETE all pipeline resources!
  Project : daykgadkproj
============================================================
  Type 'yes' to continue: yes
Updated property [core/project].

▶ Deleting Pub/Sub subscription: doc-processor-push-sub
⚠ Subscription not found — skipping

▶ Removing GCS notifications on gs://daykgadkproj-doc-uploads
⚠ Bucket not found — skipping notification removal

▶ Deleting Pub/Sub topic: document-upload-events
⚠ Topic not found — skipping

▶ Deleting Cloud Run service: doc-processor
⚠ Cloud Run service not found — skipping

▶ Deleting GCS bucket: gs://daykgadkproj-doc-uploads
⚠ Bucket not found — skipping

▶ Deleting BigQuery dataset: docpipeline_dataset
⚠ Dataset not found — skipping

▶ Deleting Container Registry image: gcr.io/daykgadkproj/doc-processor
⚠ Image not found or already deleted

============================================================
  ✅  Teardown complete. All pipeline resources deleted.
============================================================

