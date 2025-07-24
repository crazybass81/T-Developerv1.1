"""
Tests for the FeedbackCollector class.
"""
import os
import json
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

import boto3
import pytest

from tdev.monitoring.feedback import FeedbackCollector

class TestFeedbackCollector(unittest.TestCase):
    """Test the FeedbackCollector class."""
    
    @patch('boto3.resource')
    @patch('tdev.monitoring.feedback.get_registry')
    def setUp(self, mock_get_registry, mock_boto3_resource):
        """Set up the test environment."""
        # Mock registry
        self.mock_registry = MagicMock()
        mock_get_registry.return_value = self.mock_registry
        
        # Mock DynamoDB
        self.mock_dynamodb = MagicMock()
        mock_boto3_resource.return_value = self.mock_dynamodb
        
        # Create collector
        self.collector = FeedbackCollector()
    
    def test_collect(self):
        """Test collecting feedback."""
        # Configure mocks
        self.mock_registry.get.return_value = {
            "name": "TestAgent",
            "type": "agent",
            "feedback": []
        }
        
        # Mock DynamoDB table
        mock_table = MagicMock()
        self.mock_dynamodb.Table.return_value = mock_table
        
        # Collect feedback
        feedback_data = {
            "agent_name": "TestAgent",
            "rating": 4,
            "comment": "Good agent",
            "source": "test",
            "user_id": "test-user"
        }
        result = self.collector.collect(feedback_data)
        
        # Check result
        self.assertEqual(result["success"], True)
        
        # Check that registry was called (may be called multiple times)
        self.assertEqual(self.mock_registry.get.call_count, 2)
        self.mock_registry.update.assert_called_once()
        args, kwargs = self.mock_registry.update.call_args
        self.assertEqual(args[0], "TestAgent")
        self.assertEqual(len(args[1]["feedback"]), 1)
        self.assertEqual(args[1]["feedback"][0]["rating"], 4)
        self.assertEqual(args[1]["feedback"][0]["comment"], "Good agent")
        self.assertEqual(args[1]["feedback"][0]["source"], "test")
        self.assertEqual(args[1]["feedback"][0]["user_id"], "test-user")
        self.assertIn("timestamp", args[1]["feedback"][0])
        
        # Check that DynamoDB was updated
        self.mock_dynamodb.Table.assert_called_once_with(self.collector.table_name)
        mock_table.put_item.assert_called_once()
        args, kwargs = mock_table.put_item.call_args
        self.assertEqual(kwargs["Item"]["agent_name"], "TestAgent")
        self.assertEqual(kwargs["Item"]["rating"], 4)
        self.assertEqual(kwargs["Item"]["comment"], "Good agent")
        self.assertEqual(kwargs["Item"]["source"], "test")
        self.assertEqual(kwargs["Item"]["user_id"], "test-user")
        self.assertIn("timestamp", kwargs["Item"])
    
    def test_collect_missing_agent(self):
        """Test collecting feedback for a missing agent."""
        # Configure mocks
        self.mock_registry.get.return_value = None
        
        # Collect feedback
        feedback_data = {
            "agent_name": "MissingAgent",
            "rating": 4,
            "comment": "Good agent",
            "source": "test"
        }
        result = self.collector.collect(feedback_data)
        
        # Check result
        self.assertEqual(result["success"], False)
        self.assertIn("error", result)
        self.assertIn("MissingAgent", result["error"])
        
        # Check that registry was not updated
        self.mock_registry.update.assert_not_called()
    
    def test_collect_missing_agent_name(self):
        """Test collecting feedback without an agent name."""
        # Collect feedback
        feedback_data = {
            "rating": 4,
            "comment": "Good agent",
            "source": "test"
        }
        result = self.collector.collect(feedback_data)
        
        # Check result
        self.assertEqual(result["success"], False)
        self.assertIn("error", result)
        self.assertIn("required", result["error"])
        
        # Check that registry was not updated
        self.mock_registry.update.assert_not_called()
    
    @patch('requests.post')
    def test_create_issue(self, mock_requests_post):
        """Test creating an issue for low-rated feedback."""
        # Set environment variables
        os.environ["GITHUB_TOKEN"] = "test-token"
        os.environ["GITHUB_REPO"] = "test-user/test-repo"
        
        # Configure mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"html_url": "https://github.com/test-user/test-repo/issues/1"}
        mock_requests_post.return_value = mock_response
        
        # Create issue
        feedback_data = {
            "agent_name": "TestAgent",
            "rating": 2,
            "comment": "Bad agent",
            "source": "test",
            "timestamp": "2023-01-01T00:00:00"
        }
        self.collector._create_issue("TestAgent", feedback_data)
        
        # Check that requests.post was called correctly
        mock_requests_post.assert_called_once()
        args, kwargs = mock_requests_post.call_args
        self.assertEqual(args[0], "https://api.github.com/repos/test-user/test-repo/issues")
        self.assertEqual(kwargs["headers"]["Authorization"], "token test-token")
        self.assertEqual(kwargs["json"]["title"], "Low rating for TestAgent: 2/5")
        self.assertIn("Bad agent", kwargs["json"]["body"])
        self.assertIn("test", kwargs["json"]["body"])
        self.assertIn("2023-01-01T00:00:00", kwargs["json"]["body"])
        
        # Clean up
        del os.environ["GITHUB_TOKEN"]
        del os.environ["GITHUB_REPO"]
    
    def test_get_feedback(self):
        """Test getting feedback for an agent."""
        # Configure mocks
        self.mock_registry.get.return_value = {
            "name": "TestAgent",
            "type": "agent",
            "feedback": [
                {"rating": 4, "comment": "Good agent", "timestamp": "2023-01-01T00:00:00"},
                {"rating": 5, "comment": "Great agent", "timestamp": "2023-01-02T00:00:00"}
            ]
        }
        
        # Get feedback
        result = self.collector.get_feedback("TestAgent")
        
        # Check result
        self.assertEqual(result["success"], True)
        self.assertEqual(result["agent_name"], "TestAgent")
        self.assertEqual(len(result["feedback"]), 2)
        self.assertEqual(result["feedback"][0]["rating"], 4)
        self.assertEqual(result["feedback"][0]["comment"], "Good agent")
        self.assertEqual(result["feedback"][1]["rating"], 5)
        self.assertEqual(result["feedback"][1]["comment"], "Great agent")
        
        # Check that registry was queried correctly
        self.mock_registry.get.assert_called_once_with("TestAgent")
    
    def test_get_feedback_missing_agent(self):
        """Test getting feedback for a missing agent."""
        # Configure mocks
        self.mock_registry.get.return_value = None
        
        # Get feedback
        result = self.collector.get_feedback("MissingAgent")
        
        # Check result
        self.assertEqual(result["success"], False)
        self.assertIn("error", result)
        self.assertIn("MissingAgent", result["error"])
        
        # Check that registry was queried correctly
        self.mock_registry.get.assert_called_once_with("MissingAgent")
    
    def test_get_all_feedback(self):
        """Test getting feedback for all agents."""
        # Configure mocks
        self.mock_registry.get_all.return_value = {
            "Agent1": {
                "name": "Agent1",
                "type": "agent",
                "feedback": [
                    {"rating": 4, "comment": "Good agent", "timestamp": "2023-01-01T00:00:00"}
                ]
            },
            "Agent2": {
                "name": "Agent2",
                "type": "agent",
                "feedback": [
                    {"rating": 5, "comment": "Great agent", "timestamp": "2023-01-02T00:00:00"}
                ]
            },
            "Agent3": {
                "name": "Agent3",
                "type": "agent"
                # No feedback
            }
        }
        
        # Get feedback
        result = self.collector.get_feedback()
        
        # Check result
        self.assertEqual(result["success"], True)
        self.assertIn("feedback", result)
        self.assertEqual(len(result["feedback"]), 2)  # Only 2 agents have feedback
        self.assertEqual(len(result["feedback"]["Agent1"]), 1)
        self.assertEqual(result["feedback"]["Agent1"][0]["rating"], 4)
        self.assertEqual(len(result["feedback"]["Agent2"]), 1)
        self.assertEqual(result["feedback"]["Agent2"][0]["rating"], 5)
        
        # Check that registry was queried correctly
        self.mock_registry.get_all.assert_called_once()

if __name__ == '__main__':
    unittest.main()