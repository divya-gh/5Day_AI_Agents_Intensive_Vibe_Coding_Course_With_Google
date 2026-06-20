# Implementation Plan — Ambient Expense Agent

Build a local prototype of an ambient expense agent using Agents CLI and ADK 2.0. The agent automatically processes expense claims:
- Expenses under $100 are automatically approved via the `auto_approve` node.
- Expenses of $100 or more are routed to the `review_agent` node, which triggers a human-in-the-loop pause (`RequestInput`) to get manual approval.

## Proposed Changes

### [Component: Expense Agent Prototype]

#### [NEW] [expense-agent/](file:///C:/Users/divya/.gemini/antigravity/scratch/expense-agent)
We will scaffold the project inside `C:\Users\divya\.gemini\antigravity\scratch\expense-agent`.

#### [NEW] [expense_agent/agent.py](file:///C:/Users/divya/.gemini/antigravity/scratch/expense-agent/app/agent.py)
We will implement the ADK 2.0 Workflow graph in `app/agent.py`. It will have:
- **Input Schema**: `ExpenseInput` containing `amount: float`, `merchant: str`, and `description: str`.
- **Output Schema**: `ExpenseResult` containing `status: str` ("Approved" or "Rejected"), `amount: float`, and `reason: str`.
- **Workflow Edges**:
  - `START` to `classify_expense` function.
  - `classify_expense` route `"approve"` to `auto_approve`.
  - `classify_expense` route `"review"` to `review_agent`.
  - `auto_approve` to final output.
  - `review_agent` to final output.
- **`review_agent` behavior**:
  - Yields a `RequestInput` with `interrupt_id="manual_approval"` and a prompt asking the reviewer to approve or reject.
  - Checks `ctx.resume_inputs` on resumption to determine if the expense is approved.

## Verification Plan

### Automated/Local Tests
- Run `agents-cli run "Submit expense of $50 from Acme Corp"` to verify automatic approval.
- Run `agents-cli run "Submit expense of $150 from TechCorp"` to verify hitl pause (`RequestInput` returned).
- Run `agents-cli run` with a simulated resume input to verify the review agent completes processing.
