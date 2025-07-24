"""
AWS Bedrock client for T-Developer.

This module provides a client for interacting with AWS Bedrock services.
"""
import os
import json
import boto3
from typing import Dict, Any, List, Optional

class BedrockClient:
    """Client for interacting with AWS Bedrock services."""
    
    def __init__(self, region_name: Optional[str] = None):
        """
        Initialize the Bedrock client.
        
        Args:
            region_name: AWS region name (defaults to environment variable or 'us-east-1')
        """
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        try:
            self.bedrock_runtime = boto3.client(
                service_name="bedrock-runtime",
                region_name=self.region_name
            )
            self.bedrock_agent = boto3.client(
                service_name="bedrock-agent",
                region_name=self.region_name
            )
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
            self.bedrock_runtime = None
            self.bedrock_agent = None
    
    def invoke_model(self, model_id: str, prompt: str, parameters: Dict[str, Any] = None) -> str:
        """
        Invoke a Bedrock model with a prompt.
        
        Args:
            model_id: The ID of the model to invoke
            prompt: The prompt to send to the model
            parameters: Optional parameters for the model
            
        Returns:
            The model's response as a string
        """
        if self.bedrock_runtime is None:
            return f"Mock response for: {prompt}"
        
        # Default parameters if none provided
        if parameters is None:
            parameters = {
                "maxTokens": 512,
                "temperature": 0.7,
                "topP": 0.9
            }
        
        try:
            # Prepare the request body based on the model
            if "anthropic" in model_id.lower():
                body = {
                    "prompt": f"\\n\\nHuman: {prompt}\\n\\nAssistant:",
                    "max_tokens_to_sample": parameters.get("maxTokens", 512),
                    "temperature": parameters.get("temperature", 0.7),
                    "top_p": parameters.get("topP", 0.9)
                }
            elif "amazon" in model_id.lower():
                body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": parameters.get("maxTokens", 512),
                        "temperature": parameters.get("temperature", 0.7),
                        "topP": parameters.get("topP", 0.9)
                    }
                }
            else:
                # Generic format for other models
                body = {
                    "prompt": prompt,
                    **parameters
                }
            
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            # Parse the response
            response_body = json.loads(response["body"].read().decode("utf-8"))
            
            # Extract text based on model type
            if "anthropic" in model_id.lower():
                return response_body.get("completion", "")
            elif "amazon" in model_id.lower():
                return response_body.get("results", [{}])[0].get("outputText", "")
            else:
                return str(response_body)
                
        except Exception as e:
            print(f"Warning: Bedrock model invocation failed: {e}")
            return f"Fallback response for: {prompt}"
    
    def create_agent(self, name: str, description: str, instructions: str, model_id: str) -> Dict[str, Any]:
        """
        Create a new Bedrock agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            instructions: Instructions for the agent
            model_id: The foundation model ID to use
            
        Returns:
            The created agent's details
        """
        response = self.bedrock_agent.create_agent(
            agentName=name,
            description=description,
            instructions=instructions,
            foundationModel=model_id
        )
        
        return response
    
    def deploy_agent_function(self, agent_id: str, function_name: str, lambda_arn: str) -> Dict[str, Any]:
        """
        Deploy a Lambda function as an agent action.
        
        Args:
            agent_id: The ID of the agent
            function_name: The name of the function
            lambda_arn: The ARN of the Lambda function
            
        Returns:
            The deployment response
        """
        # Create an action group
        action_group = self.bedrock_agent.create_agent_action_group(
            agentId=agent_id,
            actionGroupName=function_name,
            description=f"Action group for {function_name}",
            actionGroupExecutor={
                "lambda": {
                    "lambdaArn": lambda_arn
                }
            }
        )
        
        # Prepare the agent for deployment
        prepare_response = self.bedrock_agent.prepare_agent(
            agentId=agent_id
        )
        
        # Deploy the agent
        deploy_response = self.bedrock_agent.create_agent_alias(
            agentId=agent_id,
            agentAliasName="prod",
            description="Production deployment"
        )
        
        return {
            "action_group": action_group,
            "prepare": prepare_response,
            "deploy": deploy_response
        }