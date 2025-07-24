"""
Tests for the Deployer module.
"""
import pytest
from unittest.mock import MagicMock, patch
from tdev.agent_core.deployer import AgentDeployer

class TestAgentDeployer:
    """Test the AgentDeployer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_boto3 = MagicMock()
        with patch('tdev.agent_core.deployer.boto3', self.mock_boto3):
            self.deployer = AgentDeployer()
    
    @patch('tdev.agent_core.deployer.boto3')
    @patch('tdev.agent_core.deployer.BedrockClient')
    def test_init(self, mock_bedrock_client, mock_boto3):
        """Test deployer initialization."""
        deployer = AgentDeployer()
        assert deployer is not None
    
    @patch('tdev.agent_core.deployer.get_registry')
    @patch('tdev.agent_core.deployer.boto3')
    @patch('tdev.agent_core.deployer.BedrockClient')
    def test_deploy_agent(self, mock_bedrock_client, mock_boto3, mock_get_registry):
        """Test agent deployment."""
        # Mock registry
        mock_registry = MagicMock()
        mock_registry.get.return_value = {
            "name": "TestAgent",
            "type": "agent",
            "class_path": "tdev.agents.test_agent.TestAgent"
        }
        mock_get_registry.return_value = mock_registry
        
        # Mock AWS clients
        mock_lambda = MagicMock()
        mock_boto3.client.return_value = mock_lambda
        mock_lambda.create_function.return_value = {
            'FunctionArn': 'arn:aws:lambda:us-east-1:123456789012:function:test-agent'
        }
        mock_lambda.get_function.return_value = {
            'Configuration': {'FunctionArn': 'arn:aws:lambda:us-east-1:123456789012:function:test-agent'}
        }
        
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_bedrock_client.return_value = mock_bedrock
        mock_bedrock.create_agent.return_value = {'agentId': 'test-agent-id'}
        
        with patch('tempfile.mkdtemp', return_value='/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/handler.py'):
                with patch('builtins.open', MagicMock()):
                    with patch('subprocess.run'):
                        with patch('shutil.make_archive'):
                            deployer = AgentDeployer()
                            result = deployer.deploy_agent("TestAgent")
        
        assert result["success"] is True
        assert "lambda_arn" in result
    
    @patch('tdev.agent_core.deployer.BedrockClient')
    def test_generate_handler(self, mock_bedrock_client):
        """Test handler generation."""
        deployer = AgentDeployer()
        agent_meta = {
            "class_path": "tdev.agents.test_agent.TestAgent"
        }
        
        handler_code = deployer._generate_handler("TestAgent", agent_meta)
        
        assert isinstance(handler_code, str)
        assert "lambda_handler" in handler_code
        assert "TestAgent" in handler_code