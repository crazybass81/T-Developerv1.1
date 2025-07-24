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
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from tdev.core.registry import get_registry
from tdev.agents.dev_coordinator_agent import DevCoordinatorAgent
from tdev.monitoring.feedback import FeedbackCollector
from tdev.core.auth import auth_manager
from tdev.core.i18n import i18n
from tdev.core.versioning import version_manager

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

class VersionRequest(BaseModel):
    agent_name: str
    version: str
    action: str = "promote"  # promote, list, get

# Authentication dependency
security = HTTPBearer(auto_error=False)

def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current user from API key."""
    if not authorization:
        return None
    
    # Extract API key from Bearer token
    if authorization.startswith("Bearer "):
        api_key = authorization[7:]
    else:
        api_key = authorization
    
    return auth_manager.authenticate(api_key)

# For testing - simple dependency override
def get_test_user():
    """Test user for unit tests."""
    from tdev.core.auth import User
    return User(user_id="test", tenant_id="test", permissions={"read": True, "write": True})

# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "T-Developer API", "version": "1.1.0"}

@app.get("/agents")
async def list_agents(user=Depends(get_current_user), lang: str = "en"):
    """List all registered agents."""
    # Set language for responses
    i18n.set_language(lang)
    
    agents = registry.get_by_type("agent")
    
    # Filter by tenant if user is authenticated
    if user:
        # In a real implementation, filter by tenant_id
        pass
    
    return {"agents": agents, "message": i18n.translate("agents.listed", lang)}

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
async def orchestrate(request: OrchestrationRequest, user=Depends(get_current_user), lang: str = "en"):
    """Orchestrate a goal."""
    i18n.set_language(lang)
    
    # Check permissions
    if user and hasattr(user, 'permissions') and not auth_manager.check_permission(user, "write"):
        raise HTTPException(status_code=403, detail=i18n.translate("error.permission_denied", lang))
    
    result = coordinator.run({"goal": request.goal, "options": request.options or {}})
    if not result.get("success", False):
        error_msg = i18n.translate("orchestrate.failed", lang)
        raise HTTPException(status_code=400, detail=result.get("error", error_msg))
    
    result["message"] = i18n.translate("orchestrate.success", lang)
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
async def get_feedback(agent_name: str, limit: int = 100, user=Depends(get_current_user)):
    """Get feedback for an agent."""
    # Check permissions
    if user and hasattr(user, 'permissions') and not auth_manager.check_permission(user, "read"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    result = feedback_collector.get_feedback(agent_name, limit)
    if not result.get("success", False):
        raise HTTPException(status_code=404, detail=result.get("error", "Agent not found"))
    return result

@app.post("/agents/{agent_name}/versions")
async def manage_agent_version(agent_name: str, request: VersionRequest, user=Depends(get_current_user)):
    """Manage agent versions."""
    # Check permissions
    if user and hasattr(user, 'permissions') and not auth_manager.check_permission(user, "write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    if request.action == "promote":
        success = version_manager.promote_version(agent_name, request.version)
        if not success:
            raise HTTPException(status_code=404, detail="Version not found")
        return {"success": True, "message": f"Version {request.version} promoted to active"}
    
    elif request.action == "list":
        versions = version_manager.get_versions(agent_name)
        return {"versions": [v.__dict__ for v in versions]}
    
    elif request.action == "get":
        version = version_manager.get_active_version(agent_name)
        if not version:
            raise HTTPException(status_code=404, detail="No active version found")
        return {"version": version.__dict__}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

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

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.1.0"}

if __name__ == "__main__":
    start_server()