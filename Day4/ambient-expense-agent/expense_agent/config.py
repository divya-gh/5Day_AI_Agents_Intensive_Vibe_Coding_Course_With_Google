"""
Configuration for the Ambient Expense Approval Agent.

Centralises the approval threshold and model name so they're easy to
tweak without touching the workflow graph.
"""

# ── Approval rule ──────────────────────────────────────────────
# Expenses *below* this dollar amount are auto-approved instantly
# (no LLM call, no human review).
APPROVAL_THRESHOLD: float = 100.0

# ── LLM model ─────────────────────────────────────────────────
# Used only for the risk-assessment step on high-value expenses.
MODEL_NAME: str = "gemini-3.1-flash-lite"
