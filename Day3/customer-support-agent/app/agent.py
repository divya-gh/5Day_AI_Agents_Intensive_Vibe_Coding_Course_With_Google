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
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions
from google.adk.models import Gemini
from google.adk.workflow import Workflow, node
from google.genai import types

# Load .env file for GEMINI_API_KEY if present
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

# Initialize model
model = Gemini(
    model="gemini-2.5-flash",
    retry_options=types.HttpRetryOptions(attempts=3),
)


# Schemas
class Classification(BaseModel):
    is_shipping_related: bool = Field(
        description="True if the user's query is related to shipping (rates, tracking, delivery, returns). False otherwise."
    )


# Nodes
@node
def store_query(ctx: Context, node_input: types.Content) -> Event:
    """Stores the original query text in the context state for downstream nodes."""
    query = ""
    if hasattr(node_input, "parts") and node_input.parts:
        query = "".join(part.text for part in node_input.parts if part.text)
    else:
        query = str(node_input)
    return Event(output=query, actions=EventActions(state_delta={"user_query": query}))


classifier = LlmAgent(
    name="classifier",
    model=model,
    instruction=(
        "You are an assistant that classifies customer support queries.\n"
        "Analyze the user's query and determine if it is related to shipping (e.g., rates, tracking, delivery, returns) or unrelated.\n"
        "Output the classification in the required schema."
    ),
    output_schema=Classification,
)


@node
def route_query(ctx: Context, node_input: dict) -> Event:
    """Routes the flow depending on the classification result."""
    is_shipping = node_input.get("is_shipping_related", False)
    user_query = ctx.state.get("user_query", "")
    route = "shipping" if is_shipping else "unrelated"
    return Event(output=user_query, actions=EventActions(route=route))


faq_agent = LlmAgent(
    name="faq_agent",
    model=model,
    instruction=(
        "You are a super playful, enthusiastic, and helpful customer support representative for a shipping company! 🎉🚀\n"
        "Provide a fun, energetic, and helpful answer to the user's shipping query based on their question, using plenty of happy emojis. ✨\n"
        "When talking about shipping rates, be sure to enthusiastically highlight that we offer **FREE shipping on all orders over $50**! 🚚💨💰\n"
        "If you do not know the exact tracking status, provide general helpful information on how they can track it or look up rates in a cheerful way."
    ),
)


@node
def decline_node(ctx: Context, node_input: str) -> Event:
    """Politely declines to answer non-shipping queries."""
    msg = "I'm sorry, but I can only answer questions related to shipping (such as rates, tracking, delivery, and returns). Let me know if you have a shipping-related inquiry!"
    yield Event(
        content=types.Content(role="model", parts=[types.Part.from_text(text=msg)])
    )
    yield Event(output=msg)


# Graph workflow definition
root_agent = Workflow(
    name="customer_support_workflow",
    edges=[
        ("START", store_query),
        (store_query, classifier),
        (classifier, route_query),
        (route_query, {"shipping": faq_agent, "unrelated": decline_node}),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
