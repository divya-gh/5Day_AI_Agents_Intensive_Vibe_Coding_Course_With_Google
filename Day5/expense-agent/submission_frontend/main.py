import os
import logging
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manager-dashboard")

app = FastAPI(title="Expense Manager Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or "divya-doc-pipeline"
AGENT_RUNTIME_ID = os.environ.get("AGENT_RUNTIME_ID") or "4416447937706459136"
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-east1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize ADK Session Service
session_service = VertexAiSessionService(
    project=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_RUNTIME_ID
)

# Load the Agent Engine
try:
    agent_engine = agent_engines.get(
        f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_RUNTIME_ID}"
    )
    logger.info(f"Loaded Agent Engine: {AGENT_RUNTIME_ID}")
except Exception as e:
    logger.error(f"Failed to load reasoning engine: {e}")
    agent_engine = None


class ActionRequest(BaseModel):
    approved: bool
    interrupt_id: str
    user_id: Optional[str] = "default-user"


@app.get("/api/pending")
async def get_pending_approvals():
    if not AGENT_RUNTIME_ID:
        raise HTTPException(status_code=500, detail="AGENT_RUNTIME_ID not configured")
    
    try:
        # 1. List all sessions
        list_resp = await session_service.list_sessions(app_name=AGENT_RUNTIME_ID)
        sessions = list_resp.sessions
        
        pending_list = []
        
        # 2. Iterate and check history of each session
        for s in sessions:
            try:
                full_session = await session_service.get_session(
                    app_name=AGENT_RUNTIME_ID,
                    user_id=s.user_id,
                    session_id=s.id
                )
                if not full_session:
                    continue
                
                # Check for unresolved adk_request_input function calls
                # Track request input function calls (by ID) and matching responses (by ID)
                calls = {}
                responses = set()
                
                for ev in full_session.events:
                    if ev.content and ev.content.parts:
                        for part in ev.content.parts:
                            if part.function_call and part.function_call.name == "adk_request_input":
                                # Save call details
                                calls[part.function_call.id] = {
                                    "id": part.function_call.id,
                                    "message": part.function_call.args.get("message") if part.function_call.args else None,
                                    "timestamp": ev.timestamp
                                }
                            elif part.function_response and part.function_response.name == "adk_request_input":
                                responses.add(part.function_response.id)
                
                # Find unresolved
                unresolved_ids = set(calls.keys()) - responses
                
                for uid in unresolved_ids:
                    # Get expense payload details from state
                    expense_payload = full_session.state.get("expense") or {}
                    
                    pending_list.append({
                        "session_id": s.id,
                        "user_id": s.user_id,
                        "interrupt_id": uid,
                        "message": calls[uid]["message"],
                        "expense": expense_payload,
                        "timestamp": calls[uid]["timestamp"]
                    })
            except Exception as se:
                logger.error(f"Error fetching session {s.id}: {se}")
                continue
                
        return pending_list
    except Exception as e:
        logger.error(f"Error listing pending approvals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/action/{session_id}")
async def take_action(session_id: str, req: ActionRequest):
    if not agent_engine:
        raise HTTPException(status_code=500, detail="Agent Runtime is not loaded")
    
    try:
        # Resolve target user_id. We must match the session's actual owner.
        user_id = req.user_id or "default-user"
        
        # Build resume payload
        message_payload = {
            "role": "user",
            "parts": [
                {
                    "function_response": {
                        "id": req.interrupt_id,
                        "name": "adk_request_input",
                        "response": {
                            "approved": req.approved,
                            "response": "yes" if req.approved else "no"
                        }
                    }
                }
            ]
        }
        
        # Execute stream_query
        events = []
        for event in agent_engine.stream_query(
            message=message_payload,
            user_id=user_id,
            session_id=session_id
        ):
            events.append(event)
            
        # Parse events to find final output / compliance review
        final_review = None
        for ev in reversed(events):
            if ev.get("output") is not None:
                final_review = ev.get("output")
                break
                
        return {
            "status": "success",
            "final_review": final_review,
            "events": events
        }
    except Exception as e:
        logger.error(f"Error taking action on session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expense Compliance Control Hub</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-color: #0b0c16;
                --card-bg: rgba(20, 24, 43, 0.45);
                --card-border: rgba(255, 255, 255, 0.08);
                --glow-primary: rgba(138, 75, 255, 0.4);
                --glow-approve: rgba(0, 240, 150, 0.4);
                --glow-reject: rgba(255, 80, 80, 0.4);
                --text-main: #f3f4f6;
                --text-muted: #9ca3af;
                --accent-approve: #00f096;
                --accent-reject: #ff5050;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg-color);
                color: var(--text-main);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                overflow-x: hidden;
                position: relative;
            }

            /* Sleek background radial glows */
            body::before {
                content: '';
                position: absolute;
                width: 600px;
                height: 600px;
                top: -100px;
                left: -100px;
                background: radial-gradient(circle, var(--glow-primary) 0%, transparent 70%);
                z-index: -1;
                pointer-events: none;
            }

            body::after {
                content: '';
                position: absolute;
                width: 800px;
                height: 800px;
                bottom: -200px;
                right: -200px;
                background: radial-gradient(circle, rgba(75, 140, 255, 0.25) 0%, transparent 70%);
                z-index: -1;
                pointer-events: none;
            }

            header {
                padding: 2.5rem 2rem;
                max-width: 1200px;
                width: 100%;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }

            .logo-section h1 {
                font-weight: 800;
                font-size: 2.2rem;
                letter-spacing: -0.5px;
                background: linear-gradient(135deg, #fff 0%, #a78bfa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .logo-section p {
                font-size: 0.95rem;
                color: var(--text-muted);
                margin-top: 0.25rem;
            }

            .header-actions {
                display: flex;
                gap: 1rem;
            }

            button.btn-refresh {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid var(--card-border);
                color: var(--text-main);
                padding: 0.75rem 1.25rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.9rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(10px);
            }

            button.btn-refresh:hover {
                background: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.2);
                transform: translateY(-2px);
            }

            main {
                flex: 1;
                max-width: 1200px;
                width: 100%;
                margin: 0 auto;
                padding: 3rem 2rem;
            }

            .section-title {
                font-size: 1.4rem;
                font-weight: 600;
                margin-bottom: 2rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }

            .badge {
                background: rgba(138, 75, 255, 0.2);
                color: #c084fc;
                border: 1px solid rgba(138, 75, 255, 0.3);
                padding: 0.2rem 0.6rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
            }

            /* Grid Layout */
            .cards-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
                gap: 2rem;
            }

            /* Glassmorphic Card */
            .card {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 20px;
                padding: 2rem;
                backdrop-filter: blur(16px) saturate(180%);
                -webkit-backdrop-filter: blur(16px) saturate(180%);
                display: flex;
                flex-direction: column;
                position: relative;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                overflow: hidden;
            }

            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #8b5cf6, #3b82f6);
                opacity: 0.7;
            }

            .card:hover {
                transform: translateY(-6px) scale(1.01);
                border-color: rgba(138, 75, 255, 0.3);
                box-shadow: 0 12px 30px rgba(138, 75, 255, 0.15);
            }

            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 1.5rem;
            }

            .session-id {
                font-family: monospace;
                font-size: 0.8rem;
                color: var(--text-muted);
                background: rgba(255, 255, 255, 0.05);
                padding: 0.25rem 0.5rem;
                border-radius: 6px;
            }

            .amount-tag {
                font-size: 2rem;
                font-weight: 800;
                color: #fff;
                background: linear-gradient(135deg, #fff 60%, #93c5fd 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .card-details {
                flex: 1;
                margin-bottom: 2rem;
            }

            .merchant {
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #fff;
            }

            .description {
                font-size: 0.95rem;
                color: var(--text-muted);
                line-height: 1.5;
                margin-bottom: 1.25rem;
            }

            .prompt-message {
                font-size: 0.9rem;
                background: rgba(255, 255, 255, 0.03);
                border-left: 3px solid #8b5cf6;
                padding: 0.75rem 1rem;
                border-radius: 0 10px 10px 0;
                color: #e5e7eb;
                font-style: italic;
            }

            .card-actions {
                display: flex;
                gap: 1rem;
            }

            .btn {
                flex: 1;
                padding: 0.85rem;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            }

            .btn-approve {
                background: rgba(0, 240, 150, 0.15);
                color: var(--accent-approve);
                border: 1px solid rgba(0, 240, 150, 0.2);
            }

            .btn-approve:hover:not(:disabled) {
                background: var(--accent-approve);
                color: #000;
                box-shadow: 0 0 20px var(--glow-approve);
                transform: translateY(-2px);
            }

            .btn-reject {
                background: rgba(255, 80, 80, 0.15);
                color: var(--accent-reject);
                border: 1px solid rgba(255, 80, 80, 0.2);
            }

            .btn-reject:hover:not(:disabled) {
                background: var(--accent-reject);
                color: #fff;
                box-shadow: 0 0 20px var(--glow-reject);
                transform: translateY(-2px);
            }

            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            /* Slide-out Panel / Modal */
            .sidebar {
                position: fixed;
                top: 0;
                right: -460px;
                width: 440px;
                height: 100vh;
                background: rgba(13, 16, 33, 0.95);
                border-left: 1px solid var(--card-border);
                box-shadow: -20px 0 40px rgba(0, 0, 0, 0.6);
                z-index: 1000;
                backdrop-filter: blur(25px);
                transition: right 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                flex-direction: column;
            }

            .sidebar.open {
                right: 0;
            }

            .sidebar-header {
                padding: 2rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .sidebar-header h2 {
                font-weight: 700;
                font-size: 1.4rem;
            }

            .btn-close {
                background: none;
                border: none;
                color: var(--text-muted);
                font-size: 1.5rem;
                cursor: pointer;
                transition: color 0.2s;
            }

            .btn-close:hover {
                color: #fff;
            }

            .sidebar-content {
                padding: 2rem;
                flex: 1;
                overflow-y: auto;
            }

            .result-status {
                display: inline-block;
                padding: 0.5rem 1rem;
                border-radius: 10px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 1.5rem;
            }

            .result-status.approved {
                background: rgba(0, 240, 150, 0.2);
                color: var(--accent-approve);
                border: 1px solid rgba(0, 240, 150, 0.3);
            }

            .result-status.rejected {
                background: rgba(255, 80, 80, 0.2);
                color: var(--accent-reject);
                border: 1px solid rgba(255, 80, 80, 0.3);
            }

            .review-section {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid var(--card-border);
                border-radius: 14px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }

            .review-label {
                font-size: 0.8rem;
                color: var(--text-muted);
                text-transform: uppercase;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }

            .review-value {
                font-size: 1.05rem;
                line-height: 1.6;
                color: var(--text-main);
            }

            .no-pending {
                grid-column: 1 / -1;
                text-align: center;
                padding: 4rem 2rem;
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 20px;
                backdrop-filter: blur(16px);
            }

            .no-pending h3 {
                font-size: 1.3rem;
                margin-bottom: 0.5rem;
            }

            .no-pending p {
                color: var(--text-muted);
            }

            /* Loading spinner */
            .spinner {
                width: 1.25rem;
                height: 1.25rem;
                border: 2px solid currentColor;
                border-top-color: transparent;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <header>
            <div class="logo-section">
                <h1>Hub</h1>
                <p>Expense Compliance Control Dashboard</p>
            </div>
            <div class="header-actions">
                <button class="btn-refresh" onclick="loadPending()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                    Refresh
                </button>
            </div>
        </header>

        <main>
            <div class="section-title">
                <span>Pending Compliance Approvals</span>
                <span class="badge" id="pending-count">0</span>
            </div>

            <div class="cards-grid" id="cards-container">
                <div class="no-pending">
                    <h3>Loading items...</h3>
                </div>
            </div>
        </main>

        <!-- Slide out panel -->
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h2>Compliance Decision Results</h2>
                <button class="btn-close" onclick="closeSidebar()">&times;</button>
            </div>
            <div class="sidebar-content" id="sidebar-content">
                <!-- Content injected dynamically -->
            </div>
        </div>

        <script>
            async function loadPending() {
                const container = document.getElementById('cards-container');
                const badge = document.getElementById('pending-count');
                
                try {
                    const response = await fetch('/api/pending');
                    const data = await response.json();
                    
                    badge.innerText = data.length;
                    
                    if (data.length === 0) {
                        container.innerHTML = `
                            <div class="no-pending">
                                <h3>All caught up!</h3>
                                <p>No pending expenses require manual compliance review at this time.</p>
                            </div>
                        `;
                        return;
                    }
                    
                    container.innerHTML = '';
                    data.forEach(item => {
                        const amount = item.expense.amount !== undefined ? item.expense.amount : 0.0;
                        const merchant = item.expense.merchant || 'Unknown Merchant';
                        const description = item.expense.description || 'No description provided';
                        
                        const card = document.createElement('div');
                        card.className = 'card';
                        card.id = `card-${item.session_id}`;
                        card.innerHTML = `
                            <div class="card-header">
                                <span class="session-id">ID: ${item.session_id.substring(0, 12)}...</span>
                                <span class="amount-tag">$${parseFloat(amount).toFixed(2)}</span>
                            </div>
                            <div class="card-details">
                                <h3 class="merchant">${merchant}</h3>
                                <p class="description">${description}</p>
                                <p class="prompt-message">${item.message}</p>
                            </div>
                            <div class="card-actions">
                                <button class="btn btn-approve" onclick="takeAction('${item.session_id}', '${item.interrupt_id}', true, '${item.user_id}', this)">
                                    Approve
                                </button>
                                <button class="btn btn-reject" onclick="takeAction('${item.session_id}', '${item.interrupt_id}', false, '${item.user_id}', this)">
                                    Reject
                                </button>
                            </div>
                        `;
                        container.appendChild(card);
                    });
                } catch (e) {
                    container.innerHTML = `
                        <div class="no-pending" style="border-color: var(--accent-reject);">
                            <h3 style="color: var(--accent-reject);">Failed to fetch pending items</h3>
                            <p>${e.message}</p>
                        </div>
                    `;
                }
            }

            async function takeAction(sessionId, interruptId, approved, userId, button) {
                const card = document.getElementById(`card-${sessionId}`);
                const actionsDiv = card.querySelector('.card-actions');
                const originalContent = actionsDiv.innerHTML;
                
                // Disable interface
                actionsDiv.innerHTML = `<div style="display:flex; justify-content:center; width:100%; color:var(--text-muted);"><div class="spinner"></div></div>`;
                
                try {
                    const response = await fetch(`/api/action/${sessionId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ approved, interrupt_id: interruptId, user_id: userId })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        // Remove card
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            card.remove();
                            loadPending();
                        }, 400);
                        
                        // Open sidebar with review details
                        openSidebar(data.final_review);
                    } else {
                        throw new Error('Action execution failed');
                    }
                } catch (e) {
                    alert(`Error: ${e.message}`);
                    actionsDiv.innerHTML = originalContent;
                }
            }

            function openSidebar(review) {
                const sidebar = document.getElementById('sidebar');
                const content = document.getElementById('sidebar-content');
                
                if (!review) {
                    content.innerHTML = `
                        <div class="review-section">
                            <div class="review-label">Compliance Decision</div>
                            <div class="review-value">Decision accepted, but no final evaluation returned. Check agent logs.</div>
                        </div>
                    `;
                } else {
                    const statusClass = review.status.toLowerCase() === 'approved' ? 'approved' : 'rejected';
                    content.innerHTML = `
                        <div class="result-status ${statusClass}">${review.status}</div>
                        
                        <div class="review-section">
                            <div class="review-label">Transaction Amount</div>
                            <div class="review-value" style="font-size: 1.5rem; font-weight: 700;">$${parseFloat(review.amount).toFixed(2)}</div>
                        </div>
                        
                        <div class="review-section">
                            <div class="review-label">Compliance Review Notes</div>
                            <div class="review-value">${review.reason}</div>
                        </div>
                    `;
                }
                
                sidebar.classList.add('open');
            }

            function closeSidebar() {
                document.getElementById('sidebar').classList.remove('open');
            }

            // Initial load
            window.addEventListener('DOMContentLoaded', loadPending);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
