# Deploy an ADK agent to Agent Runtime using Agents CLI


## Goal:  
You’ll take an ADK 2.0 agent that you’ve been running locally and deploy it to Agent Runtime on Google Cloud using agents-cli.

## Big picture:

**Local → Cloud:** Start with a `local Ambient Expense Agent` and end with it running in the `cloud.`

**Production mindset:** You’re not just `“running code”; you’re packaging, verifying, deploying, and observing a production‑grade workflow.`

**Tooling:** You’ll use `Agents CLI, ADK 2.0, and Google Cloud` together.

## 1. Overview

### 1.1 What this lab is about

## Story:  

##### You’re working with the Ambient Expense Agent—an ADK 2.0 graph‑based workflow that:
- Auto‑approves standard, low‑risk expenses.
- Flags higher‑risk or large expenses for human‑in‑the‑loop review.
- Uses a graph workflow (nodes, edges, branching) instead of a single monolithic LLM call.

### In this codelab, you:
- Start from a local prototype of this agent.
- Prepare it for deployment (descriptors, configs, wrappers).
- Deploy it to Agent Runtime using agents-cli.
- Inspect traces in Cloud Trace to see how it behaves in production.

## 1.2 What you’ll learn (step‑by‑step view)

## 1.2.1 Prepare your local Ambient Expense Agent for cloud hosting

### Step 1: Make sure your Ambient Expense Agent project exists locally (from earlier codelabs).
### Step 2: Confirm it’s using ADK 2.0 and a graph workflow (function nodes, edges, etc.).
### Step 3: Clean up the project:
- Organize code into a clear structure (e.g., agent/, specs/, tests/).
- Ensure your entrypoint (the main workflow) is clearly defined.

### Step 4: Verify it runs locally:

#### Run your local commands (e.g., make playground or python -m ...) and confirm:
- The workflow executes.
- The expense logic (approve vs. escalate) behaves as expected.

## 1.2.2 Scaffold deployment descriptors and production wrappers

### Step 1: Use agents-cli to initialize deployment config (the codelab will give exact commands later, e.g. agents-cli deploy init).
### Step 2: This usually creates:

#### A deployment descriptor (YAML/JSON) describing:
- Which workflow to run.
- Which models/tools it uses.
- Runtime settings (timeouts, environment).
- Optional wrappers (e.g., HTTP handlers, adapters) that make your workflow callable by Agent Runtime.

### Step 3: Open the generated files and:
- Check model names (e.g., gemini-1.5-flash vs newer).
- Check environment variables (API keys, project IDs).
- Align them with your local .env or config.

## .2.3 Perform dry‑runs and deploy with Agents CLI

### Step 1: Run a dry‑run deployment:
- A command like `agents-cli deploy dry-run` (exact syntax will appear later in the codelab).

#### This checks:
- Config validity.
- That the workflow can be packaged.

### Step 2: Fix any issues reported:
- Missing env vars.
- Invalid model names.
- Import errors in your Python code.

### Step 3: Run the actual deployment:
- A command like agents-cli deploy run or similar.
- This uploads your agent to Agent Runtime in your Google Cloud project.

### Step 4: Note the deployed agent ID / endpoint—you’ll use this to send requests.

## 1.2.4 Monitor execution traces in Cloud Trace

### Step 1: Go to Google Cloud Console → Cloud Trace.

### Step 2: Filter by:
- Your project.
- The service/agent name used by the deployment.

### Step 3: Trigger your agent:
- Send a test expense request (the codelab will give you a sample payload).

### Step 4: Watch the trace:
- See each node in the graph.
- Check latency, errors, and branching decisions (approve vs. escalate).

### Step 5: Use this to:
- Debug mis‑routing.
- Validate that your production behavior matches your local expectations.

## 1.3 What you’ll need 

### 1.3.1 An active Google Cloud project with billing enabled

#### Why: Agent Runtime and Cloud Trace are Google Cloud services; they need a project with billing.

### Checklist:
- You have a Google Cloud project ID.
- Billing is enabled for that project.

### 1.3.2 The gcloud SDK installed and authenticated

#### Why: gcloud is your command‑line bridge to Google Cloud.

### Checklist:
- gcloud --version works in your terminal.

### You’ve run:
- gcloud init (to set project & region).
- gcloud auth login (to log in).

#### Your active project is the one you’ll deploy to:
- gcloud config get-value project

### 1.3.3 The uv package manager installed

#### Why: The course uses uv to manage Python environments and dependencies quickly.

### Checklist:
- uv --version works.
- You can run commands like:
- uv run python main.py
- uv add <package>

### 1.3.4 Google Antigravity IDE installed

#### Why: Antigravity is your AI coding environment for:
- Vibe‑coding the agent.
- Managing specs and skills.
- Running local workflows.

### Checklist:
- You can open Antigravity.
- You can open your Ambient Expense Agent project folder inside it.

## 1.4 Prerequisites (what you should already be comfortable with)

### 1.4.1 Terminal navigation

### You should be able to:
- cd into your project folder.

### Run commands like:
- ls / dir
- uv run ...
- agents-cli ...

### 1.4.2 Basic Python development

### You should understand:
- How to install dependencies (e.g., via uv or pip).
- How to run a Python script or module.
- Basic project structure (packages, modules, imports).

### 1.4.3 Fundamental Google Cloud concepts

#### You should roughly know:
- What a project is.
- That services (like Agent Runtime, Cloud Trace) are enabled per project.
- That IAM / permissions control what you can do.

-----------------------------------------------------------------------------
# 2. Set up your Google Cloud Environment

**Before deploying anything, you must configure your Google Cloud project and enable the APIs required for:**

- Agent Runtime
- Cloud Run
- Pub/Sub
- Cloud Trace
- Generative AI models
You will do this inside Antigravity, but here’s the exact meaning of each step so you understand what’s happening.

## ✅ 2.1 What You Need Before Running the Prompt

#### Make sure you have:
- Your Google Cloud Project ID
- gcloud installed and working (you already fixed this 🎉)
- You are logged in (gcloud auth login)
- You have Application Default Credentials (gcloud auth application-default login)

## ✅ 2.2 The Prompt You Give to Antigravity
- Inside Antigravity, paste this:
```
Help me set up my Google Cloud environment. Connect to my project
`YOUR_PROJECT_ID` in the global region, authenticate, and enable the necessary
generative platform APIs (aiplatform.googleapis.com, cloudtrace.googleapis.com,
cloudbuild.googleapis.com, agentregistry.googleapis.com).
```

### Replace:
```
YOUR_PROJECT_ID
with your actual project ID, e.g.: *****
```


## ✅ 2.3 What Antigravity Will Do (Behind the Scenes)
**Antigravity will propose and run the following steps:**

### 1. Set your active project

**Equivalent to:**

bash
```
gcloud config set project YOUR_PROJECT_ID
```

### 2. Set region to global

**Equivalent to:**

bash
```
gcloud config set compute/region global
```

### 3. Authenticate your user

**Antigravity will show a URL like:**

Code
```
https://accounts.google.com/o/oauth2/auth?...
```

- You click it → sign in → return to Antigravity.

**Equivalent to:**
bash
```
gcloud auth login
```

### 4. Enable Application Default Credentials

**Equivalent to:**

bash
```
gcloud auth application-default login
```

### 5. Enable required APIs
- Antigravity will run commands like:

bash
```
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudtrace.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable agentregistry.googleapis.com
```

## These APIs are required for:
- Agent Runtime
- Cloud Trace
- Cloud Build
- Model execution

## ⚠️ Important Note (from the codelab)

#### If this is a brand‑new Google Cloud project, you may see:

Code
```
Service Usage API must be enabled
```

#### If that happens:
- Antigravity will show a link
- Click it
- Enable Service Usage API in the Cloud Console
- Return to Antigravity and continue
- This is normal.

## Once Antigravity finishes:
- Your project is authenticated
- All required APIs are enabled
- Your environment variables are set
You’re ready to build the Manager Dashboard and deploy it to Cloud Run
---------------------------------------------------------------------------------

# ⭐ 3. Set up Agents CLI & ADK Skills — What This Step Really Means

### Antigravity needs the Agents CLI toolchain + ADK skills so it can:
- Scaffold ADK agent projects
- Deploy agents to Agent Runtime
- Run evaluation workflows
- Manage your agent lifecycle
- Understand ADK APIs and patterns

### When you run the prompt, Antigravity will:
- Open a terminal
- Run uvx google-agents-cli setup

- nstall the CLI + skills into your environment
- Run agents-cli info
- Show you a list of installed skills (e.g., google-agents-cli-deploy, google-agents-cli-workflow, etc.)
- This equips Antigravity to build and deploy your dashboard later.

### ⭐ Where do you paste the prompt?
##### 👉 Paste it in the main Antigravity chat window (Antigravity 2.0)
**NOT in the IDE.**
- Same place you pasted the Google Cloud setup prompt.

### ⭐ The exact prompt to paste
#### Paste this into Antigravity:

Code
```
Install the agents-cli toolchain and its ADK skills so you can help me build
an ADK agent. Run "uvx google-agents-cli setup", then confirm with
"agents-cli info" and tell me which skills are now available.
```

## Antigravity will:
- Show an implementation plan
- Ask you to approve
- Run the commands
- Show the installed skills
- You just click Approve whenever it asks.

### ⭐ What you should see after installation

#### When Antigravity runs:

bash
```
agents-cli info
```

### You should see skills like:
- google-agents-cli-deploy
- google-agents-cli-workflow
- google-agents-cli-eval
- adk-cheatsheet
- adk-scaffold
This confirms everything is installed correctly.

### ⭐ Notes from the codelab (in simple terms)
#### ✔ Antigravity may show a plan before running commands
Just click Approve.

#### ✔ If you hit quota
Switch to another model inside Antigravity (Gemini 2.0 Flash, Flash Lite, etc.)

#### ✔ You only need to install Agents CLI once
After that, Antigravity remembers the skills.

--------------------------------------------------------------------------------------

# ⭐ 4. Create your agent project

#### Now that:
- Your Google Cloud environment is configured
- Your Agents CLI + ADK skills are installed
- Antigravity is fully equipped
- …you’re ready to scaffold a brand‑new Ambient Expense Agent that is fully compatible with ADK 2.0.

### This step generates:
- A complete ADK 2.0 project folder
- A graph workflow with nodes
- A auto_approve node for < $100
- A review_agent node that triggers a RequestInput pause for ≥ $100
- A runnable prototype you can deploy later

### ⭐ The exact prompt to paste
Code
```
Use Agents CLI to build a local prototype for an ambient expense agent that
streamlines employee expense reporting by instantly approving standard claims
while flagging larger expenses for review. Ensure the graph workflow is
compatible with ADK 2.0 and includes an `auto_approve` node that automatically
approves expenses under $100, and a `review_agent` node that triggers a
human-in-the-loop pause (`RequestInput`) for expenses of $100 or more.
```

## ⭐ What Antigravity will do behind the scenes

### When you paste that prompt, Antigravity will:

### 1. Propose an implementation plan
You click Approve.

### 2. Run the scaffold command
**Equivalent to:**

bash
```
agents-cli scaffold create expense-agent --adk
```

#### This generates a folder like:
```
expense-agent/
  app/
    agent.py
    nodes/
    tools/
  pyproject.toml
  README.md
```

### 3. Modify the generated workflow

**Antigravity will:**
- Ensure the workflow uses ADK 2.0 graph syntax
- Add an auto_approve node:
- Runs deterministic Python
- Approves expenses < $100

#### Add a review_agent node:
- Calls Gemini
- Triggers RequestInput for human review

#### Wire the edges correctly:
- start → auto_approve
- auto_approve → end (if < $100)
- auto_approve → review_agent (if ≥ $100)
- review_agent → end (after human decision)

### 4. Show you the generated code

### Antigravity will open the IDE panel and display:
- The workflow graph
- The node implementations
- The routing logic
- The human‑in‑the‑loop pause
You can ask Antigravity to explain any part of the code.

-------------------------------------------------------------------------------

# 5. Prepare for Production Deployment

**Now that your Ambient Expense Agent works locally, it’s time to prepare it for Agent Runtime, Google Cloud’s fully managed hosting environment for AI agents.**

##### This step upgrades your local project so it can be deployed as a production‑grade cloud service.

## ⭐ Why Deploy to Agent Runtime?
- Local agents (running on your laptop):
- Stop running when you close your machine
- Have no persistent memory
- Cannot be accessed by a frontend
- Cannot scale
- Cannot be monitored
- Agent Runtime solves all of this by giving you:

### ✔ Always‑on execution
Your agent runs 24/7 in Google Cloud.

### ✔ Managed stateful sessions
Agent Runtime stores conversation state and long‑term memory.

### ✔ Secure sandboxing
Tool calls and code execution happen in isolated environments.

### ✔ Enterprise observability
Telemetry streams automatically to Cloud Trace and Cloud Logging.

### ✔ A public endpoint
Your frontend (Cloud Run dashboard) will call this endpoint in the next codelab.

## ⭐ What This Step Does
You will ask Antigravity to enhance your local project with production deployment files.

## This adds:

### 1. app/agent_runtime_app.py
A production‑ready wrapper that exposes your agent as a cloud service.

### 2. deployment_metadata.json
A schema that tells Agent Runtime how to provision resources.

### 3. No changes to your core logic
Your app/agent.py stays exactly the same.

### ⭐ What You Need to Do

#### Paste this prompt into Antigravity (main chat):

```
Scaffold the production deployment files for Agent Runtime.
```

### Antigravity will:
- Show an implementation plan
- Ask you to approve

### Run the command:

```
agents-cli scaffold enhance --deployment-target agent_runtime --yes
```

- Generate the production files
- Show them in the IDE panel

-----------------------------------------------------------------------------------

# 6. Packaging and Local Verification

## Before you deploy your agent to Agent Runtime, you need to:
- Lock your Python dependencies
- Run a dry‑run deployment to catch issues early
- This prevents version drift, dependency conflicts, and misconfigured deployment metadata.
- Antigravity handles all of this for you with a single prompt.

## ⭐ What this step does

### 1. uv lock

### This creates a deterministic lockfile (like uv.lock), ensuring:
- The exact same package versions run locally and in the cloud
- No surprises during deployment
- Reproducible builds

### 2. agents-cli deploy --dry-run
- This simulates a deployment without uploading anything.

### It checks:
- Your project structure
- Your deployment metadata
- Your Python environment
- Your dependencies
- Your Agent Runtime wrapper
- Your ADK graph validity
If something is wrong, you’ll see it here — before wasting time on a real deployment.

### ⭐ What you need to do
- Paste this into Antigravity (main chat):

```
Lock my python dependencies and run a dry-run deployment to check for any
configuration or dependency issues.
```

### Antigravity will:
- Show an implementation plan
- Ask you to approve

### Run:
```
uv lock
```

### Then run:
```
agents-cli deploy --dry-run
```
Show the dry‑run output in the terminal panel

### ⭐ What you should see

#### A successful dry‑run ends with something like:

```Dry-run complete. No issues detected.
Ready for deployment.
```

If there are warnings or errors, Antigravity will highlight them and you can fix them before deploying.

<img src=".././Images/expense_dryrun.png" width="500" height="400">

---------------------------------------------------------------------------------

# 7. Deploy to Agent Runtime

## Now that your project is:
- Scaffolded
- Enhanced for production
- Locked with deterministic dependencies
- Successfully dry‑run tested
…you’re ready to deploy your Ambient Expense Agent to Agent Runtime.

**This step turns your local agent into a fully managed, always‑on cloud service with a public endpoint.**

## ⭐ What this step does

### When you ask Antigravity to deploy:
- It activates the google‑agents‑cli‑deploy skill

### It runs the deployment command:
```
agents-cli deploy --project YOUR_PROJECT_ID --region us-west1
```
- It packages your code
- Uploads it to Google Cloud
- Provisions an Agent Runtime instance
- Streams logs and progress in the terminal
- Finally prints your live endpoint URL
This process usually takes 5–10 minutes.

## ⭐ What you need to do
- Paste this into Antigravity (main chat):

```
Deploy this agent to Agent Runtime.
```

### Antigravity will:
- Show an implementation plan
- Ask you to approve
- Run the deployment
- Stream progress
- Display your live endpoint when done
- You just approve each step.

### ⭐ Optional: Avoid locking your terminal
**If you don’t want to wait in the terminal, you can tell Antigravity:**
```
Deploy this agent to Agent Runtime using the --no-wait flag.
```

### This runs:
```
agents-cli deploy --project YOUR_PROJECT_ID --region us-west1 --no-wait
```

#### Then later you can check status:
```
agents-cli deploy --status
```

### ⭐ Region Troubleshooting Tip

#### If deployment fails due to capacity or quota, try another region:
- us-central1
- us-east1
- us-west4
- europe-west1

#### The Google Cloud Region Picker can help you choose based on:
- Latency
- Price
- Carbon footprint

## ⭐ What you should see at the end

### A successful deployment ends with something like:
```
Deployment complete.
Your agent is now live at:
https://agent-runtime-xxxxxx-uc.a.run.app
This URL is your public backend endpoint.
```

You will use this in the next codelab to build your Manager Dashboard on Cloud Run.

<img src=".././Images/deployment_status.png" width="600" height="500">

---------------------------------------------------------------------------------------

# 8. Test your Agent

**Now that your agent is deployed to Agent Runtime, you should verify that it behaves correctly in production.**

## You can test it in two ways:
- Directly through Antigravity (recommended)
- Manually through the Google Cloud Console Playground
Both methods confirm that your workflow logic is functioning end‑to‑end.

## ⭐ Option A — Test using Antigravity (recommended)
- Paste this into Antigravity (main chat):
```
Test my deployed Agent Runtime engine with two test cases: first a standard
meal expense of $50 to verify automatic approval, and second, a client dinner
expense of $150 to verify that the human-in-the-loop pause is triggered.
```

## Antigravity will:
- Detect your deployed endpoint
- Send both test payloads
- Show the responses

## If something fails, it will:
- Debug the issue
- Fix the code
- Redeploy automatically
This is the easiest and most automated way to test.

## ⭐ Option B — Test manually in the Google Cloud Console

## If you prefer to test manually:

### 1. Open the Playground
- Go to Google Cloud Console
- Navigation menu → Agent Platform → Deployments
- Select your deployed agent
- Click Playground
This opens an interactive chat interface for your agent.

### ⭐ Test Case 1 — Auto‑Approval (< $100)
- Paste this JSON into the Playground:

json
```
{"data": {"amount": 50.0, "submitter": "user@example.com", "category": "meals", "description": "Lunch", "date": "2026-06-04"}}
```

### Expected behavior:
- The agent routes to auto_approve
- Returns a JSON response with "status": "approved"
This confirms your deterministic Python node is working.

### ⭐ Test Case 2 — Human‑in‑the‑Loop (≥ $100)
- Paste this JSON:

json
```
{"data": {"amount": 150.0, "submitter": "user@example.com", "category": "meals", "description": "Client dinner", "date": "2026-06-04"}}
```

### Expected behavior:
- The agent routes to review_agent
- Triggers a RequestInput pause
- The Playground UI will show a pending human decision
- You will see a prompt asking for Approve or Reject
- This confirms your HITL flow is functioning.

### ⭐ What success looks like

#### For the $50 test:

```
"status": "approved"
"node": "auto_approve"
```
#### For the $150 test:
```
"status": "pending_human_input"
"node": "review_agent"
"pause_reason": "RequestInput"
```
**Once you click Approve/Reject, the workflow resumes and completes.**

<img src=".././Images/payload_test.png" width="600" height="500">

-------------------------------------------------------------------------------------

# 9. Monitor and Observe your Production Agent

**Once your agent is deployed to Agent Runtime, Google Cloud automatically wires up full observability for you. You don’t need to add logging code or tracing hooks — it’s all built in.**

### Every time your agent:
- Receives an event
- Runs a node
- Calls a model
- Executes a tool
- Pauses for human input
- Agent Runtime streams telemetry into your Google Cloud project.
This gives you deep visibility into your agent’s behavior in production.

## ⭐ Where to Observe Your Agent

### You have three main observability tools:

### 1. Cloud Trace — Execution Maps & Latency

### Cloud Trace shows:
- End‑to‑end execution timelines
- Node‑by‑node spans
- Model latency
- Tool execution time
- Human‑in‑the‑loop pauses
- Errors and retries

### How to open Cloud Trace:
- Go to Google Cloud Console
- Navigation menu → Trace
- Select Trace Explorer
- You’ll see a waterfall diagram of your agent’s workflow.
This is incredibly useful for debugging slow model calls or verifying routing logic.

### 2. Cloud Logging — Real‑Time Logs

### Cloud Logging shows:
- Standard output
- Python print statements
- Errors and stack traces
- Tool call logs
- Request/response payloads
- Approval decisions

### How to open Cloud Logging:
- Google Cloud Console
- Navigation menu → Logging → Logs Explorer

### Filter by:
- resource.type="agentruntime.googleapis.com/AgentEngine"
- or your deployment name
You can watch logs stream in real time as you test your agent.

### 3. BigQuery Analytics (Optional)

#### If you enabled:
```
--bq-analytics
```
during scaffolding, your agent’s interactions are automatically written to BigQuery.

#### This lets you run SQL queries to analyze:
- Approval ratios
- Rejection trends
- Expense categories
- Model usage
- Human‑in‑the‑loop frequency
- Session lengths

### Example SQL (from the codelab)
sql
```
SELECT
  COUNTIF(REGEXP_CONTAINS(response_text, r'(?i)approved')) AS approved_count,
  COUNTIF(REGEXP_CONTAINS(response_text, r'(?i)rejected')) AS rejected_count,
  COUNT(1) AS total_processed,
  SAFE_DIVIDE(COUNTIF(REGEXP_CONTAINS(response_text, r'(?i)approved')), COUNT(1)) AS approval_ratio
FROM
  `[YOUR_PROJECT_ID].[YOUR_DATASET_ID].v_agent_response`
WHERE
  agent = 'expense_processor';
```
You can ask Antigravity to customize this query for your dataset.

### ⭐ What You Should Expect to See

#### For a $50 expense:
- Auto‑approval node executes
- Trace shows a short workflow
- Logs show "status": "approved"

#### For a $150 expense:
- Workflow pauses at review_agent
- Trace shows a RequestInput span
- Logs show "pending_human_input"
- BigQuery logs a HITL event (if enabled)

--------------------------------------------------------------------------------
# 10. (Optional) Verify Registration in Agent Registry

Your Ambient Expense Agent is now deployed to Agent Runtime, and one of the perks of using Agent Runtime is that your agent is automatically registered in the Gemini Enterprise Agent Registry.

### This registry is what allows:
- Other developers
- Other services
- Other agents
- Internal enterprise systems
…to discover, inspect, and reuse your agent safely.

**You don’t need to manually publish anything — Agent Runtime handles it for you.**

## ⭐ Why This Matters
Once registered, your agent becomes:

Discoverable across your organization

Version‑tracked

Governed under enterprise policies

Reusable by other teams

Visible in the Agent Registry UI

This is especially important in enterprise environments where multiple teams build agents that need to interoperate.

⭐ What You Need to Do
Paste this into Antigravity (main chat):

Code
Verify that my deployed expense agent is automatically registered in the Gemini
Enterprise Agent Registry.
Antigravity will:

Show an implementation plan

Ask you to approve

Run the command:

Code
agents-cli publish gemini-enterprise --list
Display a list of all registered agents in your project

Confirm that your Ambient Expense Agent appears in the registry

You should see an entry with:

Your agent’s name (e.g., expense-agent or expense_processor)

Its version

Its deployment metadata

Its registration status

This confirms your agent is discoverable and ready for enterprise use.

⭐ What Success Looks Like
You’ll see something like:

Code
Registered Gemini Enterprise Agents:
- expense_processor (active)
- version: 1
- runtime: agent_runtime
- project: divya-doc-pipeline
This means:

Your agent is live

Registered

Discoverable

Synced with Agent Runtime

Any future deployments will automatically update this registry entry.

⭐ You’ve Now Completed the Entire Backend Codelab
You have:

Built an ADK 2.0 agent

Added HITL logic

Prepared it for production

Deployed it

Tested it

Observed it

Verified registry registration

You’re officially ready for the next codelab:

Image - 

