"""
Test configuration and fixtures
"""
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_aws_services():
    """Mock AWS services to prevent actual API calls during testing"""
    with patch('boto3.client') as mock_client:
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_bedrock.invoke_model.return_value = {
            'body': MagicMock(read=lambda: b'{"completion": "mocked response"}')
        }
        
        # Mock Lambda client
        mock_lambda = MagicMock()
        mock_lambda.create_function.return_value = {'FunctionArn': 'arn:aws:lambda:us-east-1:123456789012:function:test'}
        
        # Configure mock client to return appropriate service mocks
        def client_side_effect(service_name, **kwargs):
            if service_name == 'bedrock-runtime':
                return mock_bedrock
            elif service_name == 'lambda':
                return mock_lambda
            else:
                return MagicMock()
        
        mock_client.side_effect = client_side_effect
        yield mock_client

@pytest.fixture
def mock_bedrock_client():
    """Specific Bedrock client mock"""
    with patch('tdev.agent_core.bedrock_client.BedrockClient') as mock:
        mock_instance = MagicMock()
        mock_instance.invoke_model.return_value = "Mocked AI response"
        mock.return_value = mock_instance
        yield mock_instance
