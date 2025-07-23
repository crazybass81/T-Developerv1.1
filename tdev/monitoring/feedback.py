"""
Feedback collection and processing for T-Developer.

This module provides functionality for collecting and processing user feedback
for continuous improvement of agents.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

import boto3
import requests

from tdev.core.registry import get_registry

class FeedbackCollector:
    """Collector for user feedback on agents."""
    
    def __init__(self):
        """Initialize the FeedbackCollector."""
        self.registry = get_registry()
        self.dynamodb = boto3.resource("dynamodb")
        self.table_name = os.environ.get("FEEDBACK_TABLE", "t-developer-feedback")
    
    def collect(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect feedback for an agent.
        
        Args:
            feedback_data: Feedback data
                - agent_name: Name of the agent
                - rating: Numeric rating (1-5)
                - comment: Optional comment
                - source: Source of the feedback (e.g., "ui", "slack")
                - user_id: Optional user identifier
                
        Returns:
            Result of feedback collection
        """
        agent_name = feedback_data.get("agent_name")
        if not agent_name:
            return {"success": False, "error": "Agent name is required"}
        
        # Get agent from registry
        agent_meta = self.registry.get(agent_name)  # type: ignore[attr-defined]
        if not agent_meta:
            return {"success": False, "error": f"Agent {agent_name} not found"}
        
        # Add timestamp to feedback
        feedback_data["timestamp"] = datetime.now().isoformat()
        
        # Store feedback in registry
        self._store_in_registry(agent_name, feedback_data)
        
        # Store feedback in DynamoDB (if available)
        try:
            self._store_in_dynamodb(feedback_data)
        except Exception as e:
            print(f"Warning: Could not store feedback in DynamoDB: {e}")
        
        # Create issue for low ratings
        rating = feedback_data.get("rating", 0)
        if rating <= 2:
            self._create_issue(agent_name, feedback_data)
        
        return {"success": True}
    
    def _store_in_registry(self, agent_name: str, feedback_data: Dict[str, Any]) -> None:
        """
        Store feedback in the registry.
        
        Args:
            agent_name: Name of the agent
            feedback_data: Feedback data
        """
        agent_meta = self.registry.get(agent_name)  # type: ignore[attr-defined]
        
        # Initialize feedback list if not exists
        if "feedback" not in agent_meta:
            agent_meta["feedback"] = []
        
        # Add feedback to agent metadata
        agent_meta["feedback"].append(feedback_data)
        
        # Limit feedback list size
        if len(agent_meta["feedback"]) > 100:
            agent_meta["feedback"] = agent_meta["feedback"][-100:]
        
        # Update registry
        self.registry.update(agent_name, agent_meta)  # type: ignore[attr-defined]  # type: ignore[attr-defined]
    
    def _store_in_dynamodb(self, feedback_data: Dict[str, Any]) -> None:
        """
        Store feedback in DynamoDB.
        
        Args:
            feedback_data: Feedback data
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            table.put_item(Item=feedback_data)
        except Exception as e:
            # If table doesn't exist, create it
            if "ResourceNotFoundException" in str(e):
                self._create_feedback_table()
                table = self.dynamodb.Table(self.table_name)
                table.put_item(Item=feedback_data)
            else:
                raise e
    
    def _create_feedback_table(self) -> None:
        """Create the feedback table in DynamoDB."""
        self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {"AttributeName": "agent_name", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "agent_name", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
    
    def _create_issue(self, agent_name: str, feedback_data: Dict[str, Any]) -> None:
        """
        Create an issue for low-rated feedback.
        
        Args:
            agent_name: Name of the agent
            feedback_data: Feedback data
        """
        # Get GitHub token and repo from environment
        github_token = os.environ.get("GITHUB_TOKEN")
        github_repo = os.environ.get("GITHUB_REPO")
        
        if not github_token or not github_repo:
            print("Warning: GitHub token or repo not set, skipping issue creation")
            return
        
        # Create issue title and body
        title = f"Low rating for {agent_name}: {feedback_data.get('rating')}/5"
        body = f"""
## Feedback for {agent_name}

- **Rating:** {feedback_data.get('rating')}/5
- **Comment:** {feedback_data.get('comment', 'No comment')}
- **Source:** {feedback_data.get('source', 'Unknown')}
- **Timestamp:** {feedback_data.get('timestamp')}
- **User ID:** {feedback_data.get('user_id', 'Anonymous')}

### Action Required

Please review this agent's behavior and improve it based on the feedback.
"""
        
        # Create issue via GitHub API
        url = f"https://api.github.com/repos/{github_repo}/issues"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "body": body,
            "labels": ["feedback", "improvement", "low-rating"]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Created GitHub issue: {response.json().get('html_url')}")
        except Exception as e:
            print(f"Error creating GitHub issue: {e}")
    
    def get_feedback(self, agent_name: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get feedback for an agent or all agents.
        
        Args:
            agent_name: Optional name of the agent
            limit: Maximum number of feedback items to return
            
        Returns:
            Dictionary of feedback items
        """
        if agent_name:
            # Get feedback for a specific agent
            agent_meta = self.registry.get(agent_name)  # type: ignore[attr-defined]
            if not agent_meta:
                return {"success": False, "error": f"Agent {agent_name} not found"}
            
            feedback = agent_meta.get("feedback", [])
            return {
                "success": True,
                "agent_name": agent_name,
                "feedback": feedback[-limit:] if limit < len(feedback) else feedback
            }
            
        # Get feedback for all agents
        all_feedback = {}
        for name, meta in self.registry.get_all().items():  # type: ignore[attr-defined]
            feedback = meta.get("feedback", [])
            if feedback:
                all_feedback[name] = feedback[-limit:] if limit < len(feedback) else feedback
        
        return {
            "success": True,
            "feedback": all_feedback
        }