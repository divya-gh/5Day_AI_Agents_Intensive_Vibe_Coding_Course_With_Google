# Vibe coding AI agents: managing the lifecycle with Agents CLI and ADK 2.0

**Build and manage a complete ADK 2.0 agent lifecycle—scaffold, run, evaluate, and (optionally) deploy—using Agents CLI.**

**You’ll go from “idea” to a working, testable agent in a structured, repeatable flow.**

## Introduction
#### ADK 2.0 gives you structured, graph‑based workflows for agents—nodes, tools, and orchestration in Python.   

#### Agents CLI wraps that with lifecycle commands: it knows how to scaffold projects, run agents, evaluate them, and ship them to production. 

#### `“Vibe coding”` here means: you stay in flow, describe what you want, and let the tooling handle boilerplate and lifecycle.

## What you’ll learn:
- How to install and set up agents-cli and its associated skills.
- How to scaffold a new agent project.
- The structure and key files of an ADK 2.0 graph workflow agent project.
- How to run automated linting and code cleanups.
- How to launch and use the local web playground for interactive testing with auto-reloading.

    - ADK 2.0 basics: graph‑based, code‑first agent workflows 
    - Agents CLI role: scaffolding, evaluation, deployment, observability around ADK agents 
    - End‑to‑end lifecycle: create → run → test/eval → iterate → deploy

## Prerequisites and setup
### Goal: Have the toolchain ready so every later command “just works”.

#### Install core tools:
Python: 3.11+ , Node.js: for skills installation, uv: modern Python package manager 


## 1. [Install Agents CLI](https://google.github.io/agents-cli/guide/getting-started/?utm_source=copilot.com)

bash
```
uvx google-agents-cli setup
```

#### This installs:
- agents-cli binary
- Agents CLI skills (for coding agents like Gemini CLI / Antigravity) 

#### Authentication (local dev)
bash
```
export GEMINI_API_KEY="your-key-here"
```
- This lets Agents CLI call Gemini models without needing full gcloud auth for simple local runs. 

## Install UV: 
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

```

## [Node.js 18+:](https://nodejs.org/en/download/prebuilt-installer)

----------------------------------------------------------------------------------

# 2. Set up Authentication & Environment

## Option 1 — Gemini API Key (Google AI Studio)
**If you’re using AI Studio and a standard Gemini API key.**

bash
```
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_ENTERPRISE=FALSE
```
#### Use this config:
- You want the simplest setup
- You’re running locally
- You’re not using Vertex AI enterprise features

## Option 2 — Google Cloud ADC (Vertex AI)
** If you’re using Vertex AI and want enterprise features.**

bash
```
gcloud auth application-default login
gcloud config set project <YOUR_PROJECT_ID>

export GOOGLE_GENAI_USE_ENTERPRISE=TRUE
export GOOGLE_CLOUD_PROJECT=REPLACE-WITH-YOUR-PROJECT_ID
export GOOGLE_CLOUD_LOCATION=REPLACE-WITH-LOCATION
```

#### Use this when:
- You want enterprise Gemini models
- You want to deploy to Google Cloud
- You want IAM‑based authentication

#### NOte: If you want the variable to persist across terminal sessions, add it to:

**Git Bash:** ```~/.bashrc or ~/.bash_profile```

**PowerShell:** ```$PROFILE```

## 3. Set up Agents CLI & Skills

#### install the agents-cli tool. : Done

- 👉 Open a terminal and run: ```uvx google-agents-cli setup```

### This command automatically installs:
- The Agents CLI tool globally on your system.
- Seven domain-specific coding assistant skills that Antigravity can use to help you build, scaffold, evaluate, and deploy agents. These skills are installed once globally into ~/.agents/skills/ and are automatically discovered by Antigravity.

##### Note: Skills are installed into ~/.agents/skills/ and picked up automatically by Antigravity. 
- You can verify this using the /skills command or your Antigravity settings.

------------------------------------------------

# 4. Create your Agent Project
**Create your Agent Project” using that Antigravity prompt and Agents CLI.**

## 1 Open Antigravity in your workspace
- Create a folder: `customer-support-agent` locally
- Open Antigravity → Select your local **workspace folder**

## 2 Confirm authentication and environment
**Ensure your terminal/IDE session already has Gemini or gcloud auth set so the agent can call models.**

#### For AI Studio key:
```
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_ENTERPRISE=FALSE
```
## 3 Open the coding agent panel in Antigravity

- Antigravity → Agent / Chat panel
- Verify that the panel is connected to your current workspace
- Optionally confirm that Agents CLI skills are installed 
```
What are the skills availabel?
```
- Will show ADK etc
- Prompt:
```
Use ADK 2.0 to create a new graph workflow agent project called
customer-support-agent. I don't want to deploy this agent, so you can skip
the deployment files. The workflow should act as a customer support
representative for a shipping company. It should first classify if the user
query is related to shipping (rates, tracking, delivery, returns) or
unrelated. If it is related to shipping, route to a shipping FAQ agent to
answer the question. If it is unrelated, route to a node that politely
declines to answer.
```
<img src=".././Images/customer_request.png" width="600" height="300">


### Checkout: 

## 1. Implementaion Plan
<img src=".././Images/customer_implimentaion.png" width="400" height="300">

## 2. Walkthrough
<img src=".././Images/custer_walkthrough.png" width="400" height="300">

## Queries:

![Shipping Querry 1](<img src=".././Images/shipping_query1.png" width="400" height="300">.png)

![Shipping Querry 2](<img src=".././Images/shipping_query2.png" width="600" height="300">.png)
---------------------------------------------------------------------------------

# 5. Explore the Agent Code

Prompt:
```
Read and explain the project structure of my new agent project. Walk me
through how `app/agent.py` is configured, highlighting the role of the
tools, nodes, edges, and the root Workflow.
```

### Check out the code walkthrough: Code_walkthrough.md

### Key Concepts

##### Workflow & Edges: In ADK 2.0, agent applications are orchestrated as a graph using Workflow. The edges list defines the execution flow, chaining nodes together from START and enabling conditional branching based on routes (e.g., routing to faq_agent on "shipping" or handle_unrelated on "unrelated").

##### LlmAgent: Declarative nodes that define LLM-powered tasks with specific instructions, models, and structured outputs (output_schema).

##### Nodes & Context: Python functions decorated with @node (or standard functions) that perform logic, access execution state via Context, and yield Event objects to pass data and routing signals along the graph.

##### Model: `gemini-3.1-flash-lite' is used as the default fast reasoning model.

##### App Wrapper: The top-level App object wraps the root workflow. External tools like the local playground, ADK evaluation harnesses, and Agent Runtime discover and execute your workflow through this standardized app interface.

-----------------------------------------------------------------------

# 6. Automated Linting

**Before running or testing your agent, it is a good practice to ensure your code is clean and formatted correctly.**

### 👉 Prompt Antigravity:
```
Run linting on my agent project to verify its health.
Antigravity will execute agents-cli lint behind the scenes to run pre-configured checks, verifying imports, syntax, and formatting consistency across your files.
```

<img src=".././Images/custom_code_linting.png" width="400" height="300">

------------------------------------------------------------------------------

# Interactive Testing with the Playground — Step‑by‑Step

**The local web playground is the fastest way to verify your agent's behavior. It provides an interactive chat interface where you can chat with your agent and inspect tool executions in real-time.**

## 01. Launch the local development playground

- Open Antigravity

- Ask Antigravity: “Launch the local development playground for my agent.”

    - Antigravity runs agents-cli playground for you
    - Wait for the terminal to show a local URL (usually http://127.0.0.1:8080/dev-ui/?app=app)
    - Copy and open the URL in your browser

<img src=".././Images/dev_playground.png" width="700" height="600">

## 02. Test Real-Time Auto-Reloading
- You can see how real-time edits to your agent are reflected in the Playground.
- Modify the faq_agent instruction in app/agent.py by asking Antigravity:
```
Modify the faq_agent instruction in app/agent.py to make the shipping rates
response more playful and enthusiastic. Add some emojis and highlight the
free shipping threshold.
```

- Send a new message to the agent in the playground to test the auto-reloading:
```
How much is standard shipping?
```
The playground automatically reloads and executes your updated code in real-time without needing a server restart! You should see some emojis in the response now.

<img src=".././Images/playground_test.png" width="700" height="600">

-----------------------------------------------------------------------

# 8. Command Line Execution
**For quick tests, automation, or scripting, you can ask Antigravity to run your agent directly from the terminal.**

### 👉 Prompt Antigravity:

```
Run a CLI query asking my agent how long standard delivery takes.
Antigravity will execute the query command (agents-cli run "How long does standard delivery take?"). This runs a quick single-turn inference and prints the agent's final response along with tool execution details.
```
- Antigravity will execute the query command (agents-cli run "How long does standard delivery take?"). This runs a quick single-turn inference and prints the agent's final response along with tool execution details.

<img src=".././Images/playground_terminal.png" width="500" height="500">

-----------------------------------------------------------------------------------

# 9. Cleanup

**To avoid leaving unwanted resources in your local environment, follow these cleanup steps:**

### Stop Local Servers: 
- If your agents-cli playground server is still running, stop it in your terminal by pressing `Ctrl + C.`

### Remove Local Project Files: 
- Delete the scaffolded agent project directory from your local machine.
```
rm -rf customer-support-agent
```

=--------------------------------------------------------------------------------=

# ✅ 10. Summary & Next Steps 

**We’ve now completed the full local development lifecycle of an AI agent using Agents CLI + ADK 2.0.**

## What you learned:
### 1. Installed & Configured Your Tools configured domain-specific workflow skills for Antigravity.
    - Installed Agents CLI
    - Enabled domain‑specific workflow skills inside Antigravity
    - Set up authentication (Gemini API Key or ADC)

### 2. Scaffolded a Complete Agent Project

### Created the customer-support-agent project using:
```
agents-cli scaffold create customer-support-agent --prototype --yes
```
- Let Antigravity generate the ADK 2.0 workflow structure

### 3. and Analyzed Explored ADK 2.0 Architecture

### Learned how ADK organizes agent logic:
- Workflow → the graph orchestrating execution
- Edges → define flow and conditional routing
- Nodes → Python functions that emit Events
- Conditional routing.
- LlmAgent → declarative LLM-powered nodes
- App → top-level wrapper that exposes your workflow to tools

### 4. Ensured Local Code Health
```
agents-cli lint
```
Verified formatting, imports, and code quality

### 5. Tested the Agent Interactively

#### Launched the local playground:
```
agents-cli playground
```

### Verified Behavior: Tested the agent interactively with real-time hot-reloading via the playground, and ran quick tests on the command line.

- Shipping questions → routed to faq_agent
- Unrelated questions → routed to handle_unrelated
- Observed real-time hot reloading when modifying code


## Step 2 — Understand What This Means

### We now know how to:
- Build an agent from scratch
- Understand and modify ADK 2.0 workflows
- Test and iterate locally
- Use Antigravity + Agents CLI together as a full development loop
This is the core skillset for building production-grade agents.

-------------------------------------------------------------------------------

## Next: 

### Path A — Evaluate Your Agent (Recommended Next Step)
Create an evalset (CSV or JSONL with prompts + expected behavior)

#### Run: Code
```
agents-cli eval run
```

#### Inspect:
- Accuracy
- Failure cases
- Regression risks
This is essential before deploying or scaling.

### Path B — Deploy to Enterprise Cloud Scale

### When ready to go beyond local: Package your agent
```
agents-cli deploy
```

### Deploy to:
- Agent Runtime
- Cloud Run

### Enable observability:
**Set up production telemetry to stream logs and execution traces to Cloud Trace and BigQuery.**
- Logs → Cloud Logging
- Traces → Cloud Trace
- Metrics → BigQuery
This gives you production-grade monitoring and reliability.

---------------------------------------------

## More Enhacements

### Path C — Extend Your Agent’s Capabilities

#### WE can add:
- More categories (billing, account issues, product info)
- Additional sub-agents
- External tools (APIs, databases, vector search)
- Memory or context windows
- Guardrails and validation
Antigravity can help you generate and refine all of these.

---------------------------------------------------------------

## Bookmark Key Resources

### Official references to use:

- Agents CLI GitHub Repository

- Agent Development Kit (ADK) Documentation

- Agent Platform Overview

