"""
Tests for the API server.
"""
import os
import json
import unittest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from tdev.api.server import app
from tdev.core.registry import get_registry

class TestAPIServer(unittest.TestCase):
    """Test the API server."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create proper mock registry with all required methods
        self.mock_registry = MagicMock()
        self.mock_registry.get.return_value = {"name": "PlannerAgent", "type": "agent"}
        self.mock_registry.get_by_type.return_value = [
            {"name": "Agent1", "type": "agent"},
            {"name": "Agent2", "type": "agent"}
        ]
        
        # Patch get_registry to return our mock
        self.registry_patcher = patch('tdev.api.server.get_registry')
        self.mock_get_registry = self.registry_patcher.start()
        self.mock_get_registry.return_value = self.mock_registry
        
        # Mock the coordinator
        self.coordinator_patcher = patch('tdev.api.server.DevCoordinatorAgent')
        self.mock_coordinator_class = self.coordinator_patcher.start()
        self.mock_coordinator = MagicMock()
        self.mock_coordinator_class.return_value = self.mock_coordinator
        
        # Mock the feedback collector
        self.feedback_patcher = patch('tdev.api.server.FeedbackCollector')
        self.mock_feedback_class = self.feedback_patcher.start()
        self.mock_feedback = MagicMock()
        self.mock_feedback_class.return_value = self.mock_feedback
        
        # Create test client after all patches are set up
        self.client = TestClient(app)
    
    def tearDown(self):
        """Clean up the test environment."""
        self.registry_patcher.stop()
        self.coordinator_patcher.stop()
        self.feedback_patcher.stop()
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
    
    def test_list_agents(self):
        """Test the list_agents endpoint."""
        # Make request
        response = self.client.get("/agents")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("agents", data)
        self.assertEqual(len(data["agents"]), 2)
        self.assertEqual(data["agents"][0]["name"], "Agent1")
        self.assertEqual(data["agents"][1]["name"], "Agent2")
        
        # Check that registry was called correctly
        self.mock_registry.get_by_type.assert_called_once_with("agent")
    
    def test_orchestrate(self):
        """Test the orchestrate endpoint."""
        # Configure mock coordinator
        self.mock_coordinator.run.return_value = {
            "success": True,
            "result": "Test result",
            "workflow_id": "test-workflow"
        }
        
        # Make request
        response = self.client.post(
            "/orchestrate",
            json={"goal": "Test goal", "options": {"key": "value"}}
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["result"], "Test result")
        self.assertEqual(data["workflow_id"], "test-workflow")
        
        # Check that coordinator was called correctly
        self.mock_coordinator.run.assert_called_once_with({
            "goal": "Test goal",
            "options": {"key": "value"}
        })
    
    def test_orchestrate_failure(self):
        """Test the orchestrate endpoint with a failure."""
        # Configure mock coordinator
        self.mock_coordinator.run.return_value = {
            "success": False,
            "error": "Test error"
        }
        
        # Make request
        response = self.client.post(
            "/orchestrate",
            json={"goal": "Test goal"}
        )
        
        # Check response
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Test error")
    
    def test_classify(self):
        """Test the classify endpoint."""
        # Configure mock coordinator
        self.mock_coordinator.run.return_value = {
            "success": True,
            "result": {
                "type": "agent",
                "brain_count": 1
            }
        }
        
        # Make request
        response = self.client.post(
            "/classify",
            json={"code": "def test(): pass", "options": {}}
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["result"]["type"], "agent")
        self.assertEqual(data["result"]["brain_count"], 1)
        
        # Check that coordinator was called correctly
        self.mock_coordinator.run.assert_called_once_with({
            "code": "def test(): pass",
            "options": {}
        })
    
    def test_feedback(self):
        """Test the feedback endpoint."""
        # Configure mock feedback collector
        self.mock_feedback.collect.return_value = {
            "success": True
        }
        
        # Make request
        response = self.client.post(
            "/feedback",
            json={
                "agent_name": "TestAgent",
                "rating": 5,
                "comment": "Great agent!",
                "source": "test"
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        
        # Check that feedback collector was called correctly
        self.mock_feedback.collect.assert_called_once()
        args, kwargs = self.mock_feedback.collect.call_args
        self.assertEqual(args[0]["agent_name"], "TestAgent")
        self.assertEqual(args[0]["rating"], 5)
        self.assertEqual(args[0]["comment"], "Great agent!")
        self.assertEqual(args[0]["source"], "test")

if __name__ == '__main__':
    unittest.main()