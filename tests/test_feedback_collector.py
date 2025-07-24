"""
Tests for FeedbackCollector.
"""
import pytest
from unittest.mock import MagicMock, patch
import os

from tdev.monitoring.feedback import FeedbackCollector

class TestFeedbackCollector:
    """Test the Feedback Collector."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.collector = FeedbackCollector()
    
    def test_collect_feedback_success(self):
        """Test successful feedback collection."""
        feedback_data = {
            "agent_name": "TestAgent",
            "rating": 5,
            "comment": "Great agent!",
            "source": "test"
        }
        
        result = self.collector.collect(feedback_data)
        
        assert result["success"] is True
        assert "message" in result
    
    def test_collect_feedback_missing_agent(self):
        """Test feedback collection with missing agent name."""
        feedback_data = {
            "rating": 5,
            "comment": "Great!",
            "source": "test"
        }
        
        result = self.collector.collect(feedback_data)
        
        assert result["success"] is False
        assert "agent_name is required" in result["error"]
    
    def test_collect_feedback_invalid_rating(self):
        """Test feedback collection with invalid rating."""
        feedback_data = {
            "agent_name": "TestAgent",
            "rating": 10,  # Invalid rating (should be 1-5)
            "comment": "Great!",
            "source": "test"
        }
        
        result = self.collector.collect(feedback_data)
        
        assert result["success"] is False
        assert "Rating must be between 1 and 5" in result["error"]
    
    def test_get_feedback_success(self):
        """Test getting feedback for an agent."""
        # First collect some feedback
        feedback_data = {
            "agent_name": "TestAgent",
            "rating": 4,
            "comment": "Good agent",
            "source": "test"
        }
        self.collector.collect(feedback_data)
        
        result = self.collector.get_feedback("TestAgent", 10)
        
        assert result["success"] is True
        assert "feedback" in result
        assert len(result["feedback"]) > 0
    
    def test_get_feedback_no_data(self):
        """Test getting feedback when no data exists."""
        result = self.collector.get_feedback("NonExistentAgent", 10)
        
        assert result["success"] is True
        assert result["feedback"] == []
    
    def test_get_agent_stats(self):
        """Test getting agent statistics."""
        # Collect multiple feedback entries
        feedback_entries = [
            {"agent_name": "TestAgent", "rating": 5, "source": "test"},
            {"agent_name": "TestAgent", "rating": 4, "source": "test"},
            {"agent_name": "TestAgent", "rating": 3, "source": "test"}
        ]
        
        for feedback in feedback_entries:
            self.collector.collect(feedback)
        
        stats = self.collector.get_agent_stats("TestAgent")
        
        assert stats["success"] is True
        assert stats["total_feedback"] == 3
        assert stats["average_rating"] == 4.0
        assert stats["rating_distribution"]["5"] == 1
        assert stats["rating_distribution"]["4"] == 1
        assert stats["rating_distribution"]["3"] == 1
    
    def test_get_agent_stats_no_data(self):
        """Test getting stats when no feedback exists."""
        stats = self.collector.get_agent_stats("NonExistentAgent")
        
        assert stats["success"] is True
        assert stats["total_feedback"] == 0
        assert stats["average_rating"] == 0
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token", "GITHUB_REPO": "test/repo"})
    @patch('tdev.monitoring.feedback.requests.post')
    def test_create_github_issue_success(self, mock_post):
        """Test creating GitHub issue for negative feedback."""
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"number": 123}
        
        feedback_data = {
            "agent_name": "TestAgent",
            "rating": 1,
            "comment": "This agent is broken",
            "source": "test"
        }
        
        result = self.collector.collect(feedback_data)
        
        assert result["success"] is True
        mock_post.assert_called_once()
    
    def test_create_github_issue_no_config(self):
        """Test GitHub issue creation without configuration."""
        # Ensure no GitHub config
        with patch.dict(os.environ, {}, clear=True):
            feedback_data = {
                "agent_name": "TestAgent",
                "rating": 1,
                "comment": "This agent is broken",
                "source": "test"
            }
            
            result = self.collector.collect(feedback_data)
            
            # Should still succeed even without GitHub config
            assert result["success"] is True