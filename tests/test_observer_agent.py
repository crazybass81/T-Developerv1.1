"""Tests for ObserverAgent."""
import unittest
from unittest.mock import MagicMock, patch
from tdev.monitoring.observer import ObserverAgent

class TestObserverAgent(unittest.TestCase):
    """Test ObserverAgent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.observer = ObserverAgent()
    
    def test_init(self):
        """Test ObserverAgent initialization."""
        self.assertIsNotNone(self.observer)
        self.assertEqual(self.observer.name, "ObserverAgent")
    
    @patch('tdev.monitoring.observer.boto3')
    def test_collect_metrics(self, mock_boto3):
        """Test metrics collection."""
        mock_cloudwatch = MagicMock()
        mock_boto3.client.return_value = mock_cloudwatch
        
        result = self.observer.collect_metrics("TestAgent")
        
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
    
    def test_run_basic(self):
        """Test basic observer run."""
        result = self.observer.run({"action": "status", "agent_name": "TestAgent"})
        
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
    
    def test_get_agent_status(self):
        """Test agent status retrieval."""
        result = self.observer.get_agent_status("TestAgent")
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)