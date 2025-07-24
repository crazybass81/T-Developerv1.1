"""
Integration tests for T-Developer workflow.
"""
import pytest
from unittest.mock import MagicMock, patch
from tdev.agents.dev_coordinator_agent import DevCoordinatorAgent
from tdev.agents.classifier_agent import ClassifierAgent
from tdev.agents.planner_agent import PlannerAgent

class TestIntegrationWorkflow:
    """Test end-to-end workflow integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_registry = MagicMock()
        self.mock_registry.get_by_type.return_value = [
            {"name": "EchoAgent", "type": "agent"},
            {"name": "ClassifierAgent", "type": "agent"}
        ]
        self.mock_registry.get_instance.return_value = MagicMock()
    
    @patch('tdev.agents.dev_coordinator_agent.get_registry')
    def test_full_workflow_code_classification(self, mock_get_registry):
        """Test full workflow: code input → classification → result."""
        mock_get_registry.return_value = self.mock_registry
        
        # Mock classifier agent
        mock_classifier = MagicMock()
        mock_classifier.run.return_value = {
            "type": "agent",
            "name": "TestAgent",
            "brain_count": 1,
            "reusability": "B"
        }
        self.mock_registry.get_instance.return_value = mock_classifier
        
        # Create coordinator
        coordinator = DevCoordinatorAgent()
        
        # Test code classification workflow
        request = {
            "code": "class TestAgent(Agent): pass",
            "options": {}
        }
        
        result = coordinator.run(request)
        
        # Verify workflow completion
        assert result["success"] is True
        assert result["type"] == "classification"
        assert result["result"]["type"] == "agent"
    
    @patch('tdev.agents.dev_coordinator_agent.get_registry')
    def test_full_workflow_goal_planning(self, mock_get_registry):
        """Test full workflow: goal → planning → evaluation → execution."""
        mock_get_registry.return_value = self.mock_registry
        
        # Mock all required agents
        mock_planner = MagicMock()
        mock_planner.run.return_value = {
            "workflow": {
                "id": "test-workflow",
                "steps": [{"agent": "EchoAgent"}]
            },
            "missing_capabilities": []
        }
        
        mock_evaluator = MagicMock()
        mock_evaluator.run.return_value = {
            "score": 95,
            "needs_improvement": False,
            "suggestions": []
        }
        
        mock_executor = MagicMock()
        mock_executor.run.return_value = {
            "output": "Workflow completed successfully",
            "steps": [{"step": 1, "agent": "EchoAgent", "result": "success"}]
        }
        
        def get_instance_side_effect(name):
            if name == "PlannerAgent":
                return mock_planner
            elif name == "EvaluatorAgent":
                return mock_evaluator
            elif name == "WorkflowExecutorAgent":
                return mock_executor
            return MagicMock()
        
        self.mock_registry.get_instance.side_effect = get_instance_side_effect
        
        # Create coordinator
        coordinator = DevCoordinatorAgent()
        
        # Test goal-based workflow
        request = {
            "goal": "Echo test message",
            "options": {"input": {"message": "Hello World"}}
        }
        
        result = coordinator.run(request)
        
        # Verify full workflow execution
        assert result["success"] is True
        assert result["type"] == "workflow_execution"
        assert result["result"] == "Workflow completed successfully"
        assert result["workflow_id"] == "test-workflow"
    
    @patch('tdev.agents.dev_coordinator_agent.get_registry')
    def test_workflow_with_missing_capabilities(self, mock_get_registry):
        """Test workflow handling when capabilities are missing."""
        mock_get_registry.return_value = self.mock_registry
        
        # Mock planner that identifies missing capabilities
        mock_planner = MagicMock()
        mock_planner.run.return_value = {
            "workflow": {
                "id": "test-workflow",
                "steps": [{"agent": "NonExistentAgent"}]
            },
            "missing_capabilities": [{
                "type": "agent",
                "name": "NonExistentAgent",
                "description": "Missing agent for workflow"
            }]
        }
        
        # Mock agent composer for generating missing capabilities
        mock_composer = MagicMock()
        mock_composer.run.return_value = {
            "success": True,
            "metadata": {"name": "NonExistentAgent"},
            "path": "/path/to/generated/agent.py"
        }
        
        def get_instance_side_effect(name):
            if name == "PlannerAgent":
                return mock_planner
            elif name == "AutoAgentComposerAgent":
                return mock_composer
            return MagicMock()
        
        self.mock_registry.get_instance.side_effect = get_instance_side_effect
        
        # Create coordinator
        coordinator = DevCoordinatorAgent()
        
        # Test workflow with missing capabilities
        request = {
            "goal": "Use non-existent agent",
            "options": {}
        }
        
        result = coordinator.run(request)
        
        # Verify capability generation was attempted
        assert result["success"] is True
        mock_composer.run.assert_called_once()
    
    def test_classifier_agent_integration(self):
        """Test ClassifierAgent with various code types."""
        classifier = ClassifierAgent()
        
        # Test agent classification
        agent_code = '''
from tdev.core.agent import Agent

class TestAgent(Agent):
    def run(self, input_data):
        return input_data
'''
        result = classifier.run({"code": agent_code})
        assert result["type"] == "agent"
        assert result["brain_count"] == 1
        
        # Test tool classification
        tool_code = '''
@tool
def test_tool(input_data):
    return input_data
'''
        result = classifier.run({"code": tool_code})
        assert result["type"] == "tool"
        assert result["brain_count"] == 0
    
    @patch('tdev.agents.planner_agent.get_registry')
    def test_planner_agent_integration(self, mock_get_registry):
        """Test PlannerAgent with goal planning."""
        mock_registry = MagicMock()
        mock_registry.get_by_type.return_value = [
            {"name": "EchoAgent", "type": "agent"},
            {"name": "TestAgent", "type": "agent"}
        ]
        mock_get_registry.return_value = mock_registry
        
        planner = PlannerAgent()
        result = planner.run("Echo the input message")
        
        assert "workflow" in result
        assert "missing_capabilities" in result
        workflow = result["workflow"]
        assert workflow["id"] is not None
        assert len(workflow["steps"]) > 0