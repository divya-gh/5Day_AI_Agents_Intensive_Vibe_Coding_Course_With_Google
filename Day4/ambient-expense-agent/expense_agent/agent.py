# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Ambient Expense Approval Agent — ADK 2.0 Workflow Graph
========================================================

Graph topology
--------------

    START
      │
      ▼
  parse_expense              ← decode Pub/Sub base64 *or* plain JSON
      │
      ▼
  route_expense              ← python threshold check, no LLM
      │
      ├─ "auto_approve" ──▶  auto_approve        ← stamp & exit
      │
      └─ "needs_review" ──▶  security_checkpoint ← scrub PII, detect injection
                                  │
                                  ├─ "clean" ──────▶  risk_reviewer  ← LLM risk analysis
                                  │                        │
                                  │                        ▼
                                  └─ "injection" ──▶  human_approval ← HITL pause
                                                           │
                                                           ▼
                                                     record_decision ← persist & exit
"""

from __future__ import annotations

import base64
import json
import re
from typing import Any

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.apps import App, ResumabilityConfig
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.adk.workflow import Workflow, node
from google.genai import types
from pydantic import BaseModel

from . import config

load_dotenv()  # loads GOOGLE_API_KEY from .env


# ╔══════════════════════════════════════════════════════════════╗
# ║  Schemas                                                     ║
# ╚══════════════════════════════════════════════════════════════╝

class RiskAssessment(BaseModel):
    """Structured output the LLM must return."""

    risk_level: str          # "low" | "medium" | "high"
    risk_factors: list[str]  # specific concerns found
    recommendation: str      # "approve" | "reject" | "escalate"
    summary: str             # one-paragraph narrative


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 1 — parse_expense                                      ║
# ║  Handles both real Pub/Sub (base64 under "data") and local   ║
# ║  testing (plain JSON).                                        ║
# ╚══════════════════════════════════════════════════════════════╝

def parse_expense(node_input: Any) -> dict:
    """Extract expense fields from the incoming event payload.

    Supports two formats:
    • Pub/Sub envelope  → {"data": "<base64-encoded JSON>"}
    • Local / testing   → {"data": {…}}  or  raw {amount, submitter, …}
    """
    # START with no input_schema delivers types.Content
    if hasattr(node_input, "parts") and node_input.parts:
        text = node_input.parts[0].text
    elif isinstance(node_input, str):
        text = node_input
    else:
        text = str(node_input)

    payload: dict = json.loads(text)

    # ── unwrap Pub/Sub envelope ──
    if "data" in payload:
        raw = payload["data"]
        if isinstance(raw, str):
            try:
                decoded = base64.b64decode(raw).decode("utf-8")
                return json.loads(decoded)
            except Exception:
                # Not base64 — treat as a plain JSON string
                return json.loads(raw)
        if isinstance(raw, dict):
            return raw

    # ── already a flat expense object ──
    return payload


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 2 — route_expense                                      ║
# ║  Pure-python threshold check.  Returns an Event whose        ║
# ║  `route` string selects the next branch in the graph.        ║
# ╚══════════════════════════════════════════════════════════════╝

def route_expense(node_input: dict) -> Event:
    """Route the expense based on the dollar threshold in config."""
    amount = float(node_input.get("amount", 0))

    if amount < config.APPROVAL_THRESHOLD:
        return Event(
            output=node_input,
            route="auto_approve",
            state={"expense": node_input},
        )

    return Event(
        output=node_input,
        route="needs_review",
        state={"expense": node_input},
    )


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 3a — auto_approve  (< threshold branch)               ║
# ║  No LLM, no human — just stamp it.                          ║
# ╚══════════════════════════════════════════════════════════════╝

def auto_approve(node_input: dict):
    """Instantly approve a low-value expense."""
    amount = float(node_input.get("amount", 0))
    result = {
        "status": "approved",
        "decided_by": "auto",
        "reason": (
            f"Amount ${amount:.2f} is below the "
            f"${config.APPROVAL_THRESHOLD:.2f} auto-approval threshold"
        ),
        "expense": node_input,
    }
    # Content event → visible in the ADK web UI / playground
    yield Event(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(
                text=f"✅ Auto-approved:\n```json\n{json.dumps(result, indent=2)}\n```"
            )],
        ),
    )
    # Output event → terminates this branch and saves state
    yield Event(output=result, state={"result": result})


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 3b — security_checkpoint  (≥ threshold branch)        ║
# ║  Scrubs PII and detects prompt injection BEFORE any data     ║
# ║  reaches the LLM or appears in logs / human-review cards.   ║
# ╚══════════════════════════════════════════════════════════════╝

# ── PII patterns ──
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_CC_RE = re.compile(
    r"\b(?:\d{4}[- ]?){3}\d{4}\b"          # 16-digit card numbers
)

# ── Prompt-injection patterns (case-insensitive) ──
_INJECTION_RES = [
    re.compile(r"ignore\s+(?:previous|above|all|prior)\s+(?:instructions?|rules?|prompts?)", re.I),
    re.compile(r"(?:auto[- ]?approve|force\s+approv|bypass|override|skip\s+review)", re.I),
    re.compile(r"you\s+(?:are|must)\s+now", re.I),
    re.compile(r"(?:system|assistant)\s*:", re.I),
    re.compile(r"(?:do\s+not|don't|never)\s+(?:check|review|flag|reject)", re.I),
    re.compile(r"<\s*/?(?:system|prompt|instruction)", re.I),
    re.compile(r"\]\]>|\{\{|%\{|\$\{", re.I),  # template / escape tricks
]


def security_checkpoint(node_input: dict):
    """Scrub PII and detect prompt injection before the LLM sees anything.

    Routes:
        "clean"     → safe to send to the LLM risk reviewer
        "injection" → bypass the LLM, escalate straight to a human
    """
    expense = dict(node_input)  # shallow copy — don't mutate upstream data
    original_desc = expense.get("description", "")
    description = original_desc
    redacted_categories: list[str] = []

    # ── 1. Scrub SSNs ──
    if _SSN_RE.search(description):
        description = _SSN_RE.sub("[REDACTED-SSN]", description)
        redacted_categories.append("SSN")

    # ── 2. Scrub credit-card numbers ──
    if _CC_RE.search(description):
        description = _CC_RE.sub("[REDACTED-CC]", description)
        redacted_categories.append("credit_card")

    expense["description"] = description  # cleaned version for all downstream

    # ── 3. Detect prompt injection (check the ORIGINAL text) ──
    matched_patterns: list[str] = []
    for pattern in _INJECTION_RES:
        match = pattern.search(original_desc)
        if match:
            matched_patterns.append(match.group())

    if matched_patterns:
        # Emit a visible security alert *before* the routing Event
        yield Event(
            content=types.Content(
                role="model",
                parts=[types.Part.from_text(
                    text=(
                        "🚨  PROMPT-INJECTION DETECTED — bypassing LLM reviewer\n"
                        f"    Matched: {matched_patterns}\n"
                        "    Routing directly to human review."
                    )
                )],
            ),
        )
        yield Event(
            output=expense,
            route="injection",
            state={
                "expense": expense,
                "redacted_categories": redacted_categories,
                "security_alert": {
                    "type": "prompt_injection",
                    "matched_patterns": matched_patterns,
                    "original_description": original_desc,
                },
            },
        )
        return

    # ── Clean — proceed to LLM ──
    yield Event(
        output=expense,
        route="clean",
        state={
            "expense": expense,
            "redacted_categories": redacted_categories,
        },
    )


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 3c — risk_reviewer  (clean expenses only)             ║
# ║  The ONLY node that calls the LLM.                           ║
# ╚══════════════════════════════════════════════════════════════╝

risk_reviewer = LlmAgent(
    name="risk_reviewer",
    model=config.MODEL_NAME,
    instruction=(
        "You are a corporate expense-risk analyst.\n\n"
        "You will receive an expense report as JSON.  Analyse it for risk "
        "factors such as:\n"
        "• Amount unusually high for the stated category\n"
        "• Vague or missing description\n"
        "• Weekend or holiday submission date\n"
        "• Category / description mismatch\n"
        "• Potential policy violations\n\n"
        "Return a structured risk assessment."
    ),
    output_schema=RiskAssessment,
    output_key="risk_assessment",   # also stored in ctx.state
)


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 4 — human_approval  (HITL)                            ║
# ║  Pauses the workflow with RequestInput; resumes when the     ║
# ║  human replies.                                              ║
# ║                                                              ║
# ║  Two incoming edges:                                         ║
# ║    • risk_reviewer  → normal review (risk_assessment in      ║
# ║                       state)                                 ║
# ║    • security_checkpoint "injection" → LLM bypassed          ║
# ║      (security_alert in state, no risk_assessment)           ║
# ╚══════════════════════════════════════════════════════════════╝

@node(rerun_on_resume=True)
async def human_approval(ctx: Context, node_input: dict):
    """Pause for a human to approve or reject the expense."""
    expense = ctx.state.get("expense", {})
    risk = ctx.state.get("risk_assessment", {})
    security_alert = ctx.state.get("security_alert")
    redacted = ctx.state.get("redacted_categories", [])

    # ── first run: present the review card and pause ──
    if not ctx.resume_inputs:
        # -- expense details (shared by both paths) --
        expense_block = (
            f"  Submitter:   {expense.get('submitter', 'N/A')}\n"
            f"  Amount:      ${float(expense.get('amount', 0)):.2f}\n"
            f"  Category:    {expense.get('category', 'N/A')}\n"
            f"  Description: {expense.get('description', 'N/A')}\n"
            f"  Date:        {expense.get('date', 'N/A')}"
        )
        if redacted:
            expense_block += f"\n  ⚠️  Redacted fields: {', '.join(redacted)}"

        if security_alert:
            # ── injection-detected path (LLM was bypassed) ──
            patterns = security_alert.get("matched_patterns", [])
            header = (
                "🚨  SECURITY ALERT — MANUAL REVIEW REQUIRED\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            )
            detail_block = (
                "\n"
                "🛡️  SECURITY DETAILS\n"
                f"  Type:     {security_alert.get('type', 'unknown')}\n"
                f"  Matches:  {', '.join(patterns)}\n"
                "\n"
                "⚠️  This expense bypassed the LLM reviewer due to\n"
                "    suspected prompt injection in the description.\n"
            )
        else:
            # ── normal review path (risk assessment available) ──
            risk_factors = risk.get("risk_factors", [])
            header = (
                "🔍  EXPENSE REVIEW REQUIRED\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            )
            detail_block = (
                "\n"
                "📊  RISK ASSESSMENT\n"
                f"  Level:          {risk.get('risk_level', 'N/A')}\n"
                f"  Factors:        {', '.join(risk_factors) if risk_factors else 'none'}\n"
                f"  Recommendation: {risk.get('recommendation', 'N/A')}\n"
                f"  Summary:        {risk.get('summary', 'N/A')}\n"
            )

        message = (
            header
            + expense_block
            + detail_block
            + "\n👉  Reply with  approve  or  reject  (optionally followed by a reason)."
        )
        yield RequestInput(interrupt_id="expense_decision", message=message)
        return  # workflow suspends here

    # ── second run (after human replies): read their decision ──
    decision_text = ctx.resume_inputs["expense_decision"]
    yield Event(output={
        "decision_text": decision_text,
        "expense": expense,
        "risk_assessment": risk,
        "security_alert": security_alert,
    })


# ╔══════════════════════════════════════════════════════════════╗
# ║  Node 5 — record_decision                                   ║
# ║  Converts the human's free-text reply into a structured      ║
# ║  outcome and emits a visible summary.                        ║
# ╚══════════════════════════════════════════════════════════════╝

def record_decision(node_input: dict):
    """Turn the human's reply into a final, structured decision record."""
    decision_text = str(node_input.get("decision_text", ""))
    expense = node_input.get("expense", {})
    approved = "approve" in decision_text.lower()

    result = {
        "status": "approved" if approved else "rejected",
        "decided_by": "human",
        "reason": decision_text,
        "expense": expense,
        "risk_assessment": node_input.get("risk_assessment", {}),
        "security_alert": node_input.get("security_alert"),
    }

    emoji = "✅" if approved else "❌"
    yield Event(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(
                text=f"{emoji}  Decision recorded:\n```json\n{json.dumps(result, indent=2)}\n```"
            )],
        ),
    )
    yield Event(output=result, state={"result": result})


# ╔══════════════════════════════════════════════════════════════╗
# ║  Workflow Graph                                              ║
# ╚══════════════════════════════════════════════════════════════╝

root_agent = Workflow(
    name="expense_approval",
    edges=[
        # ── stage 1: ingest ──
        ("START", parse_expense),
        (parse_expense, route_expense),
        # ── stage 2: amount branch ──
        (route_expense, {
            "auto_approve": auto_approve,
            "needs_review": security_checkpoint,
        }),
        # ── stage 3: security branch ──
        (security_checkpoint, {
            "clean": risk_reviewer,
            "injection": human_approval,
        }),
        # ── stage 4: review → decision ──
        (risk_reviewer, human_approval),
        (human_approval, record_decision),
    ],
)


# ╔══════════════════════════════════════════════════════════════╗
# ║  App (entry-point for `agents-cli playground / run`)         ║
# ║  ResumabilityConfig enables the HITL pause-and-resume cycle. ║
# ╚══════════════════════════════════════════════════════════════╝

app = App(
    name="expense_agent",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(),
)
