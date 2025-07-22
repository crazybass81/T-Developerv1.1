import pytest
import json
import tempfile
from pathlib import Path

from tdev.core.workflow import Workflow, save_workflow
from tdev.agents.workflow_executor_agent import WorkflowExecutorAgent
from tdev.core.registry import AgentRegistry

class MockAgent:
    """A mock agent for testing."""
    
    def __init__(self, return_value=None):
        """Initialize the mock agent."""
        self.return_value = return_value or "mock output"
        self.called = False
    
    def run(self, input_data):
        """Run the mock agent."""
        self.called = True
        return self.return_value

class MockRegistry:
    """A mock registry for testing."""
    
    def __init__(self, agents=None):
        """Initialize the mock registry."""
        self.agents = agents or {}
    
    def get_instance(self, name):
        """Get an instance of a component."""
        return self.agents.get(name)

class TestWorkflowExecutor:
    """Tests for the WorkflowExecutorAgent."""
    
    def setup_method(self):
        """Set up a temporary workflow for testing."""
        # Create a temporary directory for workflows
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workflows_dir = Path(self.temp_dir.name)
        
        # Create a simple workflow
        self.workflow = Workflow(
            id="test-workflow-v1",
            steps=[{"agent": "MockAgent"}],
            inputs={"input": "string"},
            outputs={"result": "output"}
        )
        
        # Save the workflow
        self.workflow_path = self.workflows_dir / "test-workflow.json"
        save_workflow(self.workflow, self.workflow_path)
        
        # Create a mock agent
        self.mock_agent = MockAgent()
        
        # Create a mock registry
        self.mock_registry = MockRegistry({"MockAgent": self.mock_agent})
        
        # Create a workflow executor
        self.executor = WorkflowExecutorAgent()
        
        # Monkey patch the executor to use the mock registry
        self.executor._get_registry = lambda: self.mock_registry
    
    def teardown_method(self):
        """Clean up the temporary workflow."""
        self.temp_dir.cleanup()
    
    def test_workflow_execution(self, monkeypatch):
        """Test executing a workflow."""
        # Monkey patch the get_workflow_path function
        def mock_get_workflow_path(workflow_id):
            return self.workflow_path
        
        monkeypatch.setattr("tdev.agents.workflow_executor_agent.get_workflow_path", mock_get_workflow_path)
        
        # Monkey patch the get_registry function in the workflow executor
        monkeypatch.setattr("tdev.agents.workflow_executor_agent.get_registry", lambda: self.mock_registry)
        
        # Execute the workflow
        result = self.executor.run("test-workflow")
        
        # Check that the mock agent was called
        assert self.mock_agent.called
        
        # Check the result
        assert "mock output" in result.values()