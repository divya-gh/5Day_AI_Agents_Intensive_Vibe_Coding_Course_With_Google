import os
import json
import asyncio
import base64
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from expense_agent.agent import root_agent

def serialize_bytes(obj):
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8')
        except Exception:
            return base64.b64encode(obj).decode('utf-8')
    if isinstance(obj, set):
        return sorted(list(obj))
    if isinstance(obj, dict):
        return {k: serialize_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize_bytes(v) for v in obj]
    return obj

def map_adk_event_to_agent_event(event, default_agent_name="expense_approval"):
    if not event.content:
        return None
        
    author = event.author
    if author == "eval_user":
        author = "user"
        
    content_dict = serialize_bytes(event.content.model_dump(exclude_none=True))
    
    is_tool_response = False
    if "parts" in content_dict:
        for part in content_dict["parts"]:
            if "function_response" in part:
                is_tool_response = True
                break
                
    if is_tool_response:
        author = "tool"
    elif author != "user":
        author = default_agent_name
        
    return {
        "author": author,
        "content": content_dict
    }

async def main():
    dataset_path = "tests/eval/datasets/basic-dataset.json"
    output_path = "artifacts/traces/generated_traces.json"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    generated_cases = []
    
    for case in dataset["eval_cases"]:
        case_id = case["eval_case_id"]
        prompt_text = case["prompt"]["parts"][0]["text"]
        print(f"Running scenario: {case_id}...")
        
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(user_id="eval_user", app_name="expense_agent")
        runner = Runner(agent=root_agent, session_service=session_service, app_name="expense_agent")
        
        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)]
        )
        
        # Run first turn
        events = list(
            runner.run(
                new_message=user_message,
                user_id="eval_user",
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE)
            )
        )
        
        # Check if we were interrupted for human approval
        is_interrupted = False
        for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_call and part.function_call.name == "adk_request_input":
                        is_interrupted = True
                        break
        
        resume_events = []
        decision = None
        if is_interrupted:
            if "ignore" in prompt_text.lower() or "bypass" in prompt_text.lower():
                decision = "reject"
            else:
                decision = "approve"
            
            print(f"  [HITL] Intercepted human approval. Automating decision: {decision}")
            
            resume_message = types.Content(
                role="tool",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            id="expense_decision",
                            name="adk_request_input",
                            response={"expense_decision": decision}
                        )
                    )
                ]
            )
            
            # Resume run
            resume_events = list(
                runner.run(
                    new_message=resume_message,
                    user_id="eval_user",
                    session_id=session.id,
                    run_config=RunConfig(streaming_mode=StreamingMode.SSE)
                )
            )
            
        # Compile turns
        turns = []
        
        # Turn 0
        turn_0_events = [{
            "author": "user",
            "content": {
                "role": "user",
                "parts": [{"text": prompt_text}]
            }
        }]
        for event in events:
            mapped = map_adk_event_to_agent_event(event)
            if mapped:
                turn_0_events.append(mapped)
            
        turns.append({
            "turn_index": 0,
            "events": turn_0_events
        })
        
        # Turn 1
        if is_interrupted:
            turn_1_events = [{
                "author": "user",
                "content": {
                    "role": "user",
                    "parts": [{"text": decision}]
                }
            }]
            for event in resume_events:
                mapped = map_adk_event_to_agent_event(event)
                if mapped:
                    turn_1_events.append(mapped)
                
            turns.append({
                "turn_index": 1,
                "events": turn_1_events
            })
            
        generated_cases.append({
            "eval_case_id": case_id,
            "agent_data": {
                "agents": {
                    "expense_approval": {
                        "agent_id": "expense_approval",
                        "instruction": "Ambient Expense Approval workflow"
                    }
                },
                "turns": turns
            }
        })
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"eval_cases": generated_cases}, f, indent=2)
        
    print(f"Traces successfully generated and saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
