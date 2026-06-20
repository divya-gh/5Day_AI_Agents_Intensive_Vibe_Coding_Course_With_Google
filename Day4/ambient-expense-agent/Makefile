# Ambient Expense Approval Agent - Management Makefile
# Compatible with GNU Make on Windows/Linux/macOS

.PHONY: install playground run-service run-test generate-traces grade clean

install:
	@echo "Installing project dependencies using uv..."
	uv pip install -e .

playground:
	@echo "Starting ADK Playground UI..."
	agents-cli playground

run-service:
	@echo "Starting local FastAPI web service on port 8080..."
	uv run python -m app.fast_api_app

run-test:
	@echo "Submitting test expense payload to the agent..."
	agents-cli run --agent expense_agent --payload '{"amount": 150.0, "submitter": "alice@company.com", "category": "software", "description": "IDE License", "date": "2026-06-06"}'

generate-traces:
	@echo "Generating evaluation traces..."
	uv run python tests/eval/generate_traces.py

grade:
	@echo "Grading generated traces..."
	agents-cli eval grade --traces artifacts/traces/generated_traces.json --config tests/eval/eval_config.yaml

clean:
	@echo "Cleaning cache files..."
	if exist .pytest_cache rmdir /s /q .pytest_cache
	if exist .venv rmdir /s /q .venv
	if exist expense_agent\__pycache__ rmdir /s /q expense_agent\__pycache__
