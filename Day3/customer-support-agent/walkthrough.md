# Customer Support Agent Graph Workflow Walkthrough

We have successfully created and implemented the `customer-support-agent` graph workflow using ADK 2.0.

## Accomplishments

1. **Scaffolded Project**:
   - Initialized a minimal prototype ADK 2.0 project without deployment files:
     `agents-cli scaffold create customer-support-agent --agent adk --prototype -d none`
   - Configured `pyproject.toml` and `agents-cli-manifest.yaml` with the correct project details.

2. **Graph Workflow Architecture**:
   - Implemented the routing graph in [app/agent.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day3/customer-support-agent/app/agent.py):
     - **`START`** -> **`store_query`**: Extracts and stores original query text.
     - **`store_query`** -> **`classifier`**: An `LlmAgent` using a Pydantic schema to determine if the query is shipping-related.
     - **`classifier`** -> **`route_query`**: Evaluates the classification results and routes the flow.
     - **`route_query`** -- `"shipping"` -> **`faq_agent`**: An `LlmAgent` designed to politely answer shipping questions.
     - **`route_query`** -- `"unrelated"` -> **`decline_node`**: A custom `FunctionNode` that politely declines unrelated questions.

3. **Google AI Studio Authentication Support**:
   - Removed Vertex AI defaults and configured [app/agent.py](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day3/customer-support-agent/app/agent.py) to read `GEMINI_API_KEY` from a local [.env](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day3/customer-support-agent/.env) file.
   - Created a template [.env](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day3/customer-support-agent/.env) in the project root containing a placeholder.

4. **Validation and Linting**:
   - Ran `agents-cli lint` and resolved all styling, formatting, and type-checking warnings. Type checking (`ty check`) and formatting (`ruff`) are completely clean.

## Next Steps

> [!IMPORTANT]
> Since we are using Google AI Studio Developer API for local testing:
> 1. Open the [.env](file:///c:/Users/divya/OneDrive/Desktop/Learn/AI/Agent%20AI/Google%205Day%20Intensive%20Vibe%20Coding/5Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/Day3/customer-support-agent/.env) file in your workspace.
> 2. Replace `YOUR_GEMINI_API_KEY` with your actual Google AI Studio API key.
> 3. Run `agents-cli run "What are the rates to ship a package to Canada?"` to test shipping-related routing.
> 4. Run `agents-cli run "Who won the 2022 world cup?"` to test decline routing.
