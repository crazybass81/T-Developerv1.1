"""
API server for T-Developer.

This module provides a FastAPI server for interacting with T-Developer
from web and chat interfaces.
"""
import os
import json
import asyncio
import uvicorn
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tdev.core.registry import get_registry
from tdev.agents.dev_coordinator_agent import DevCoordinatorAgent
from tdev.monitoring.feedback import FeedbackCollector

# Create FastAPI app
app = FastAPI(
    title="T-Developer API",
    description="API for interacting with T-Developer",
    version="1.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
registry = get_registry()
coordinator = DevCoordinatorAgent()
feedback_collector = FeedbackCollector()

# WebSocket connections
active_connections: Dict[str, WebSocket] = {}

# Models
class OrchestrationRequest(BaseModel):
    goal: str
    options: Optional[Dict[str, Any]] = None

class CodeRequest(BaseModel):
    code: str
    options: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    agent_name: str
    rating: int
    comment: Optional[str] = None
    source: str = "api"
    user_id: Optional[str] = None

# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "T-Developer API", "version": "1.1.0"}

@app.get("/agents")
async def list_agents():
    """List all registered agents."""
    agents = registry.get_by_type("agent")
    return {"agents": agents}

@app.get("/tools")
async def list_tools():
    """List all registered tools."""
    tools = registry.get_by_type("tool")
    return {"tools": tools}

@app.get("/teams")
async def list_teams():
    """List all registered teams."""
    teams = registry.get_by_type("team")
    return {"teams": teams}

@app.post("/orchestrate")
async def orchestrate(request: OrchestrationRequest):
    """Orchestrate a goal."""
    result = coordinator.run({"goal": request.goal, "options": request.options or {}})
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Orchestration failed"))
    return result

@app.post("/classify")
async def classify(request: CodeRequest):
    """Classify code."""
    result = coordinator.run({"code": request.code, "options": request.options or {}})
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Classification failed"))
    return result

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for an agent."""
    result = feedback_collector.collect(request.model_dump())
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to submit feedback"))
    return result

@app.get("/feedback/{agent_name}")
async def get_feedback(agent_name: str, limit: int = 100):
    """Get feedback for an agent."""
    result = feedback_collector.get_feedback(agent_name, limit)
    if not result.get("success", False):
        raise HTTPException(status_code=404, detail=result.get("error", "Agent not found"))
    return result

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections[client_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            
            # Handle different request types
            if "goal" in request:
                # Orchestrate a goal
                result = coordinator.run({"goal": request["goal"], "options": request.get("options", {})})
                await websocket.send_json(result)
            elif "code" in request:
                # Classify code
                result = coordinator.run({"code": request["code"], "options": request.get("options", {})})
                await websocket.send_json(result)
            else:
                await websocket.send_json({"error": "Invalid request"})
    
    except WebSocketDisconnect:
        del active_connections[client_id]

def start_server():
    """Start the API server."""
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

if __name__ == "__main__":
    start_server()