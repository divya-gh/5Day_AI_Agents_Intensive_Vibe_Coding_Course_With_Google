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
import json
import logging

from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from app.app_utils.telemetry import setup_telemetry
from app.app_utils.typing import Feedback

# Configure standard Python logging for console logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

class LocalLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def log_struct(self, info: dict, severity: str = "INFO"):
        level = getattr(logging, severity, logging.INFO)
        self.logger.log(level, f"JSON: {json.dumps(info)}")

logger = LocalLogger("ambient_expense_agent")

# Set up local telemetry config
setup_telemetry()

allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
session_service_uri = None
artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

# Construct FastAPI app via ADK
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=False,  # Disable cloud telemetry for local runs
    trigger_sources=["pubsub"],  # Register Pub/Sub trigger endpoints
)
app.title = "ambient-expense-agent"
app.description = "API for interacting with the Agent ambient-expense-agent"


# ── Custom ASGI Middleware for Pub/Sub Subscription Normalization ──
class PubSubNormalizationMiddleware:
    """Normalizes fully-qualified Pub/Sub subscription paths to short names.
    
    E.g. "projects/my-project/subscriptions/my-subscription" -> "my-subscription"
    This keeps the generated session IDs and records readable in the UI / logs.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and "trigger/pubsub" in scope["path"]:
            async def receive_with_normalization():
                message = await receive()
                if message["type"] == "http.request":
                    body = message.get("body", b"")
                    if body:
                        try:
                            data = json.loads(body)
                            if "subscription" in data and data["subscription"]:
                                sub = data["subscription"]
                                if "/" in sub:
                                    # Extract the last path segment (short name)
                                    short_name = sub.split("/")[-1]
                                    data["subscription"] = short_name
                                    logging.info(f"Normalized subscription path '{sub}' to '{short_name}'")
                                message["body"] = json.dumps(data).encode("utf-8")
                        except Exception as e:
                            logging.warning(f"Failed to parse or normalize trigger body: {e}")
                return message
            await self.app(scope, receive_with_normalization, send)
        else:
            await self.app(scope, receive, send)

# Register normalization middleware
app.add_middleware(PubSubNormalizationMiddleware)


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}


# Main execution serving on port 8080
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
