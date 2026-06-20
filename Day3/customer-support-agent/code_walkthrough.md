# Here is a walkthrough of the project structure and how app/agent.py is configured under the hood.

## 1. Project Structure Overview
The generated agent project directory consists of the following key files:

app/ : Holds the agent's core source code.

- init.py: Standard entry point that exposes the application instance app to the runner.

- agent.py: The main file where the model, schemas, nodes, edges, and root workflow are configured.

- fast_api_app.py: Serves the agent over HTTP (used during local playground execution).

- .env: Environment configuration file that houses your local credentials, specifically the GEMINI_API_KEY.

- pyproject.toml: Defines the project requirements (such as google-adk), Python versions, and developer toolchain configuration (ruff for formatting and ty for static type checking).

- agents-cli-manifest.yaml: Manifest file utilized by agents-cli to keep track of the template used (adk), session targets (in_memory), and general metadata.

## 2. Configuration of app/agent.py

**app/agent.py** is the heart of your graph workflow. It uses ADK 2.0's graph engine. 

Here is a breakdown of how it works:

### A. Model and Auth Initialization
The script first reads .env to load your GEMINI_API_KEY. It then instantiates the model 

wrapper: python
```
model = Gemini(
    model="gemini-2.5-flash",
    retry_options=types.HttpRetryOptions(attempts=3),
)
```
This model is shared by both LLM agents in our workflow.

### B. Structured Pydantic Schemas
We define the structure of our LLM classifier's output using Pydantic:
python
```
class Classification(BaseModel):
    is_shipping_related: bool = Field(
        description="True if the user's query is related to shipping (rates, tracking, delivery, returns). False otherwise."
    )
```
This forces the LLM to output a clean boolean JSON response, which avoids flaky text parsing downstream.

### C. Nodes (The Workhorses)
Nodes in ADK workflows can be LLM agents, tools, or plain Python functions.

**store_query:** A FunctionNode wrapped with the @node decorator. It captures the initial query text and saves it to the session state (ctx.state["user_query"]) so that later nodes can refer to it.
**classifier:** An LlmAgent node. It receives the query, runs prompt instructions, and uses the Classification Pydantic schema to validate and format the output.
**route_query:** A FunctionNode that inspects the classifier's output dictionary. 

It maps the decision to routing signals:
python
```
return Event(output=user_query, actions=EventActions(route=route))
```

**faq_agent:** A dedicated LlmAgent instructed to represent the company's shipping department and answer shipping inquiries.
**decline_node:** A FunctionNode that triggers for non-shipping queries, returning a polite boilerplate warning.

### D. Edges (The Connections)
Edges connect nodes together. For conditional routing, we use a dictionary mapping route strings to destination nodes:

python
```
edges = [
    ('START', store_query),                                            # 1. Entry point
    (store_query, classifier),                                         # 2. Extract and forward to classifier
    (classifier, route_query),                                         # 3. Process output and route
    (route_query, {"shipping": faq_agent, "unrelated": decline_node}), # 4. Conditional branches
]
```
If route_query returns an Event with route="shipping", the engine directs the flow to faq_agent. If it's route="unrelated", it goes to decline_node.

### E. Root Workflow
Finally, the Workflow class stitches the graph elements together:

python
```
root_agent = Workflow(
    name="customer_support_workflow",
    edges=edges,
)
app = App(
    root_agent=root_agent,
    name="customer-support-agent",
)
```
The App class is the entry point that packages this root agent, preparing it to be executed locally via the CLI or playground!

-------------------------------------------------------------------------
