# Manager Dashboard Service Walkthrough

I have implemented, deployed, and successfully verified the standalone FastAPI-based Manager Dashboard service.

## Implemented Components

1. **[pyproject.toml](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/pyproject.toml)**: Defines the backend dependencies (`fastapi`, `uvicorn`, `google-adk`, `google-cloud-aiplatform`).
2. **[Dockerfile](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/Dockerfile)**: Standardizes build steps and container environment for Cloud Run execution.
3. **[main.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/main.py)**:
   - **`GET /`**: Renders a premium, glassmorphism dark-mode UI displaying all pending expense approval cards retrieved from the agent.
   - **`GET /api/pending`**: Interfaces with the `VertexAiSessionService` of the ADK library to query active sessions, parses events, detects unresolved manual approvals, and returns details.
   - **`POST /api/action/{session_id}`**: Submits a structured function response to resume the human-in-the-loop workflow.

## Cloud Run Deployment

The service has been successfully built and deployed to Cloud Run.

* **Dashboard URL**: `https://expense-manager-dashboard-255574108149.us-east1.run.app`
* **Runtime Service Account**: `255574108149-compute@developer.gserviceaccount.com`
* **IAM Configuration**: Granted `roles/aiplatform.user` to the service account on project `divya-doc-pipeline`.
