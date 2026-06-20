import asyncio
import json
import google.auth
from google.genai import types
import vertexai

async def main():
    # Read the engine ID from deployment metadata
    with open("deployment_metadata.json") as f:
        metadata = json.load(f)
        engine_id = metadata["remote_agent_runtime_id"]

    print(f"Target reasoning engine ID: {engine_id}")
    
    # Initialize the client
    client = vertexai.Client(location="us-east1")
    
    # 1. Test Case 1: $50 (Auto Approve)
    input_data_1 = {
        "amount": 50.0,
        "merchant": "Acme Corp",
        "description": "Office supplies"
    }
    
    print("\n--- Deployed Test Case 1: Querying with $50 claim ---")
    
    # Try querying using _query or stream_query
    # Since agent_engines has sessions, let's create a session first
    session = await client.agent_engines.sessions.create(
        parent=engine_id,
        session_id="deployed_test_session_1"
    )
    print(f"Created session: {session.name}")
    
    # Now query the session
    try:
        # Let's see if we can query via the sessions service or _query
        print("Querying via client.agent_engines._query...")
        # Prepare the query request
        from google.genai import types
        # Note: the input must match what the workflow expects.
        # In ADK, it wraps the request as Content.
        # Since it's a workflow with base template adk, the input is passed via new_message.
        # Let's inspect the types for query
        # Let's try _query first
        response = await client.agent_engines.aio._query(
            name=engine_id,
            input=input_data_1,
            user_id="test_user"
        )
        print("Response:", response)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
