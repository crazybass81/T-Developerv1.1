"""Tests for MetaAgent."""
import unittest
from unittest.mock import MagicMock, patch
from tdev.agents.meta_agent import MetaAgent

class TestMetaAgent(unittest.TestCase):
    """Test MetaAgent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.meta_agent = MetaAgent()
    
    def test_init(self):
        """Test MetaAgent initialization."""
        self.assertIsNotNone(self.meta_agent)
        self.assertEqual(self.meta_agent.name, "MetaAgent")
    
    @patch('tdev.agents.meta_agent.get_registry')
    def test_run_basic(self, mock_registry):
        """Test basic MetaAgent run."""
        mock_registry.return_value.get_all.return_value = {}
        
        result = self.meta_agent.run({"goal": "test goal"})
        
        self.assertIsInstance(result, dict)
        self.assertIn("result", result)
    
    @patch('tdev.agents.meta_agent.get_registry')
    def test_coordinate_agents(self, mock_registry):
        """Test agent coordination."""
        mock_registry.return_value.get_all.return_value = {
            "TestAgent": {"type": "agent", "name": "TestAgent"}
        }
        
        result = self.meta_agent.coordinate_agents("test goal")
        
        self.assertIsInstance(result, dict)
    
    def test_analyze_goal(self):
        """Test goal analysis."""
        result = self.meta_agent.analyze_goal("Create a simple echo function")
        
        self.assertIsInstance(result, dict)
        self.assertIn("complexity", result)
        self.assertIn("domain", result)