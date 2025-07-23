"""
Tests for the BedrockClient class.
"""
import os
import json
import unittest
from unittest.mock import patch, MagicMock

import boto3
import pytest

from tdev.agent_core.bedrock_client import BedrockClient

class TestBedrockClient(unittest.TestCase):
    """Test the BedrockClient class."""
    
    @patch('boto3.client')
    def test_init(self, mock_boto3_client):
        """Test initialization of BedrockClient."""
        # Create mock clients
        mock_bedrock_runtime = MagicMock()
        mock_bedrock_agent = MagicMock()
        
        # Configure boto3.client to return our mocks
        mock_boto3_client.side_effect = lambda service_name, **kwargs: {
            'bedrock-runtime': mock_bedrock_runtime,
            'bedrock-agent': mock_bedrock_agent
        }[service_name]
        
        # Create client
        client = BedrockClient(region_name="us-east-1")
        
        # Check that boto3.client was called correctly
        mock_boto3_client.assert_any_call(service_name="bedrock-runtime", region_name="us-east-1")
        mock_boto3_client.assert_any_call(service_name="bedrock-agent", region_name="us-east-1")
        
        # Check that the client has the correct attributes
        self.assertEqual(client.region_name, "us-east-1")
        self.assertEqual(client.bedrock_runtime, mock_bedrock_runtime)
        self.assertEqual(client.bedrock_agent, mock_bedrock_agent)
    
    @patch('boto3.client')
    def test_invoke_model_anthropic(self, mock_boto3_client):
        """Test invoking an Anthropic model."""
        # Create mock clients
        mock_bedrock_runtime = MagicMock()
        mock_bedrock_agent = MagicMock()
        
        # Configure boto3.client to return our mocks
        mock_boto3_client.side_effect = lambda service_name, **kwargs: {
            'bedrock-runtime': mock_bedrock_runtime,
            'bedrock-agent': mock_bedrock_agent
        }[service_name]
        
        # Configure mock response
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'completion': 'Hello, world!'
        }).encode('utf-8')
        mock_bedrock_runtime.invoke_model.return_value = mock_response
        
        # Create client and invoke model
        client = BedrockClient(region_name="us-east-1")
        response = client.invoke_model(
            model_id="anthropic.claude-v2",
            prompt="Hello",
            parameters={"maxTokens": 10}
        )
        
        # Check that invoke_model was called correctly
        mock_bedrock_runtime.invoke_model.assert_called_once()
        args, kwargs = mock_bedrock_runtime.invoke_model.call_args
        self.assertEqual(kwargs['modelId'], "anthropic.claude-v2")
        
        # Parse the body to check the prompt format
        body = json.loads(kwargs['body'])
        self.assertIn("Human: Hello", body['prompt'])
        self.assertEqual(body['max_tokens_to_sample'], 10)
        
        # Check the response
        self.assertEqual(response, {'completion': 'Hello, world!'})
    
    @patch('boto3.client')
    def test_invoke_model_amazon(self, mock_boto3_client):
        """Test invoking an Amazon model."""
        # Create mock clients
        mock_bedrock_runtime = MagicMock()
        mock_bedrock_agent = MagicMock()
        
        # Configure boto3.client to return our mocks
        mock_boto3_client.side_effect = lambda service_name, **kwargs: {
            'bedrock-runtime': mock_bedrock_runtime,
            'bedrock-agent': mock_bedrock_agent
        }[service_name]
        
        # Configure mock response
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'outputText': 'Hello, world!'
        }).encode('utf-8')
        mock_bedrock_runtime.invoke_model.return_value = mock_response
        
        # Create client and invoke model
        client = BedrockClient(region_name="us-east-1")
        response = client.invoke_model(
            model_id="amazon.titan-text",
            prompt="Hello",
            parameters={"maxTokens": 10}
        )
        
        # Check that invoke_model was called correctly
        mock_bedrock_runtime.invoke_model.assert_called_once()
        args, kwargs = mock_bedrock_runtime.invoke_model.call_args
        self.assertEqual(kwargs['modelId'], "amazon.titan-text")
        
        # Parse the body to check the prompt format
        body = json.loads(kwargs['body'])
        self.assertEqual(body['inputText'], "Hello")
        self.assertEqual(body['textGenerationConfig']['maxTokenCount'], 10)
        
        # Check the response
        self.assertEqual(response, {'outputText': 'Hello, world!'})
    
    @patch('boto3.client')
    def test_create_agent(self, mock_boto3_client):
        """Test creating a Bedrock agent."""
        # Create mock clients
        mock_bedrock_runtime = MagicMock()
        mock_bedrock_agent = MagicMock()
        
        # Configure boto3.client to return our mocks
        mock_boto3_client.side_effect = lambda service_name, **kwargs: {
            'bedrock-runtime': mock_bedrock_runtime,
            'bedrock-agent': mock_bedrock_agent
        }[service_name]
        
        # Configure mock response
        mock_bedrock_agent.create_agent.return_value = {
            'agentId': 'test-agent-id',
            'agentName': 'TestAgent'
        }
        
        # Create client and create agent
        client = BedrockClient(region_name="us-east-1")
        response = client.create_agent(
            name="TestAgent",
            description="A test agent",
            instructions="Do test things",
            model_id="anthropic.claude-v2"
        )
        
        # Check that create_agent was called correctly
        mock_bedrock_agent.create_agent.assert_called_once_with(
            agentName="TestAgent",
            description="A test agent",
            instructions="Do test things",
            foundationModel="anthropic.claude-v2"
        )
        
        # Check the response
        self.assertEqual(response, {
            'agentId': 'test-agent-id',
            'agentName': 'TestAgent'
        })

if __name__ == '__main__':
    unittest.main()