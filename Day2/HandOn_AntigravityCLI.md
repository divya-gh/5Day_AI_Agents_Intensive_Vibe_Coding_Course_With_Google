# Hands-on with Antigravity CLI

## What is Antigravity CLI ?

**It's a lightweight Terminal User Interface (TUI) surface of Antigravity.**

 It brings the same core agentic capabilities as Antigravity (such as multi-step reasoning, multi-file editing, tool calling, and conversation history) directly to your terminal.

 ## Goal: 
 1. Lear Installing and configuring Antigravity CLI
 2. Understanding basic usage of Antigravity CLI
 3. Exploring a few use cases with Antigravity CLI

 1. Prerequisites
- Antigravity CLI installed (from the official Antigravity site)
- Google Cloud project (same one you’re using for the course is fine)
- Git + GitHub repo (e.g. 5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google)

## Installation 

**Open windows powershell - irm https://antigravity.google/cli/install.ps1 | iex**

## Project Creation:
- Create a Home Folder for projects
- name it  'agy-cli-projects' or anything
- Git bash - `cd agy-cli-projects`
-  Verify CLI is installed ``` antigravity --help ```
- Check for Version ```$ agy --version  : 1.0.7 ```
- type : `agy` to open antigravity CLI
-  Google OAuth and press Enter  to authenticate
-  Say ' Yes, I trust this folder.'

**Congratulations! You are all set now!**


## first interaction with Antigravity CLI

- type your first query : `Give me a famous quote on Artificial Intelligence and who said that?`

## Help
- use 'antigravity --help'
- /help 
- agy --help

## exit
- /quit
- ctrl +d -twice

## 4. Antigravity CLI - a few housekeeping commands

### Configuration / Settings
- /config command : brings up various areas of Antigravity that you can customize based on your preferences
    - Color Scheme, 
    - Tool permission, 
    - telemetry settings and more.

<img src=".././Images/CLI_config.png" width="350" height="450">

- settings.json : All of the configuration settings get stored in ~/.gemini/antigravity-cli/settings.json file

<img src=".././Images/CLI_setting_json.png" width="350" height="450">

### Tool Permission
- /config: Shows Tool Permission : whether terminal commands require your approval before running.
- Provides :
    - security: guarding your host system against unintended changes
    - Velocity: how autonomously the agent can work without pausing for your input

### request-review 
- agent checks in before performing any action that could affect your system or project files outside of pre-approved bounds.
- Mainly for a terminal command, perform a file operation (like writing/deleting), or call an external service.
- The user is prompted to approve or reject the specific action.

### proceed-in-sandbox
- Allows the agent to execute terminal commands automatically, but within a secure, isolated container.
- Commands are executed in a virtualized sandbox (e.g., a lightweight container).
- Agent cannot modify your actual host machine's filesystem or access your local network.

### always-proceed
- fully autonomous mode: Full permission to agent.
- Giving the agent maximum speed and capability to run commands and write files directly on your host machine
- No permission taken /Agent will never prompt you for confirmation

### strict
- zero-trust, high-security mode.
- agent's capabilities are restricted to executing read tools
-  All non-read tools will require the user to be prompted for action.

## 5. Antigravity CLI - Command Parameters

### Non-interactive mode (autonomous)
- User prompts nad agent responds without interactive  terminal opening up.
- useful in full automation

##### `agy -p` :  provide the prompt to Antigravity CLI 

### Choose a specific model
- Use `--model` parameter to tell Antigravity CLI to use a specific model during current the session.
```
$ agy --model "Gemini 3.5 Flash (Low)"

```
### dangerously-skip-permission
- use `--dangerously-skip-permissions` : to auto approve all tool permissions
- no permissions asked. Use with care!
```
agy --dangerously-skip-permissions
```

## 6. Antigravity CLI - Shell mode
**Working with the Shell from within Antigravity CLI**

- use `!` in the message box : will toggle to a Shell mode.
- `!` or `esc` to exit

### Other commands
- use `pwd` , `ls`, `mkdir` like on gitbash



