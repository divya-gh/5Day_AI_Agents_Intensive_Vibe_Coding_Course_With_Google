# Implementation Plan: Standalone Manager Dashboard Service

Create a FastAPI-based Manager Dashboard service inside the `submission_frontend/` folder. This service will retrieve pending expenses from Agent Runtime sessions using `VertexAiSessionService`, allow interactive manual approvals/rejections, and visually present the agent's review and status.

## Proposed Changes

### [New Component] submission_frontend

Creation of the manager dashboard service directory structure:

#### [NEW] [pyproject.toml](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/pyproject.toml)
Defines project dependencies: `fastapi`, `uvicorn`, `google-adk`, `google-cloud-aiplatform`, `jinja2` (for templates), and `python-dotenv`.

#### [NEW] [main.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/main.py)
Implements:
1. **FastAPI Initialization**: Configures CORS, loads env variables (`GOOGLE_CLOUD_PROJECT` and `AGENT_RUNTIME_ID`).
2. **Endpoints**:
   - `GET /`: Serves a sleek, interactive glassmorphic dashboard HTML page with dark mode, glowing accents, Outfit font, and animated transitions.
   - `GET /api/pending`:
     - Initializes `VertexAiSessionService`.
     - Lists all sessions using `list_sessions`.
     - Fetches full history for each session using `get_session`.
     - Scans for unresolved `adk_request_input` function calls (meaning a function call was found with name `adk_request_input`, but no matching response part exists later in the event log).
     - Returns session details, interrupt ID, and expense state (from `session.state.get("expense")`).
   - `POST /api/action/{session_id}`:
     - Receives `approved` (Boolean) and `interrupt_id` (String).
     - Initializes `ReasoningEngine` using `vertexai.agent_engines.get(...)`.
     - Submits a custom resume message structured as:
       ```python
       resume_message = {
           "role": "user",
           "parts": [
               {
                   "function_response": {
                       "id": interrupt_id,
                       "name": "adk_request_input",
                       "response": {
                           "approved": approved,
                           "response": "yes" if approved else "no"
                       }
                   }
               }
           ]
       }
       ```
     - Sets `user_id` to `"default-user"` strictly to avoid session ownership issues.
     - Runs the stream and captures the final compliance evaluation event to return it to the dashboard.

## Verification Plan

### Automated Tests
- We will run the FastAPI service locally using `uv run uvicorn main:app --port 8000` and query the endpoints.

### Manual Verification
- View the dashboard at `http://127.0.0.1:8000` and visually inspect the pending expenses.
- Perform a manual approval/rejection and confirm it resumes and finishes the Agent Runtime session.
