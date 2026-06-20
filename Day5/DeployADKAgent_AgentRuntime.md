# Deploy an ADK agent to Agent Runtime using Agents CLI


## Goal:  
You’ll take an ADK 2.0 agent that you’ve been running locally and deploy it to Agent Runtime on Google Cloud using agents-cli.

Big picture:

Local → Cloud: Start with a local Ambient Expense Agent and end with it running in the cloud.

Production mindset: You’re not just “running code”; you’re packaging, verifying, deploying, and observing a production‑grade workflow.

Tooling: You’ll use Agents CLI, ADK 2.0, and Google Cloud together.

1. Overview
1.1 What this lab is about
Story:  
You’re working with the Ambient Expense Agent—an ADK 2.0 graph‑based workflow that:

Auto‑approves standard, low‑risk expenses.

Flags higher‑risk or large expenses for human‑in‑the‑loop review.

Uses a graph workflow (nodes, edges, branching) instead of a single monolithic LLM call.

In this codelab, you:

Start from a local prototype of this agent.

Prepare it for deployment (descriptors, configs, wrappers).

Deploy it to Agent Runtime using agents-cli.

Inspect traces in Cloud Trace to see how it behaves in production.

1.2 What you’ll learn (step‑by‑step view)
1.2.1 Prepare your local Ambient Expense Agent for cloud hosting
Step 1: Make sure your Ambient Expense Agent project exists locally (from earlier codelabs).

Step 2: Confirm it’s using ADK 2.0 and a graph workflow (function nodes, edges, etc.).

Step 3: Clean up the project:

Organize code into a clear structure (e.g., agent/, specs/, tests/).

Ensure your entrypoint (the main workflow) is clearly defined.

Step 4: Verify it runs locally:

Run your local commands (e.g., make playground or python -m ...) and confirm:

The workflow executes.

The expense logic (approve vs. escalate) behaves as expected.

1.2.2 Scaffold deployment descriptors and production wrappers
Step 1: Use agents-cli to initialize deployment config (the codelab will give exact commands later, e.g. agents-cli deploy init).

Step 2: This usually creates:

A deployment descriptor (YAML/JSON) describing:

Which workflow to run.

Which models/tools it uses.

Runtime settings (timeouts, environment).

Optional wrappers (e.g., HTTP handlers, adapters) that make your workflow callable by Agent Runtime.

Step 3: Open the generated files and:

Check model names (e.g., gemini-1.5-flash vs newer).

Check environment variables (API keys, project IDs).

Align them with your local .env or config.

1.2.3 Perform dry‑runs and deploy with Agents CLI
Step 1: Run a dry‑run deployment:

A command like agents-cli deploy dry-run (exact syntax will appear later in the codelab).

This checks:

Config validity.

That the workflow can be packaged.

Step 2: Fix any issues reported:

Missing env vars.

Invalid model names.

Import errors in your Python code.

Step 3: Run the actual deployment:

A command like agents-cli deploy run or similar.

This uploads your agent to Agent Runtime in your Google Cloud project.

Step 4: Note the deployed agent ID / endpoint—you’ll use this to send requests.

1.2.4 Monitor execution traces in Cloud Trace
Step 1: Go to Google Cloud Console → Cloud Trace.

Step 2: Filter by:

Your project.

The service/agent name used by the deployment.

Step 3: Trigger your agent:

Send a test expense request (the codelab will give you a sample payload).

Step 4: Watch the trace:

See each node in the graph.

Check latency, errors, and branching decisions (approve vs. escalate).

Step 5: Use this to:

Debug mis‑routing.

Validate that your production behavior matches your local expectations.

1.3 What you’ll need (with beginner‑friendly notes)
1.3.1 An active Google Cloud project with billing enabled
Why: Agent Runtime and Cloud Trace are Google Cloud services; they need a project with billing.

Checklist:

You have a Google Cloud project ID.

Billing is enabled for that project.

1.3.2 The gcloud SDK installed and authenticated
Why: gcloud is your command‑line bridge to Google Cloud.

Checklist:

gcloud --version works in your terminal.

You’ve run:

gcloud init (to set project & region).

gcloud auth login (to log in).

Your active project is the one you’ll deploy to:

gcloud config get-value project

1.3.3 The uv package manager installed
Why: The course uses uv to manage Python environments and dependencies quickly.

Checklist:

uv --version works.

You can run commands like:

uv run python main.py

uv add <package>

1.3.4 Google Antigravity IDE installed
Why: Antigravity is your AI coding environment for:

Vibe‑coding the agent.

Managing specs and skills.

Running local workflows.

Checklist:

You can open Antigravity.

You can open your Ambient Expense Agent project folder inside it.

1.4 Prerequisites (what you should already be comfortable with)
1.4.1 Terminal navigation
You should be able to:

cd into your project folder.

Run commands like:

ls / dir

uv run ...

agents-cli ...

1.4.2 Basic Python development
You should understand:

How to install dependencies (e.g., via uv or pip).

How to run a Python script or module.

Basic project structure (packages, modules, imports).

1.4.3 Fundamental Google Cloud concepts
You should roughly know:

What a project is.

That services (like Agent Runtime, Cloud Trace) are enabled per project.

That IAM / permissions control what you can do.