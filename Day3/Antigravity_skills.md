# Authoring Google Antigravity Skills

## 📖 what is Google Antigravity ?

**It is an agentic development platform that acts as the command center for your AI agents.**

#### It lets you:
- Launch agents
- Monitor their actions
- Orchestrate workflows
- Extend capabilities using Skills

## 📖 What is Agent Skills?
**Agent Skills, a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows**

### Agent skills are small, portable folders that contain:
- Instructions
- Workflows
- Tools
- Code snippets
- Templates
- Domain knowledge
They allow your agent to temporarily “gain expertise” in a specific domain without bloating its system prompt.


## 🎯 Goal
- Build your first Google Antigravity Agent Skills — lightweight, modular capability packs that extend your AI agent with specialized workflows such as:

        - Git formatter
        - Template generator
        - Tool scaffolding
        - Custom utilities
By the end, you will have multiple working Skills that Antigravity can load and execute. 

📘 What We Will Learn
- What Agent Skills are 
- Thier benifits and why they matter
- How Skills are Constructed and how they are structured (SKILL.md, scripts/, references/)
- How Antigravity discovers and loads Skills
- How to build Skills step-by-step
- How to test Skills inside Antigravity
- How to extend Skills with scripts and workflows

## 🧰 Prerequisites
##### Before starting, ensure you have:

#### ✔ Antigravity installed
You should already have run the installer and authenticated.

#### ✔ Basic understanding of Antigravity
Recommended: complete Getting Started with Google Antigravity.

#### ✔ A working development environment
- macOS, Linux, or Windows
- Terminal / Shell
- A code editor (VS Code recommended)

#### ✔ Basic familiarity with
- Markdown
- Python or JavaScript (optional but helpful)
- File system navigation

-------------------------------------------------------------------

## 2. Why Skills?
#### `Skills shift agents from “load everything upfront” to “load only what the user needs,” using progressive disclosure to keep context clean and performance high.`

### 🌍 The Problem: Modern Agents Are Overloaded
**AI agents today aren’t just chatbots — they are complex reasoners**

##### They Can:
- read/write files , call external tools , run code , interact with MCP servers , orchestrate workflows

##### But as agents became more capable, developers started loading them with:
- entire codebases, hundreds of tools , long procedural instructions , domain‑specific workflows

**This leads to Context Saturation — the agent’s context window gets stuffed with 40–50k tokens of irrelevant tools and instructions.**

### Symptoms of Context Saturation
- High latency , Higher cost , “Tool bloat” , “Context rot” → the model becomes confused by irrelevant information
- Even with huge context windows, dumping everything into memory hurts performance.

## 💡 The Solution: Agent Skills
**Anthropic introduced Agent Skills to fix this architectural problem: `monolithic context loading` to `Progressive Disclosure`**

### why Progressive Disclosure Model?
**It drastically reduced the initial token load compared to treditional context loading . By loading only the light weight metadata, it improves, latency, cost and performance.**

##### Instead of loading everything into the agent’s brain at startup, Skills allow:
 - modular packaging of workflows
 - on‑demand loading of instructions
 - progressive disclosure of complexity
 - clean, minimal context

#### A Skill is a self‑contained capability pack that includes:
- instructions , workflows , scripts , templates , domain knowledge
- **But the agent does not load the heavy content until it is needed.**

## ⚙️ How It Works (Progressive Disclosure)
#### At the start of a session, the model sees only a lightweight menu of metadata:
- Skill names , Short descriptions

#### When the user’s intent matches a Skill:
**The agent loads:**
- the full SKILL.md , scripts , workflows , examples , references
This is the heavy procedural knowledge — but it loads only when needed.


### Example
**If the user says:** “Refactor the authentication middleware.”

#### The agent loads:
- Security Skill, Auth Skill, Code Refactoring Skill

#### But it does NOT load:
- CSS pipeline tools, Database migration scripts , Frontend build tools

### This keeps the context:
- lean, fast, accurate, cost‑efficient

## 🧠 Why This Matters
**Skills solve the biggest pain points in agent design:**

#### 1. No more monolithic prompts
Agents don’t need 50k tokens of instructions at startup.

#### 2. No more tool bloat
Only relevant tools load.

#### 3. No more context rot
Irrelevant instructions never enter the context window.

#### 4. Faster, cheaper, more accurate agents
Because the agent’s working memory stays clean.

------------------------------------------------

# 3. Agent Skills and Antigravity

**In the Antigravity ecosystem, the Skills act as specialized training modules that bridge the gap between the generalist models and your specific context.**

- They allow the agent to temporarily “equip” specialized knowledge — like security audits, database migrations, or code review standards — only when the user’s request requires it.
- This transforms the agent from a generic assistant into a context‑aware specialist that rigorously adheres to an organization's codified best practices and safety standards.

## 🧠 What Is a Skill in Antigravity?
#### In Antigravity, a Skill is:
- A directory‑based capability package containing a `SKILL.md` file plus optional scripts, templates, and references.

#### It is the fundamental unit of on‑demand capability extension.
#### A Skill includes:
Code
my_skill/
 ├── SKILL.md          # Required: instructions, workflows, rules
 ├── scripts/          # Optional: Python/Bash tools the agent can run
 ├── references/       # Optional: docs, specs, examples
 └── assets/           # Optional: images, templates

## Why Skills Matter in Antigravity
##### Skills solve two major problems:

### 1. On‑Demand Loading (Progressive Disclosure)
**Unlike a system prompt — which is always loaded — a Skill is only activated when the agent detects that the user’s intent matches the Skill’s purpose.**

##### This means:
- No unnecessary instructions in context
- No irrelevant tools loaded
- No cognitive overload for the model
- Faster, cheaper, more accurate reasoning

### 2. Capability Extension
**Skills can execute, not just instruct.**

#### By bundling scripts, a Skill can:
- run migrations
- generate changelogs
- scaffold tools
- validate schemas
- perform multi-step workflows
This turns the agent into a tool‑using operator, not just a text generator.

## 🛠 Skills vs. Tools vs. Rules vs. Workflows
**Antigravity Agents have multiple capability layers.**

### Tools (MCP Servers) - Agent’s hands
- Provide persistent, stateful access to external systems 
#### Examples: GitHub MCP, PostgreSQL MCP, Filesystem MCP

### 🧠 Skills - agent’s brain
- Contain the methodology for how to use tools
- Lightweight, ephemeral, loaded only when needed

This serverless approach allows agents to execute ad-hoc tasks (like generating changelogs or migrations) without the operational overhead of running persistent processes, loading the context only when the task is active and releasing it immediately after.

### Rules : Global constraints

#### Example: “Always use Safe-Migration Skill for DB changes.”

### Workflows : Orchestrate multiple Skills

#### Example: “Build → Test → Migrate → Deploy” pipeline

### How They Work Together
- Tools provide capabilities
- Skills provide procedures
- Rules enforce safety
- Workflows orchestrate everything
This modularity is what makes Antigravity powerful.

### How Skills Are Triggered
Skills are agent-triggered, not user-triggered.

#### The model:
- Reads the user’s request
- Matches it against Skill metadata
- Loads the relevant Skill(s)
- Executes instructions and scripts
- Unloads them when done
This is dynamic specialization — the agent becomes an expert only when needed.

##🔗 Example
#### User says:

    “Generate a database migration for the new Orders table.”

#### Antigravity automatically loads:
- Safe-Migration Skill
- SQL Standards Skill
- Schema Validation Skill

#### But it does not load:
- CSS pipeline Skill
- Frontend template generator
- API documentation Skill
This keeps the context clean and the reasoning sharp.


--------------------------------------------------------------------------

# 🌟4. Creating Skills

## Overview
**Creating a Skill in Antigravity follows a simple, standardized directory structure. This ensures:**

- Skills are portable
- Agents can reliably parse and execute them
- Developers can easily extend Antigravity with new capabilities
The design intentionally uses Markdown + YAML, making Skills accessible to any developer — no special frameworks required.

## 📂 Skill Directory Structure
**A Skill is just a folder with a predictable layout:**

```
my-skill/
├── SKILL.md          # Required: the definition file
├── scripts/          # Optional: Python, Bash, Node scripts
│    ├── run.py
│    └── util.sh
├── references/       # Optional: docs, templates, specs
│    └── api-docs.md
└── assets/           # Optional: images, logos, static files
```

### Why this structure matters

- SKILL.md = instructions + workflows
- scripts/ = executable logic
- references/ = knowledge base
- assets/ = supporting visuals

##### This separation mirrors good software engineering practices: 
- instructions, logic, and knowledge are cleanly separated.

### 🧠 The SKILL.md File (The Brain of the Skill)
**SKILL.md is the most important part of the Skill.**

#### It tells the agent:
- What the Skill is
- When to use it
- How to execute it
- What constraints to follow

#### It has two parts:
- YAML Frontmatter `(metadata)`
- Markdown Body `(instructions)`

## 1️⃣ YAML Frontmatter (Metadata Layer)
**This is the only part indexed by Antigravity’s high‑level router.**

- When a user sends a prompt, the agent semantic-matches the prompt against the description fields of all available skills.

#### Example:

##### yaml
```
---
name: database-inspector
description: Use this skill when the user asks to query the database, check table schemas, or inspect user data in the local PostgreSQL instance.
---
```
### Key Fields

<img src=".././Images/skills_yaml_frontmatter.png" width="600" height="300">

#### Important Notes
**name** : 
- Not mandatory. Must be unique within the scope should be lowercase, hyphenated (postgres-query, pr-reviewer).
-  If it's not provided, it will default to the directory name.

**description:**
- This is mandatory and the most important field
- description must be precise and semantic, not vague(functions as the "trigger phrase.")

#### Description Example:

❌ “Database tools”

✔ “Executes read-only SQL queries against the local PostgreSQL database to retrieve user or transaction data.”

- A good description ensures the Skill is activated only when relevant.

## 2️⃣ Markdown Body (Instructions Layer)
**Main instructions like prompt engineering" persisted to a file.**

- This is the content injected into the agent’s context when the Skill is activated.

#### It should include:

##### ✔ Goal
A clear statement of what the Skill accomplishes.

##### ✔ Instructions
Step-by-step logic the agent must follow.

##### ✔ Examples
Few-shot examples of inputs and outputs to guide the model's performance. to guide the model’s behavior.

##### ✔ Constraints
Rules the agent must not violate. E.g. "Do not" rules (e.g., "Do not run DELETE queries").

## Example SKILL.md Body
Code
```
Database Inspector

Goal
To safely query the local database and provide insights on the current data state.

Instructions
- Analyze the user's natural language request to understand the data need.
- Formulate a valid SQL query.
  - CRITICAL: Only SELECT statements are allowed.
- Use the script scripts/query_runner.py to execute the SQL.
  - Command: python scripts/query_runner.py "SELECT * FROM..."
- Present the results in a Markdown table.

Constraints
- Never output raw user passwords or API keys.
- If the query returns > 50 rows, summarize the data instead of listing it all.
```
**This is prompt engineering stored on disk — reusable, versionable, and loadable on demand.**

## Script Integration (Optional but Powerful)
**You can include xecutable scripts inside the `scripts/ directory.`**

### Why this matters:
- This allows the agent to perform actions that are difficult or impossible for an LLM to do directly

### Like:
- LLMs cannot run binaries ,  complex mathematical calculation or complex logic directly
- Scripts allow the agent to perform real actions like  interacting with legacy systems
- Skills become tool-using modules, not just text instructions

### How scripts are used
- The `SKILL.md` references them by relative path
- The agent calls them when needed
- Scripts can be Python, Bash, Node, etc.

---------------------------------------------------------------------------------

 # 4. Creating or Authoring Skills

## 🎯 Goal of This Section
**To learn how to build out Skills that integrate into Antigravity, progressively introducing features like:**
- resources
- scripts
- examples
- procedural logic

Your document states this directly:

“The goal of this section is to build out Skills that integrate into Antigravity and progressively show various features like resources / scripts / etc.”

## 📦 Skill Installation & Configuration
- go to [Skills](https://github.com/rominirani/antigravity-skills).
- Git clone - repository
- Copy the desired folders from `skills_tutorial/` into your workspace's `.agent/skills/` directory, or into your global `~/.gemini/antigravity/skills/` directory.
- Restart your agent session.

## Antigravity supports two scopes for Skills:

### 1. Global Scope : `~/.gemini/config/skills/  `
- Available across all Antigravity products and all projects.
- suitable for general utilities like ‘Format JSON’ or ‘Generate UUIDs’.”

### 2. Project Scope : `<project-root>/.agents/skills/  `
- Only available inside a specific project.
- ideal for project-specific scripts, such as deployment to a specific environment, database management for that app, or generating boilerplate code for a proprietary framework.

## Workflow:

### Installing the Skills in either Antigravity or Antigravity CLI

#### Copy the four tutorial Skills
- Copy the following 4 folders: git-commit-formatter, license-header-adder, database-schema-validator, json-to-pydantic.

#### Place them in the correct scope
**For Antigravity or Antigravity CLI:**
```
<project-root>/.agents/skills/
```
- create a folders `my_skills_project/.agents/skills` in a desired location
-  place the copiedskills in your project's skills folder
- these skills are only available to your project on Antigravity/CLI

## Validate
- Once installed, open `Antigaravity/project folder`. you can ask:
```
“What skills are available?”
and Antigravity will list them.
```
<img src=".././Images/skill_installation.png" width="400" height="600">


### Antigravity CLI:
- Antigravity CLI, you can give the following command `/skills` and it should list the 4 skills

---------------------------------------

## Skill Directory Structure
**Canonical structure:**
```
my-skill/
├── SKILL.md
├── scripts/
│    ├── run.py
│    └── util.sh
├── references/
│    └── api-docs.md
└── assets/
```
**This structure separates concerns effectively… mirroring standard software engineering practices.**

## Understanding the Four Skill Patterns in Antigravity
**Let's go into each of the Skills and understand how they were constructed**.
- We could use these templates to create your own skills too.
- Lets' walk through `four progressively more advanced Skill patterns`. 
    - Each pattern teaches a different capability of Antigravity Skills 
    — from simple routing to script execution.

## Level 1 : The Basic Router ( git-commit-formatter )

#### Pattern 1: Instruction‑Only Skill
This is the `“Hello World”` of Skills — a Skill that contains only a `SKILL.md` and **'no scripts, references, or assets.'**

### What this Skill does
##### It enforces the Conventional Commits format by giving the agent:

    - allowed commit types
    - the commit message structure
    - step‑by‑step instructions
    - an example
Because the `SKILL.md` contains all logic, the agent can **format commit messages** without any external files.

#### Why this matters
**This demonstrates the simplest Skill pattern:**
- ✔ No scripts
- ✔ No assets
- ✔ No references
- ✔ Pure instruction routing
The agent loads this Skill only when the user asks to write or format a commit message.

## Example: How to Run This Example in Antigravity

###  Step 1: Set Up a Test Git Repository
- Make sure you have git available on your local machine 
- Launch Antigravity(CLI)
- Open your workspace folder
- Prompt
```
Create a folder named git_test in the workspace, initialize a git repository inside it, and create an initial file auth.py with def login(): pass. Stage this file and make an initial commit.
```
### Validate
- The agent will create the directory, initialize the repository, stage the file, and commit it with a message like "initial commit".

<img src=".././Images/git_skills1.png" width="400" height="500">

### Step 2: Make a Code Change
- Tell the agent to modify the code so there is a change to commit.
- Prompt
```
In the git_test folder, modify auth.py to add Google Login functionality.
```
### Validate
- The agent will edit the file to add a new feature, preparing it for the commit phase.

<img src=".././Images/git_skills2.png" width="400" height="500">

### Step 3: Stage and Commit the Changes
- Trigger the `git-commit-formatter` skill by asking the agent to stage the changes and create a commit.
- Prompt
```
Stage the changes in the git_test folder and commit them. Make sure to format the commit message using the Conventional Commits skill.
```

### Validate
- The agent will run git add `auth.py`, analyze the `diff` to determine that a new feature was added to the auth module, and formulate a conventional commit message like `feat(auth): implement google login` before running git commit.

<img src=".././Images/git_skills3.png" width="400" height="500">

### Step 4: Verify the Git Log
- Ask the agent to retrieve the `git history` so you can confirm that the formatted commit was successfully recorded.
- Prompt
```
Show me the git log in the git_test folder.
```

### Validate
- The agent will run `git log -n 5` and return the output showing the formatted commit message.

<img src=".././Images/git_skills4.png" width="500" height="300">
----------------------

## Level 2 — Asset Utilization (license‑header‑adder)

### Pattern: Reference‑Based Skill

##### Every source file in a 'corporate project' might need a specific 20-line `Apache 2.0 license header`. Putting this static text directly into the `prompt (or SKILL.md)` is wasteful. It consumes `tokens` every time the skill is indexed, and the model might `"hallucinate"` typos in legal text. It is a `good practice` to offload the static text to a `plain text file` in a `resources/ folder`. 
- The skill instructs the agent to read this file only when needed.

**This level introduces external resources — specifically, a static license header stored in a file.**

## What this Skill does
- It adds a license header to new source files by:
- Reading a template from resources/HEADER_TEMPLATE.txt
- Converting comment syntax depending on language
- Prepending the header to the file

## Why this matters
**This pattern teaches:**
- ✔ How to store large, static text outside SKILL.md
- ✔ How to reduce token usage
- ✔ How to avoid hallucinations in legal text
- ✔ How to instruct the agent to read files only when needed

## Example : How to Run This Example in Antigravity
**Assuming that you have launched Antigravity or Antigravity CLI, follow these steps:**

### Step 1: Create the Python File with Sample Code
 - Prompt
 ```
 Create a new file my_script.py with the following python code:

def hello():
   print("Hello, World!")
```
### Validate
- The agent invoked a file-writing tool **(write_to_file)** to create a new file named `my_script.py` directly in your active **workspace directory(my_skills_project)** and wrote the basic Python function to it.


### Step 2: Add the License Header
- Prompt:
```
Add the license header to my_script.py.
```

### Validate
- prompt triggered the `license-header-adder skill`. The agent located and read the license template file **(HEADER_TEMPLATE.txt)**, modified the comment style from **C-style block comments (/* ... */) to Python-style comments (#)**, and prepended it to the top of the file using the **replace_file_content** tool.

<img src=".././Images/licence_skill.png" width="500" height="300">

- Take a look at the `my_script.py` file. It will contain the **license header** at the top.

<img src=".././Images/licence_skill2.png" width="500" height="400">

----------------------------

## Level 3 — Learning by Example (json‑to‑pydantic)

### Pattern: Few‑Shot Example Skill:

Since we know **“LLMs are pattern‑matching engines.”**, Authoring your skill with a golden example **(Input -> Output)** is often more effective than verbose instructions.

### What this Skill does
**It converts JSON into Pydantic models by:**
- inferring types
- generating nested classes
- following naming conventions
- using examples in /examples

### Why this matters
- ✔ How to use before/after examples
- ✔ How to guide the agent through pattern matching
- ✔ How to avoid writing 50+ rules manually

### The Skill includes:

- examples/input_data.json
- examples/output_model.py
The agent uses these as a template to generate new models.

### Understand the files : 
- Go to the json-to-pydantic/folder that contains the skill files, as shown below:

```
- json-to-pydantic/
├── SKILL.md
└── examples/
   ├── input_data.json   (The Before State)
   └── output_model.py   (The After State)
```

- check `skills.md` file:

```
---
name: json-to-pydantic
description: Converts JSON data snippets into Python Pydantic data models.
---

# JSON to Pydantic Skill

This skill helps convert raw JSON data or API responses into structured, strongly-typed Python classes using Pydantic.

Instructions

1. **Analyze the Input**: Look at the JSON object provided by the user.
2. **Infer Types**:
  - `string` -> `str`
  - `number` -> `int` or `float`
  - `boolean` -> `bool`
  - `array` -> `List[Type]`
  - `null` -> `Optional[Type]`
  - Nested Objects -> Create a separate sub-class.
 
3. **Follow the Example**:
  Review `examples/` to see how to structure the output code. notice how nested dictionaries like `preferences` are extracted into their own class.
 
  - Input: `examples/input_data.json`
  - Output: `examples/output_model.py`

Style Guidelines
- Use `PascalCase` for class names.
- Use type hints (`List`, `Optional`) from `typing` module.
- If a field can be missing or null, default it to `None`.
```

- check /examples folder for input **JSON file** and the output i.e. **Python file.**

#### input_data.json
```
{
   "user_id": 12345,
   "username": "jdoe_88",
   "is_active": true,
   "preferences": {
       "theme": "dark",
       "notifications": [
           "email",
           "push"
       ]
   },
   "last_login": "2024-03-15T10:30:00Z",
   "meta_tags": null
}
```
#### output_model.py
```
from pydantic import BaseModel, Field
from typing import List, Optional

class Preferences(BaseModel):
   theme: str
   notifications: List[str]

class User(BaseModel):
   user_id: int
   username: str
   is_active: bool
   preferences: Preferences
   last_login: Optional[str] = None
   meta_tags: Optional[List[str]] = None
```

## How to Run This Example in Antigravity
**Assuming that you have launched Antigravity or Antigravity CLI, follow these steps:**

### Step 1: Create the JSON File with Sample Data
- Ask the agent to create a new file `product.json` containing the **raw JSON payload**.
- Prompt:
```
Create a new file product.json with the following JSON:

{
 "product": "Widget",
 "cost": 10.99,
 "stock": null
}
```
<img src=".././Images/input_skills1.png" width="500" height="300">

### Step 2: Convert the JSON to a Pydantic Model
**Trigger the json-to-pydantic skill to convert the JSON data into a structured Pydantic class.**
- Prompt:

```
Convert the JSON in product.json to a Pydantic model and save it to product_model.py.
```

<img src=".././Images/output_skills.png" width="500" height="500">

### Step 3: Verify the Output
- Take a look at the `product_model.py` file. It will contain the completed **Pydantic model.**

<img src=".././Images/pydantic_skills.png" width="300" height="300">

------------------

## Level 4 — Procedural Logic (database‑schema‑validator)

### Pattern: Tool_Use - Script‑Driven Skill
**This is the most advanced pattern — using a Python script to perform deterministic validation.**

### What this Skill does
**It validates `SQL schema files` using a Python script that checks:**

- No DROP TABLE
- Table names must be snake_case
- Every table must have an id primary key

### Why this matters
**This pattern teaches:**
- ✔ How to integrate scripts
- ✔ How to run commands
- ✔ How to interpret exit codes
- ✔ How to offload complex logic to deterministic code

### usecase: If you ask an LLM "Is this schema safe?", it might say all is well, even if a critical primary key is missing, simply because the SQL looks correct.

**Fix:** Delegate this check to a **deterministic Script.** Our database-schema-validator skill will route the agent to run a **Python script** that we wrote. The script provides **binary (True/False) truth.**

### Understand the skill
- Check out `skills.md`
```
---
name: database-schema-validator
description: Validates SQL schema files for compliance with internal safety and naming policies.
---

# Database Schema Validator Skill

This skill ensures that all SQL files provided by the user comply with our strict database standards.

Policies Enforced
1. **Safety**: No `DROP TABLE` statements.
2. **Naming**: All tables must use `snake_case`.
3. **Structure**: Every table must have an `id` column as PRIMARY KEY.

Instructions

1. **Do not read the file manually** to check for errors. The rules are complex and easily missed by eye.
2. **Run the Validation Script**:
  Use the `run_command` tool to execute the python script provided in the `scripts/` folder against the user's file.
 
  `python scripts/validate_schema.py <path_to_user_file>`

3. **Interpret Output**:
  - If the script returns **exit code 0**: Tell the user the schema looks good.
  - If the script returns **exit code 1**: Report the specific error messages printed by the script to the user and suggest fixes.

```

- Check out the `validate_schema.py` file is shown below:
```
import sys
import re

def validate_schema(filename):
   """
   Validates a SQL schema file against internal policy:
   1. Table names must be snake_case.
   2. Every table must have a primary key named 'id'.
   3. No 'DROP TABLE' statements allowed (safety).
   """
   try:
       with open(filename, 'r') as f:
           content = f.read()
          
       lines = content.split('\n')
       errors = []
      
       # Check 1: No DROP TABLE
       if re.search(r'DROP TABLE', content, re.IGNORECASE):
           errors.append("ERROR: 'DROP TABLE' statements are forbidden.")
          
       # Check 2 & 3: CREATE TABLE checks
       table_defs = re.finditer(r'CREATE TABLE\s+(?P<name>\w+)\s*\((?P<body>.*?)\);', content, re.DOTALL | re.IGNORECASE)
      
       for match in table_defs:
           table_name = match.group('name')
           body = match.group('body')
          
           # Snake case check
           if not re.match(r'^[a-z][a-z0-9_]*$', table_name):
               errors.append(f"ERROR: Table '{table_name}' must be snake_case.")
              
           # Primary key check
           if not re.search(r'\bid\b.*PRIMARY KEY', body, re.IGNORECASE):
               errors.append(f"ERROR: Table '{table_name}' is missing a primary key named 'id'.")

       if errors:
           for err in errors:
               print(err)
           sys.exit(1)
       else:
           print("Schema validation passed.")
           sys.exit(0)
          
   except FileNotFoundError:
       print(f"Error: File '{filename}' not found.")
       sys.exit(1)

if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("Usage: python validate_schema.py <schema_file>")
       sys.exit(1)
      
   validate_schema(sys.argv[1])
```

## How to Run This Example in Antigravity
**Assuming that you have launched Antigravity or Antigravity CLI, follow these steps**

### Step 1: Create the JSON File with Sample Data
**Ask the agent to create a new file `bad_schema.sql` containing multiple policy violations.**

- Prompt:
```
Create a new file bad_schema.sql with the following SQL:

DROP TABLE IF EXISTS legacy_users;

CREATE TABLE userProfile (
    id INT PRIMARY KEY,
    bio TEXT
);

CREATE TABLE posts (
    title TEXT,
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE comments (
    id INT PRIMARY KEY,
    post_id INT,
    body TEXT
);

```
<img src=".././Images/schema_skill1.png" width="400" height="300">

#### Note: The above schema file violates all three policies: it uses a forbidden DROP TABLE statement, uses camelCase for the userProfile table name, and forgets the id primary key in the posts table.

### Step 2: Validate the SQL Schema
- Trigger the database-schema-validator skill to run the Python validator script against your file.
- prompt:

```
Validate bad_schema.sql using the database-schema-validator skill.
```

### Step 3: Verify the Output
**The agent will report the failure and display the specific errors found by the script directly in the chat.**
The sample output is shown below:

<img src=".././Images/schema_skill2.png" width="400" height="300">


----------------------------------------------------------------------------------

# 6. The Developer Toolkit (Agents CLI Skills)

## 🎯 Goal:
- To understand how Agents CLI Skills streamline the entire lifecycle of building, testing, and deploying AI agents — from scaffolding to local execution to cloud deployment.

## What You Will Learn
**In this section, you’ll learn:**
- What Agents CLI Skills are
- How they complement the Agent Development Kit (ADK)
- How to install them
- How to scaffold a new agent project
- How to run and test an agent locally
- How to launch the interactive playground

## 📖 Introduction
**Agents CLI Skills represent the Action & Lifecycle Pattern — Skills that automate the operational side of agent development.**

## Agent CLI Skills:
**Agent Cli  -Command Line Interface**

- The Agent CLI Skills bridge the gap between huge raw code and autonomous execution.
-  Agents CLI Skills packages this lifecycle expertise(forcing your coding assistant to guess directory structures or write boilerplate agent configuration) into specific agent skills.

## Agent Development Kit (ADK) VS Agent CLI Skills
#### ADK gives you:
- SDKs, APIs, structural blueprints

#### Agents CLI gives you:
- scaffolding , local execution, testing, deployment pipelines

**Together, they form a complete developer workflow.**

### Optional: Cloud Integration
**when mapped to Google Cloud, Agent CLI skills act as a direct pipeline to enterprise-grade infrastructure.**

#### When connected to Google Cloud, Agents CLI Skills can:
- you can use CLI commands to instantly package agent workflows
- manage IAM permissions
- deploy to Vertex AI or Cloud Run
- integrate with CI/CD pipelines

`This turns what used to be complex cloud architecture tasks into simple, reproducible terminal commands, making it much easier to integrate autonomous agents into existing CI/CD deployment pipelines.`

## 🛠 Installation

### Prerequisites
- Python 3.11+
- Node.js
- uv package manager : 👉 Open PowerShell (not Git Bash)

**Press Start → type “PowerShell” → Run as Administrator.**

#### Then run:
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### This will:
- download uv
- install it into your user profile
- add it to your PATH

#### Vslidate:
- Restart ALL terminals
- verify
```
uv --version
uvx --help
```
#### This prints: 
- version - uv 0.11.21 (5aa65dd7a 2026-06-11 x86_64-pc-windows-msvc)
- If it prints help text, you’re fully ready to install Agents CLI.

### Install Agents CLI
- Powershell
```
uvx google-agents-cli setup
```
#### This will install:
- agents-cli, the CLI Skills, the scaffolding tools

#### Note: The skills will be installed in the `~/.agents/skills` folder, which is visible to `Antigravity`. If you would like to see these skills in `Antigravity CLI,` you will have to move them to the `~/.gemini/antigravity-cli/skills` folder (global scope).

## Meaning:

### Antigravity (the GUI app)
- Automatically sees Skills in `~/.agents/skills`

### Antigravity CLI (the terminal version)
- Does NOT automatically see Skills in that folder.
- It only looks in: `~/.gemini/antigravity-cli/skills`

So if you installed Agents CLI Skills globally (which you did), they are currently in:`~/.agents/skills`

### Make Skills visible to Antigravity CLI
- Move them to:
```
~/.gemini/antigravity-cli/skills
```

### Then ask Antigravity:
- open Antigravity CLI - Type `agy' in git bash
- Ask :
```
“What skills are available”
```
You’ll see the newly installed CLI Skills.

--------------------------------------

# 🧭 Step-by-Step Walkthrough

## Step 1 — Scaffold and Initialize a New Agent Project
- Create a new agent project:
- open git bash in your desiredfolder
- type:
```
agents-cli create weather-assistant --prototype --yes
```

Move into the folder and install project dependencies:
```
cd weather-assistant
agents-cli install
```
### This gives you:
- a ready-to-run agent
- a standardized project layout
- dependency management
- a manifest for tracking agent metadata

## Step 2: Run a Local Test Query

#### Before running, export your Gemini API key:
```
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

#### Then test your agent:
```
agents-cli run "How are you?"
```

### What happens behind the scenes

#### The CLI:
- loads the ADK runtime in memory
- routes your prompt through local credentials
- streams the response directly to your terminal

## Step 3 — Launch the Interactive Web Playground

#### Start the local UI:
```
agents-cli playground
```

#### This opens a web interface at:
```
http://localhost:8080
or

http://127.0.0.1:8000
```

### What happens behind the scenes

#### The CLI:
- launches a local ADK web server
- enables hot‑reloading
- provides a visual chat interface
- lets you select your app and interact with it

## 🎓 Summary

### Agents CLI Skills give you:

- Scaffolding → create new agent projects instantly
- Local execution → run agents directly in your terminal
- Playground UI → interact visually with your agent
- Cloud-ready workflows → deploy to Google Cloud with ease
They automate the entire lifecycle so you can focus on building agent logic, not boilerplate.










