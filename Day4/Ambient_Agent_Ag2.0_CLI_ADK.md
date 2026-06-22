# Vibecode an ADK 2.0 Ambient Agent with Antigravity and Agents CLI

## 1. Introduction
**In this lab you act as a software architect: you describe what you want in natural language, and Antigravity (Google’s agentic IDE) writes and edits the code. You then review, run, and verify everything locally.**

## You’ll use:
- Google’s Agent Development Kit (ADK 2.0) — graph‑based framework for AI agents
- agents-cli — command‑line toolchain for building, running, evaluating, and deploying ADK agents
- Antigravity — to “vibecode” the agent via prompts



## The use case: Corporate expense management

### You’ll build an event‑driven ambient expense agent that triages expense reports:
- Low‑value (< $100)
- Auto‑approved by deterministic Python (no LLM call)
- High‑value (≥ $100)
- Passes a pre‑LLM security screen
- Analyzed by Gemini for compliance risk
- Paused for human review before final decision

<img src=".././Images/cost_manager1.png" width="500" height="400">


## What you’ll do
- Configure Antigravity on your machine and load ADK skills.
- Initialize an ADK project structure.
- Build a stateful, graph‑based ADK 2.0 expense workflow by prompting.

## Add a mock security screen that:
- Redacts PII
- Short‑circuits prompt‑injection attacks before the LLM runs
- Test your workflow in the interactive ADK Playground (Human‑in‑the‑Loop flow).
- Make the agent ambient so event triggers (Pub/Sub‑style) drive it.
- Evaluate the agent with Agents CLI using LLM‑as‑judge metrics (via google-agents-cli-eval skill).

## What you’ll need
- Python 3.11+ and uv available in your terminal
- Antigravity installed (see official docs)
- Either:
    - A Google AI Studio API key, or
    - A Google Cloud project with appropriate access

## How to read the prompts
- Each build step includes a prompt you can paste into Antigravity’s chat.
- They’re starting points—you can rephrase them in your own words as long as the intent stays the same.

---------------------------------------------------------------------------------

# 2. Configure Antigravity

**Antigravity :** is Google's agentic IDE, a code editor paired with an AI agent that can read your project, run commands, and write files. You'll drive the entire lab from here.

### Important notes:
- Antigravity may show implementation plans or pop‑ups before running commands or writing files.

✔️ Review and approve these so it can proceed.
- If you run out of quota, switch to another available model inside Antigravity.

## Give Antigravity the ADK Skills
**To build ADK agents effectively, Antigravity needs the ADK skill set.**

### These skills include:
- ADK API references
- Project scaffolding helpers
- Agents‑CLI workflow integration
- Evaluation helpers
- Installing the agents‑cli toolchain automatically installs these skills.

## Installing agentCLI through Antigravity Prompt:
1. Open Antigravity select- New Project
2. Create a project folder `ambient_expense_agent` 
2. Create a project file 
- Prompt:
```
Install the agents-cli toolchain and its ADK skills so you can help me build an
ADK agent. Run "uvx google-agents-cli setup", then confirm with "agents-cli info"
and list all the skills that are available.
```
