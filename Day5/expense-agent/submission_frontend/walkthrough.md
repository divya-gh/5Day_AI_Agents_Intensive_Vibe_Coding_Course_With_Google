# Manager Dashboard Service Walkthrough

I have implemented and successfully verified the standalone FastAPI-based Manager Dashboard service.

## Implemented Components

1. **[pyproject.toml](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/pyproject.toml)**: Defines the backend dependencies (`fastapi`, `uvicorn`, `google-adk`, `google-cloud-aiplatform`).
2. **[main.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day5/expense-agent/submission_frontend/main.py)**:
   - **`GET /`**: Renders a premium, glassmorphism dark-mode UI displaying all pending expense approval cards retrieved from the agent.
   - **`GET /api/pending`**: Interfaces with the `VertexAiSessionService` of the ADK library to query active sessions, parses events, detects unresolved manual approvals, and returns details.
   - **`POST /api/action/{session_id}`**: Submits a structured function response to resume the human-in-the-loop workflow.

## Verification

The service is currently running at `http://127.0.0.1:8000`. The `/api/pending` route was queried successfully, and it returned the list of pending approvals:

```json
[
  {
    "session_id": "2479069416902361088",
    "user_id": "cli-user",
    "interrupt_id": "manual_approval",
    "message": "Expense of $150.00 from Unknown Merchant requires approval. Approve? (yes/no)",
    "expense": {"amount": 150, "merchant": null, "description": "Client dinner"},
    "timestamp": 1781923850.701978
  },
  ...
]
```
