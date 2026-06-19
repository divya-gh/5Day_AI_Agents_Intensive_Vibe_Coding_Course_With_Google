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

import datetime
import os
from functools import cached_property
from typing import Optional
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import Client, types

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id or "mock-project-id"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
# If a Developer API Key is provided, disable Vertex AI so the SDK routes correctly
if os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


# In-memory store for discount codes and their redemption status
# Single-use codes: "WELCOME50" and "SUMMER20"
# Format: {code: redeemed_flag}
DISCOUNT_CODES = {
    "WELCOME50": False,
    "SUMMER20": False,
}

# Registered users list (simulated database)
REGISTERED_USERS = {"user123", "user456", "student_user"}

# In-memory store for user loyalty points
LOYALTY_POINTS = {
    "user123": 0,
    "user456": 0,
    "student_user": 0,
}

# In-memory store for processed order IDs to prevent replay attacks
PROCESSED_ORDERS = set()

# In-memory store for shopping carts
CARTS = {
    "cart1": {"user_id": "user123", "total": 100.0, "is_checked_out": False},
    "cart2": {"user_id": "user456", "total": 200.0, "is_checked_out": False},
    "cart3": {"user_id": "student_user", "total": 50.0, "is_checked_out": False},
}


def redeem_discount(code: str, user_id: str) -> str:
    """Redeems a single-use discount code for a registered user.

    Args:
        code: The discount code to redeem (e.g., 'WELCOME50', 'SUMMER20').
        user_id: The registered user ID (e.g., 'user123').

    Returns:
        A string message indicating whether the redemption was successful or why it failed.
    """
    if user_id not in REGISTERED_USERS:
        return f"Redemption failed: User ID '{user_id}' is not a registered user."

    code_upper = code.upper()
    if code_upper not in DISCOUNT_CODES:
        return f"Redemption failed: Discount code '{code}' is invalid."

    if DISCOUNT_CODES[code_upper]:
        return f"Redemption failed: Discount code '{code}' has already been redeemed."

    # Mark as redeemed
    DISCOUNT_CODES[code_upper] = True
    return f"Success: Discount code '{code}' has been successfully redeemed for user '{user_id}'!"


def award_loyalty_points(user_id: str, points: int, order_id: str) -> str:
    """Awards loyalty points to a registered user's account after a successful purchase.

    Args:
        user_id: The registered user ID (e.g., 'user123').
        points: The number of loyalty points to award (must be a positive integer).
        order_id: The unique order ID associated with the successful purchase (e.g., 'ORD123').

    Returns:
        A string message indicating the outcome of the points award.
    """
    if user_id not in REGISTERED_USERS:
        return f"Error: User ID '{user_id}' is not a registered user."

    if points <= 0:
        return f"Error: Points to award must be a positive integer. Provided: {points}"

    clean_order_id = order_id.strip()
    if not clean_order_id:
        return "Error: Order ID cannot be empty."

    if clean_order_id in PROCESSED_ORDERS:
        return f"Error: Order ID '{clean_order_id}' has already been processed. Points cannot be awarded again."

    # Process award
    PROCESSED_ORDERS.add(clean_order_id)
    current_points = LOYALTY_POINTS.get(user_id, 0)
    new_points = current_points + points
    LOYALTY_POINTS[user_id] = new_points

    return f"Success: Awarded {points} loyalty points to user '{user_id}' for order '{clean_order_id}'. New balance: {new_points} points."


def process_cart_checkout(
    cart_id: str, user_id: str, discount_code: Optional[str] = None
) -> str:
    """Processes the checkout of a shopping cart, applying an optional discount code and generating an order ID.

    Args:
        cart_id: The unique cart ID to checkout (e.g., 'cart1').
        user_id: The registered user ID completing the checkout (e.g., 'user123').
        discount_code: The optional discount code to apply (e.g., 'WELCOME50').

    Returns:
        A string summarizing the checkout outcome (original total, discount applied, final total, and order ID).
    """
    if user_id not in REGISTERED_USERS:
        return f"Checkout failed: User ID '{user_id}' is not a registered user."

    if cart_id not in CARTS:
        return f"Checkout failed: Cart ID '{cart_id}' does not exist."

    cart = CARTS[cart_id]
    if cart["user_id"] != user_id:
        return f"Checkout failed: Cart '{cart_id}' does not belong to user '{user_id}'."

    if cart["is_checked_out"]:
        return f"Checkout failed: Cart '{cart_id}' has already been checked out."

    original_total = float(cart["total"])
    discount_amount = 0.0
    final_total = original_total

    # Apply discount code if provided
    if discount_code:
        code_upper = discount_code.upper()
        if code_upper not in DISCOUNT_CODES:
            return f"Checkout failed: Invalid discount code '{discount_code}'."
        if DISCOUNT_CODES[code_upper]:
            return f"Checkout failed: Discount code '{discount_code}' has already been redeemed."

        # Mark discount code as redeemed
        DISCOUNT_CODES[code_upper] = True
        # Apply 50% discount
        discount_amount = original_total * 0.5
        final_total = original_total - discount_amount

    # Mark cart as checked out
    cart["is_checked_out"] = True
    cart["total"] = final_total

    # Generate a unique order ID
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = f"ORD-{timestamp}-{cart_id}"

    return (
        f"Checkout success: Order {order_id} processed for user '{user_id}'. "
        f"Original Total: ${original_total:.2f}, Discount Applied: ${discount_amount:.2f}, "
        f"Final Total Charged: ${final_total:.2f}."
    )


class KeyedGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyD-mock-key-value-12345"
        return Client(api_key=api_key)

    @cached_property
    def _live_api_client(self) -> Client:
        api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyD-mock-key-value-12345"
        return Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                headers=self._tracking_headers(),
                api_version=self._live_api_version,
            ),
        )


root_agent = Agent(
    name="root_agent",
    model=KeyedGemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are an AI shopping assistant for a retail store.
Help users browse products, answer questions, redeem single-use discount codes (such as WELCOME50 and SUMMER20), process cart checkouts, and award loyalty points.
When a user wants to redeem a discount code, you must ask for their discount code and registered user ID, then use the redeem_discount tool to process it.
When a user wants to check out their cart, you must ask for their cart ID, registered user ID, and any discount code, then use the process_cart_checkout tool.
When a user has made a successful purchase and has an order ID, you must ask for their registered user ID, the order ID, and the number of points to award, then use the award_loyalty_points tool to award them.""",
    tools=[redeem_discount, award_loyalty_points, process_cart_checkout],
)

app = App(
    root_agent=root_agent,
    name="app",
)
