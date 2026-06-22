# 🚀 What is Antigravity? 
#### Antigravity is Google’s agentic development platform — a full ecosystem designed for building, running, orchestrating, and managing AI agents locally on your machine.

### A “central command center” for AI agents
It lets you:

    - Develop Agents
    - Launch agents
    - Monitor them
    = Orchestrate workflows
    - Run multiple agents in parallel
    - Schedule tasks
    - Manage workspaces
It’s basically Google’s all‑in‑one environment for the “agent‑first era.”

## The Antigravity Ecosystem:  4 Types

#### 1. Antigravity (the main app) : 

**Google’s full agent platform**
- Standalone desktop application
- Runs on macOS, Windows, Linux
- Manages multiple local agents
- Schedules tasks
- Orchestrates workflows
- Works independently of any IDE
This is the “command center.”

#### 2. Antigravity IDE : 

**Where you write agent code**
- The original agent‑focused IDE
- Has deep understanding of associated codebase
- Includes agent manager, artifacts, debugging tools
- Recommended for developers
This is the “coding environment.”

#### 3. Antigravity CLI : 

**Command-line control**
- Terminal-based interface
- Lets you interact with agents from the command line
This is the “power‑user tool.”

#### 4. Antigravity SDK : 

**Libraries to integrate agents into apps**
- Developer toolkit
- Lets you integrate Antigravity programmatically into your own systems
This is the “toolbox for building custom agent systems.”

## Antigravity - Projects 

#### Antigravity uses a project-centric approach to ensure the agents have access to the right files, tools, permissions and more.

- A project is a combination of folders defining the environment and the scope of your agent. 
- Project can work with one or multiple folders (e.g., a frontend and a backend repo), providing your agents with all of the context required for your codebase. 
- All projects have their own isolated agent settings, allowing you to customize different projects' security settings independently.

## Project Agent Settings:

#### All projects come with their own agent settings . Customize different projects' security settings independently.
- Security presets (review commands or not)
    - all terminal commands and file accesses to be reviewed by you before the agent can perform actions.
- Agent behavior (auto‑execute or require approval)
    - whether the agent executes the implementation plan with or without your review.
- Local permissions 
    - File paths, URLs, etc. allowed or blocked for the agent.
- MCP server configuration
    - configure which specific MCP Tools are allowed which prevents all globally configured MCP Servers to be made available to the agent in this project.
- configuere at any point in projects life cycle.
This is where you control how much power the agent has.


## 3. Starting Conversations
Once the project is created, we can:
- Start a conversation with the agent
- Ask questions
- Rename conversation threads
- Create multiple threads inside the same project
The UI groups conversations under each project so you can keep work organized.

## 4. slash commands in chat
In the project’s chat box, type / and you’ll see commands like:

    - /browser → launches a browser sub‑agent (needs Chrome + debug permission)

    - /schedule → set recurring or one‑off tasks (e.g., “run this every Monday 9:00 AM”)

#### We Can:
 -Type /browser → Antigravity asks Chrome for debugging permission.
- Approve it → the agent can now control a browser session.
    -  An explicit command to launch the browser and ask it to do something. It requires Google Chrome and permission in Google Chrome to start a debugging session.
- Type /schedule → configure when and how often the agent should run a task.
    - Useful if you'd like to set up recurring or one-off tasks for the agent to execute at fixed intervals or on a schedule (e.g. 9:00 AM on Monday, Wednesday).

(There’s also a UI way to schedule tasks in the Scheduling Commands section.)

## 5. Scheduling Commands

Schedule feature in Antigravity is a built‑in automation system that lets you create tasks your agent will run automatically. These tasks can be recurring (every day, every hour, every 20 minutes) or one‑time reminders.

It’s essentially a task scheduler for your AI agent, inside each project.

#### What it does
- Create reminders (daily, weekly, hourly, custom intervals)
- Automate repeated actions your agent should perform
- Run prompts on a schedule (e.g., fetch data, check systems, summarize files)
- Trigger tools or workflows at specific times
- Maintain multiple scheduled tasks per project
- Enable, disable, or delete tasks anytime

#### Examples:
-A daily 5 PM meeting reminder
- A break reminder every 20 minutes
Each task runs automatically at the specified time without you needing to open the app.

### What Your Prompts Can Do
Not just simple reminders, but scheduled prompts can be much more powerful, including:
- Running tools
- Calling external systems
- Fetching data
- Updating files
- Triggering workflows
- Running multi‑step agent actions
Anything you can ask the agent normally, you can automate on a schedule.

-------------------------------------------------------------------------------------------
# MCP Servers
**A standard to help connect agents to external systems**

MCP (Model Context Protocol) Servers are connectors that let your AI agent talk to external systems—databases, APIs, cloud services, tools, or your own custom backends.

- Think of them as plugins that give your agent new abilities.

#### They keep the agent:
- Grounded in your real data
- Integrated with your systems
- Able to perform real actions, not just chat

## Antigravity with MCP servers:

### 1. Built‑in MCP Server Integrations
You can install many Google Cloud–related MCP servers with one click, such as:
- BigQuery
- Cloud Storage
- Firestore
- Vertex AI tools
Each one exposes tools your agent can call.

### 2. Support for Local & Remote MCP Servers
You can connect:
- MCP servers running on your machine
- MCP servers running on your cloud or backend
Antigravity treats both the same way.

### 3. Easy Setup Through the UI

##### Inside Antigravity: 
    `Settings → Customizations → Add MCP+ `

 - This opens a list of available servers.
- Click +Add to install one, then fill in required details like:

    - Project ID
    - Database name
    - Credentials

### 4. Configuration Stored Locally
Antigravity saves your MCP server settings in:
```
$HOME/.gemini/config/mcp_config.json
```
If you already have MCP servers configured elsewhere, you can paste them into this file, and Antigravity will detect them.

### 5. Manage Servers in the UI
After adding servers:
 -Go to Settings → Customizations → MCP Servers
- Click Refresh if needed
- You’ll see all configured servers
- You can enable/disable each one
Clicking a server shows the tools it exposes

-----------------------------------------------------------------------------------

# What Artifacts Are & What They Do in Antigravity

#### Artifacts are the way Antigravity shows you exactly what the agent is thinking, planning, and doing.

###### They are automatically generated documents like:
- Task Lists
- Implementation Plans
- Walkthroughs
- Code diffs
- Screenshots
- Architecture diagrams
- Browser recordings
- Markdown summaries
They act as a transparent record of the agent’s reasoning and actions.

## Why Artifacts Matter ?

**Artifacts solve the trust gap and provides visibility into agents thinking.**

#### Instead of the agent saying “I fixed the bug,” Antigravity gives you:
- A plan
- The steps it took
- The code changes
- A walkthrough of what changed
- Screenshots before/after
You don’t have to guess — you can verify.

### Types of Artifacts (from the page)
#### 1. Task List
A step‑by‑step breakdown of how the agent plans to complete your request.
Shows which steps are done and which are pending.

#### 2. Implementation Plan
A technical blueprint describing what code changes will be made.
You review this before the agent proceeds.

#### 3. Walkthrough
A final summary after the task is completed.
Explains what changed and how to test it.

#### 4. Code Diffs
Not technically an artifact, but shown alongside them.
Lets you review and comment on code changes.

#### 5. Screenshots
Before/after UI captures when the agent interacts with interfaces.

### How You View Artifacts
**In the Antigravity interface:**
 - Toggle the Auxiliary Pane (top‑right corner)
- You’ll see a list of all artifacts generated for the current task
 -Click any artifact to open and review it

## Source Files + Artifacts in Antigravity

#### In addition to generating Artifacts (Task List, Implementation Plan, Walkthrough), Antigravity also produces actual source files when the agent writes or modifies code. These files appear alongside artifacts in the Auxiliary Pane.

##### Examples include:
- package.json
- index.js
- Any other files the agent creates or edits

**You don’t need a full IDE to view them.**

#### Inside Antigravity, you can:
 -Click the file
- View its contents
- Add comments
- Review changes

#### This makes Antigravity a self‑contained development environment, where you can see both:
- The agent’s reasoning (Artifacts)
- The agent’s output (Source Files)
All in one place, without switching tools.

-------------------------------------------------------------------
# Antigravity IDE

## What the Antigravity IDE Is & What It Does

##### The Antigravity IDE is a full development environment that works alongside the main Antigravity app.

**In other words: The Antigravity IDE is a dedicated coding workspace where you can view, edit, and collaborate with the agent on your project’s code — all without leaving Antigravity.**

#### Like : 
- It looks and behaves like a traditional IDE (VS Code, JetBrains, etc.) but is designed specifically for agent‑assisted coding.
- You can open it directly from Antigravity using the “Open IDE” button in the Auxiliary Panel.

### What it does
The Antigravity IDE gives you:

#### 1. A full file explorer
You can see all files the agent created or modified:

    - package.json
    - index.js
Any new folders or code files

#### 2. A built‑in code editor
**You can:**
- View code
- Edit code
- Comment on code
- Review changes
No external editor required.

#### 3. An Agent Panel inside the IDE
This is a chat window where you can:
- Ask the agent to explain code
- Request fixes
- Generate new code
- Modify existing files
- Debug issues
It’s like having the Antigravity agent inside your IDE.


---------------------------------------------------------------------------------------------------------

# Skills:

## What Skills Are & What They Do in Antigravity

#### Skills are small, modular packages of knowledge or instructions that Antigravity loads only when needed.

- They prevent the agent from being overloaded with every rule, tool, or guideline all at once.
- Think of them as on‑demand expertise modules.

## Why Skills ?
##### Without skills, the agent would need:
- All your rules
- All your tools
- All your team standards
- All your workflows
…loaded into its context window every time.

##### That causes:
- Tool bloat
- Higher cost
- Slower responses
- Confusion
Skills fix this through progressive disclosure — they stay dormant until your request matches their description.

## Structure and Scope
##### Skills are directory-based packages. You can define them in two scopes depending on your needs:

### 1. Global Scope
 - ~/.gemini/skills/  
- Available everywhere: Antigravity, CLI, all projects.

### 2. Product Scope
- Antigravity: ~/.gemini/antigravity/skills/
- Antigravity CLI: ~/.gemini/antigravity-cli/skills/
- Available only to that specific product.

### 3. Project Scope
- <project-root>/.agents/skills/  
- Available only inside one project.

- For the codelab, you use Product Scope.

## The Anatomy of a Skill

**A typical skill directory looks like this :**

<img src="../Images/skills_antigravity.png" width="350" height="400">

#### The SKILL.md file contains:
 - Metadata (name, description)
 - Instructions the agent will load only when needed

 ## Code review skills:
 
 **create the SKILL.md file, that will contain the metadata and the skills instructions.**

 #### Skill.md:
 - contains the metadata (name and description) at the top and then the instructions. 
 
 ##### Note: When the agent loads, it will only read the metadata of the skills and it will only load the full skills instructions, only when needed.

















-----------------------------------------------------------------------------------------------------------

## Tool Installation 
Antigravity treats your project folder like a normal local workspace

### Run NPM:
- npm is safe to use inside your project folder
- Safely run:
```
npm init -y
npm install <package>
npm run dev
```
only inside the project folder

## What npm is used for in Antigravity projects
- Building frontend UIs
- Running local servers
- Installing MCP servers
- Installing tools or utilities
- Running scripts your agent might call
Google’s examples often use Python, but npm is fully supported.

### Run npx 
- Is just a runner for npm packages.

You can safely run commands like:
```
npx create-react-app myapp
npx @modelcontextprotocol/cli init
npx tailwindcss init
npx ts-node script.ts
…as long as you run them inside your project folder
```
Inside the project folder






