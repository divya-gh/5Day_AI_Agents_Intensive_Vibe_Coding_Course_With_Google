import asyncio
import json

from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import app


async def test_flow():
    runner = InMemoryRunner(app=app)

    # 1. Test Auto Approve ($50)
    session1 = await runner.session_service.create_session(
        app_name="app", user_id="test_user"
    )
    print("\n--- Running Test 1: $50 (Should Auto-Approve) ---")

    input_data = {
        "amount": 50.0,
        "merchant": "Acme Corp",
        "description": "Office supplies",
    }

    async for event in runner.run_async(
        user_id="test_user",
        session_id=session1.id,
        new_message=types.Content(
            role="user", parts=[types.Part.from_text(text=json.dumps(input_data))]
        ),
    ):
        if event.output is not None:
            print("Final Output Event:", event.output)

    # 2. Test Review Agent ($150)
    session2 = await runner.session_service.create_session(
        app_name="app", user_id="test_user"
    )
    print("\n--- Running Test 2: $150 (Should Pause for Review) ---")

    input_data_large = {
        "amount": 150.0,
        "merchant": "TechCorp",
        "description": "New Laptop",
    }

    async for event in runner.run_async(
        user_id="test_user",
        session_id=session2.id,
        new_message=types.Content(
            role="user", parts=[types.Part.from_text(text=json.dumps(input_data_large))]
        ),
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_input"
                ):
                    print(
                        f"Workflow paused. Request message: {part.function_call.args.get('message')}"
                    )

    # 3. Resume with Yes (Approval)
    print("\n--- Simulating Reviewer Approval: yes (Should Approve) ---")
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session2.id,
        new_message=types.Content(
            role="user",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        name="adk_request_input",
                        id="manual_approval",
                        response={"response": "yes"},
                    )
                )
            ],
        ),
    ):
        if event.output is not None:
            print("Final Resumed Output Event:", event.output)

    # 4. Resume with No (Rejection)
    session3 = await runner.session_service.create_session(
        app_name="app", user_id="test_user"
    )
    print("\n--- Running Test 3: $200 with Rejection (Should Reject) ---")

    input_data_reject = {
        "amount": 200.0,
        "merchant": "LuxuryStore",
        "description": "Premium gifts",
    }

    async for _event in runner.run_async(
        user_id="test_user",
        session_id=session3.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part.from_text(text=json.dumps(input_data_reject))],
        ),
    ):
        pass

    # Resume with "no"
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session3.id,
        new_message=types.Content(
            role="user",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        name="adk_request_input",
                        id="manual_approval",
                        response={"response": "no"},
                    )
                )
            ],
        ),
    ):
        if event.output is not None:
            print("Final Resumed Output Event:", event.output)


if __name__ == "__main__":
    asyncio.run(test_flow())
