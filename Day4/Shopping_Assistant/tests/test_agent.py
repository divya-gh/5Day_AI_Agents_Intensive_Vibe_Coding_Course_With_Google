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

import pytest
from dotenv import load_dotenv
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import (
    DISCOUNT_CODES,
    redeem_discount,
    root_agent,
)

load_dotenv()


@pytest.fixture(autouse=True)
def reset_discount_state():
    """Resets the discount codes state before each test to ensure test independence."""
    DISCOUNT_CODES.clear()
    DISCOUNT_CODES.update(
        {
            "WELCOME50": False,
            "SUMMER20": False,
        }
    )


# =====================================================================
# Unit Tests for redeem_discount Tool Business Logic & Guardrails
# =====================================================================


def test_redeem_discount_success():
    """Verify that a registered user can successfully redeem a valid, unused discount code."""
    result = redeem_discount(code="WELCOME50", user_id="user123")
    assert "Success" in result
    assert "successfully redeemed" in result
    assert DISCOUNT_CODES["WELCOME50"] is True


def test_redeem_discount_case_insensitive():
    """Verify that discount codes are treated case-insensitively (e.g. lowercase is converted)."""
    result = redeem_discount(code="welcome50", user_id="user123")
    assert "Success" in result
    assert DISCOUNT_CODES["WELCOME50"] is True


def test_redeem_discount_unregistered_user():
    """Verify that an unregistered user cannot redeem a discount code."""
    result = redeem_discount(code="WELCOME50", user_id="unregistered_spy")
    assert "Redemption failed" in result
    assert "is not a registered user" in result
    assert DISCOUNT_CODES["WELCOME50"] is False


def test_redeem_discount_invalid_code():
    """Verify that an invalid or non-existent discount code cannot be redeemed."""
    result = redeem_discount(code="FAKE50", user_id="user123")
    assert "Redemption failed" in result
    assert "is invalid" in result


def test_redeem_discount_double_redemption_prevented():
    """Verify that a discount code cannot be redeemed twice (replay/double-redemption boundary)."""
    # First redemption succeeds
    result1 = redeem_discount(code="WELCOME50", user_id="user123")
    assert "Success" in result1

    # Second redemption fails
    result2 = redeem_discount(code="WELCOME50", user_id="user123")
    assert "Redemption failed" in result2
    assert "already been redeemed" in result2


# =====================================================================
# Outcome-Based Agent E2E / Integration Tests using ADK Runner
# =====================================================================


def run_agent_prompt(prompt: str, user_id: str) -> str:
    """Helper function to execute a prompt against the root_agent via ADK Runner."""
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id=user_id, app_name="test_app")
    runner = Runner(
        agent=root_agent, session_service=session_service, app_name="test_app"
    )

    message = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])

    events = list(
        runner.run(
            new_message=message,
            user_id=user_id,
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        )
    )

    # Aggregate text responses from agent events
    response_text = ""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    return response_text


def test_agent_redeem_discount_success_outcome():
    """Verify that the agent successfully processes a valid redemption query."""
    response = run_agent_prompt(
        prompt="Please redeem code WELCOME50 for user123", user_id="user123"
    )
    assert DISCOUNT_CODES["WELCOME50"] is True
    # The agent should report success
    assert any(
        term in response.lower()
        for term in ["success", "redeem", "applied", "completed"]
    )


def test_agent_redeem_discount_failure_unregistered_user():
    """Verify that the agent correctly reports failure when the user is unregistered."""
    response = run_agent_prompt(
        prompt="Please redeem code WELCOME50 for unregistered_spy",
        user_id="unregistered_spy",
    )
    assert DISCOUNT_CODES["WELCOME50"] is False
    assert any(
        term in response.lower()
        for term in ["fail", "not registered", "invalid", "error", "cannot"]
    )


def test_agent_redeem_discount_replay_prevention():
    """Verify that the agent cannot reuse a discount code that is already redeemed."""
    # Pre-redeem the code
    DISCOUNT_CODES["WELCOME50"] = True

    response = run_agent_prompt(
        prompt="Please redeem code WELCOME50 for user123", user_id="user123"
    )
    # The agent must convey the refusal/already redeemed status
    assert any(
        term in response.lower()
        for term in ["already", "fail", "invalid", "used", "error"]
    )
