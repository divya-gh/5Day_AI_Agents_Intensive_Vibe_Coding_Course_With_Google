# 🚀 Integrating Google Developer Knowledge MCP with Antigravity 2.0 (IDE & CLI)

## 🎯 Goal: 
- Integrate Google Developer Knowledge into Antigravity, IDE or CLI call via APIs and MCP so that developers can integrate it into applications and workflows.

- Learn :  how to install and use the Developer Knowledge MCP from Antigravity 2.0, IDE, and/or CLI

## What is Google Developer Knowledge (GDK?

** GDK is 'the canonical, machine-readable source of Google's public developer documentation'.**
- provides programmatic access to Google's public developer documentation, enabling you to integrate this knowledge base into your own applications and workflows.
- Instead of relying on outdated LLM training data or manual web scraping, AI agent developers should use it for real-time access to the most accurate documentation and reduce risk of hallucinations.

### Benefits

✅ Access real-time documentation
✅ Reduce AI hallucinations
✅ Eliminate manual web scraping
✅ Avoid relying on outdated LLM training data
✅ Build more reliable AI developer assistants

## 📋Prerequisites

Before starting, ensure you have:

#### 1. Web Browser
* Chrome (recommended)
* Any modern browser

##### Used for:
* Google Cloud Console
* Codelab walkthroughs

#### 2. Google Cloud Project

##### Use either:
* A new Google Cloud project
* An existing project
Billing is not required for this codelab scenario.

#### 3. Antigravity Installed

##### Install one or both:
* Antigravity IDE
* Antigravity CLI
If you're currently using Gemini CLI, migrate to Antigravity CLI as described in Google's transition documentation.

---------------------------------------------------------------------------------------------------------------------------
Setting
---------------------------------------------------------------------------------------------------------------------------

### 🔧 Step 1 – Enable the Developer Knowledge API

#### In your Google Cloud project:
- Open Google Cloud Console.
- Select the project you’ll use for this codelab.
- Go to APIs & Services → Library.
- Search for:
     “Google Developer Knowledge API” (or similar name as shown in the codelab).

- Click the API → Enable.
After this, your project is allowed to call the Developer Knowledge backend that the MCP server will use.

## 🔑 Step 2 – Configure Antigravity to use the Developer Knowledge MCP
You’ll now “plug in” the MCP server into Antigravity. 

**Antigravity 2.0, IDE, and CLI share a central MCP configuration in the file ~/.gemini/config/mcp_config.json.**

#### Create the API key to use the Developer Knowledge MCP server

**In the Google Cloud Console, do the following:**

1. Go to APIs & Services > Credentials.
2. Click + Create credentials, then select API key from the menu.
3. Set Name with an arbitrary name such as Antigravity.
4. Click the Select API restrictions drop-down, type Developer Knowledge API, check the result, then click OK.

### 🔧 Configure Antigravity IDE

### Step 1:

- Open Antigravity IDE, click on the dropdown at the top of the editor's agent panel.
- Click Manage MCP Servers then View raw config.
- Modify it with the following custom MCP server configuration. 
- Before doing so, replace the <YOUR_API_KEY> placeholder with the API key you created in the previous steps:
```
{
  "mcpServers": {
    "google-developer-knowledge": {
      "headers": {
        "X-Goog-Api-Key": "<YOUR_API_KEY>"
      },
      "serverUrl": "https://developerknowledge.googleapis.com/mcp"
    }
    
  }
  
}
```
-------------------------------------------
### 🧪 Step 2: Validate ANtigravity IDE
- Open Antigravity User Settings via the Editor-Specific settings menu dropdown at the top of the window.
- Navigate to Customizations.
- Under Installed MCP Servers, click Refresh.
- Check for Google-developer-Knowledge MCP server installed.

### 🔧 Configure ANtigravity 2.0 and Validate
- Go to Settings / Customizations / Under Installed MCP Servers, click Refresh.
- Check for Google-developer-Knowledge MCP server installed.

### 🧪 Validate Antigravity CLI
1. Open Git Bash
2. Start the CLI executing the command `agy` from the terminal.
3. Type /mcp and press enter.


## ⚙️ Step 3 –Test the integration with prompts

#### In Antigravity IDE or CLI:
- Start a conversation in your project (Agent Panel in IDE, or antigravity chat in CLI).
- Ask something that clearly targets Google dev docs, for example:

**“Using the Developer Knowledge MCP, find the latest docs for Cloud Run deployment with Node.js and summarize key steps.”**

**“From Google Developer Knowledge, show me the official docs for using Vertex AI with Python.”**


### 🖥️ Watch for:
- The agent calling the MCP tool (you may see a “tool call” or “MCP call” in the UI).
- Responses that quote or reference official docs, not just generic LLM text.

#### 💡Variations to try:
- Ask for API reference.
- Ask for quickstart guides.
- Ask for code samples.
If it’s wired correctly, the agent will keep pulling from Google Developer Knowledge, not from stale training data.

## Example: 
### 1. Antigravity 2.0
<img src=".././Images/antigravity_mcp_test2.png" width="700" height="800">

### 1. Antigravity CLI
<img src=".././Images/mcp_test1.png" width="700" height="800">

### 📚 Why This Matters

**Without Google Developer Knowledge MCP:**

    LLM → Static Training Data

#### 🤖 Potential issues:
* ❌ Outdated documentation
* ❌ Hallucinated APIs
* ❌ Missing recent releases

#### With Google Developer Knowledge MCP:
```
LLM
  ↓
Google Developer Knowledge MCP
  ↓
Official Google Documentation
```

#### 🌈 Benefits:
* More accurate answers
* Current documentation
* Lower hallucination risk
* Better developer productivity


Citation:
