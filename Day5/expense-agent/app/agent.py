# ruff: noqa
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

import os
import google.auth
from pydantic import BaseModel
from typing import Any, Optional
import json
from google.adk.workflow import Workflow, node, Edge
from google.adk.events.event import Event, EventActions
from google.adk.events.request_input import RequestInput
from google.adk.agents.context import Context
from google.adk.apps import App
from google.genai import types

# Set up GCP environment variables
try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    pass

os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


class ExpenseInput(BaseModel):
    amount: float
    merchant: Optional[str] = None
    description: Optional[str] = None


class ExpenseResult(BaseModel):
    status: str
    amount: float
    reason: str


@node
def classify_expense(ctx: Context, node_input: Any) -> Event:
    try:
        # 1. Parse or resolve input to a dictionary
        data_dict = None
        if isinstance(node_input, dict):
            data_dict = node_input
        elif isinstance(node_input, str):
            data_dict = json.loads(node_input)
        elif hasattr(node_input, "parts") and node_input.parts:
            text = node_input.parts[0].text
            try:
                data_dict = json.loads(text)
            except json.JSONDecodeError:
                data_dict = {"amount": 0.0, "merchant": None, "description": text}
        else:
            data_dict = dict(node_input)

        # 2. Check if the payload is nested under a 'data' key
        if (
            isinstance(data_dict, dict)
            and "data" in data_dict
            and isinstance(data_dict["data"], dict)
        ):
            payload = data_dict["data"]
        else:
            payload = data_dict

        # 3. Validate against ExpenseInput schema
        expense = ExpenseInput(**payload)

        # Store expense in state so it persists across turns
        return Event(
            output=expense,
            actions=EventActions(
                route="review" if expense.amount >= 100.0 else "approve",
                state_delta={"expense": expense.model_dump()},
            ),
        )
    except Exception as e:
        # Try to recover from state during resumption turns
        if "expense" in ctx.state:
            expense = ExpenseInput(**ctx.state["expense"])
            if expense.amount < 100.0:
                return Event(output=expense, actions=EventActions(route="approve"))
            return Event(output=expense, actions=EventActions(route="review"))
        raise e


@node
def auto_approve(node_input: ExpenseInput) -> ExpenseResult:
    return ExpenseResult(
        status="Approved",
        amount=node_input.amount,
        reason=f"Expense of ${node_input.amount:.2f} under $100 auto-approved.",
    )


@node(rerun_on_resume=True)
async def review_agent(ctx: Context, node_input: ExpenseInput):
    if not ctx.resume_inputs:
        merchant_name = node_input.merchant or "Unknown Merchant"
        yield RequestInput(
            interrupt_id="manual_approval",
            message=f"Expense of ${node_input.amount:.2f} from {merchant_name} requires approval. Approve? (yes/no)",
        )
        return

    resume_val = ctx.resume_inputs.get("manual_approval")
    if isinstance(resume_val, dict):
        approval_response = resume_val.get("response", "").strip().lower()
    else:
        approval_response = str(resume_val).strip().lower()

    if approval_response in ["yes", "y", "approve", "approved"]:
        yield Event(
            output=ExpenseResult(
                status="Approved",
                amount=node_input.amount,
                reason="Expense approved manually by reviewer.",
            )
        )
    else:
        yield Event(
            output=ExpenseResult(
                status="Rejected",
                amount=node_input.amount,
                reason="Expense rejected manually by reviewer.",
            )
        )


root_agent = Workflow(
    name="expense_agent",
    edges=[
        ("START", classify_expense),
        Edge(from_node=classify_expense, to_node=auto_approve, route="approve"),
        Edge(from_node=classify_expense, to_node=review_agent, route="review"),
    ],
    output_schema=ExpenseResult,
)

app = App(
    root_agent=root_agent,
    name="app",
)
