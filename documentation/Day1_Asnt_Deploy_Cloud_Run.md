# 🚀 Deploy from AI Studio to Cloud Run
    ##### A step‑by‑step guide for building, testing, and deploying a Vibe‑coded web app

## 📌 Overview

#### Modern AI development often starts with a simple question:

    “Can I quickly prototype the idea in my head?”

**Google AI Studio is built exactly for that — a rapid prototyping environment where you can build small apps using Vibe Coding, test them instantly, and deploy them to production using Cloud Run.**

### This guide walks you through:
- Building a simple web application in AI Studio
- Testing it locally
- Deploying it to Cloud Run
- Cleaning up resources afterward

##### Source: Google Codelab — Deploy from AI Studio to Cloud Run 

#### Prerequisites

##### Before starting, make sure you have:
- A basic understanding of web applications
- A Google Cloud account
- A modern browser (Chrome, Firefox, etc.)

### 🧪 What You’ll Learn

##### By the end of this guide, you will be able to:
- Build a simple web app using Vibe Coding in AI Studio
- Test your app directly inside AI Studio
- Deploy your app to Cloud Run with minimal setup

🖥️ 1. Build

### 1. Build Your App in AI Studio
- Open Google AI Studio
- Start a new Vibe Coding session
- Describe the app you want to build
- Let AI Studio generate the initial code
- Iterate using natural‑language prompts
- Once ready, export the generated project files

Tip: Keep your app simple — a single‑page UI or small API is perfect for Cloud Run.

### 2. Test the Application

#### Inside AI Studio:
- Use the Preview panel to run your app
- Validate UI behavior
- Test API endpoints
- Fix any errors using conversational prompts

#### Once everything works:
- Download the project
- Or sync it to your local environment

#### 3. Deploy to Cloud Run
Cloud Run lets you deploy containerized apps without managing servers.

#### Steps:
- Install the Google Cloud CLI
- Authenticate:
bash
```
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

- Build and deploy:

bash
```
gcloud run deploy my-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

- Wait for Cloud Run to build and deploy your container
- Copy the generated service URL
- Open it in your browser — your app is live 🎉

#### 4. Clean Up

**To avoid charges:**

bash
```
gcloud run services delete my-app
```
Or delete the entire project if it was created only for testing.

### Congratulations
**We have now:**
 - Built an app using Vibe Coding
- Tested it in AI Studio
- Deployed it to Cloud Run
- Learned the full prototype → production workflow
This is the foundation for building more advanced AI‑powered applications.

--------------------------------------------------

# 7. Installing Agent Skills using npx skills

### If you installed skills using:
```
npx skills add <something>
```
They are now located here:
```
~/.agents/skills
```
To make Antigravity CLI see them, copy them to:

```
~/.gemini/antigravity-cli/skills/

```

### Project Scope: Located in <project-root>/.agent/skills/.
### Global Scope: Located in ~/.gemini/antigravity-cli/skills/.