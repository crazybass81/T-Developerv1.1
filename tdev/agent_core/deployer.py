"""
Agent deployer for AWS Bedrock Agent Core.

This module provides functionality to deploy agents to AWS Bedrock Agent Core.
"""
import os
import json
import boto3
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from tdev.core.registry import get_registry
from tdev.agent_core.bedrock_client import BedrockClient

class AgentDeployer:
    """Deployer for AWS Bedrock Agent Core."""
    
    def __init__(self, region_name: Optional[str] = None):
        """
        Initialize the agent deployer.
        
        Args:
            region_name: AWS region name (defaults to environment variable or 'us-east-1')
        """
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.bedrock_client = BedrockClient(region_name=self.region_name)
        self.lambda_client = boto3.client("lambda", region_name=self.region_name)
        self.registry = get_registry()
    
    def deploy_agent(self, agent_name: str) -> Dict[str, Any]:
        """
        Deploy an agent to AWS Bedrock Agent Core.
        
        Args:
            agent_name: Name of the agent to deploy
            
        Returns:
            Deployment details
        """
        # Get agent from registry
        agent_meta = self.registry.get(agent_name)
        if not agent_meta:
            raise ValueError(f"Agent {agent_name} not found in registry")
        
        # Create deployment package
        package_path = self._create_deployment_package(agent_name, agent_meta)
        
        # Deploy to Lambda
        lambda_arn = self._deploy_to_lambda(agent_name, package_path, agent_meta)
        
        # Create Bedrock agent
        bedrock_agent = self._create_bedrock_agent(agent_name, agent_meta, lambda_arn)
        
        # Update registry with deployment info
        agent_meta["deployment"] = {
            "type": "bedrock",
            "lambda_arn": lambda_arn,
            "bedrock_agent_id": bedrock_agent.get("agentId"),
            "region": self.region_name,
            "status": "deployed"
        }
        self.registry.update(agent_name, agent_meta)
        
        return {
            "success": True,
            "agent_name": agent_name,
            "lambda_arn": lambda_arn,
            "bedrock_agent_id": bedrock_agent.get("agentId")
        }
    
    def _create_deployment_package(self, agent_name: str, agent_meta: Dict[str, Any]) -> str:
        """
        Create a deployment package for the agent.
        
        Args:
            agent_name: Name of the agent
            agent_meta: Agent metadata
            
        Returns:
            Path to the deployment package
        """
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create handler.py
            with open(os.path.join(temp_dir, "handler.py"), "w") as f:
                f.write(self._generate_handler(agent_name, agent_meta))
            
            # Create requirements.txt
            with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
                f.write("boto3>=1.28.0\n")
            
            # Install dependencies
            subprocess.run(
                ["pip", "install", "-r", "requirements.txt", "-t", temp_dir],
                cwd=temp_dir,
                check=True
            )
            
            # Copy agent code
            agent_module = agent_meta.get("class_path", "").split(".")[:-1]
            agent_file = "/".join(agent_module) + ".py"
            agent_path = Path(agent_file)
            
            if agent_path.exists():
                target_dir = os.path.join(temp_dir, *agent_module[:-1])
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(agent_path, target_dir)
            
            # Create zip file
            zip_path = os.path.join(temp_dir, f"{agent_name.lower()}.zip")
            shutil.make_archive(
                os.path.join(temp_dir, agent_name.lower()),
                "zip",
                temp_dir
            )
            
            return zip_path
        
        except Exception as e:
            shutil.rmtree(temp_dir)
            raise e
    
    def _deploy_to_lambda(self, agent_name: str, package_path: str, agent_meta: Dict[str, Any]) -> str:
        """
        Deploy the agent to AWS Lambda.
        
        Args:
            agent_name: Name of the agent
            package_path: Path to the deployment package
            agent_meta: Agent metadata
            
        Returns:
            ARN of the deployed Lambda function
        """
        function_name = f"t-developer-{agent_name.lower()}"
        
        # Check if function exists
        try:
            self.lambda_client.get_function(FunctionName=function_name)
            # Update existing function
            with open(package_path, "rb") as f:
                self.lambda_client.update_function_code(
                    FunctionName=function_name,
                    ZipFile=f.read()
                )
        except self.lambda_client.exceptions.ResourceNotFoundException:
            # Create new function
            with open(package_path, "rb") as f:
                response = self.lambda_client.create_function(
                    FunctionName=function_name,
                    Runtime="python3.9",
                    Role=os.environ.get("LAMBDA_ROLE_ARN", ""),
                    Handler="handler.lambda_handler",
                    Code={"ZipFile": f.read()},
                    Timeout=30,
                    MemorySize=256,
                    Environment={
                        "Variables": {
                            "AGENT_NAME": agent_name
                        }
                    },
                    Tags={
                        "CreatedBy": "T-Developer",
                        "AgentName": agent_name
                    }
                )
        
        # Get function ARN
        function = self.lambda_client.get_function(FunctionName=function_name)
        return function["Configuration"]["FunctionArn"]
    
    def _create_bedrock_agent(self, agent_name: str, agent_meta: Dict[str, Any], lambda_arn: str) -> Dict[str, Any]:
        """
        Create a Bedrock agent for the deployed Lambda function.
        
        Args:
            agent_name: Name of the agent
            agent_meta: Agent metadata
            lambda_arn: ARN of the Lambda function
            
        Returns:
            Bedrock agent details
        """
        # Create Bedrock agent
        description = agent_meta.get("description", f"Agent for {agent_name}")
        instructions = f"You are {agent_name}, an agent that {description}. Use the available actions to fulfill user requests."
        
        bedrock_agent = self.bedrock_client.create_agent(
            name=agent_name,
            description=description,
            instructions=instructions,
            model_id="anthropic.claude-v2"  # Default model
        )
        
        # Deploy Lambda function as agent action
        self.bedrock_client.deploy_agent_function(
            agent_id=bedrock_agent["agentId"],
            function_name=agent_name,
            lambda_arn=lambda_arn
        )
        
        return bedrock_agent
    
    def _generate_handler(self, agent_name: str, agent_meta: Dict[str, Any]) -> str:
        """
        Generate Lambda handler for an agent.
        
        Args:
            agent_name: Name of the agent
            agent_meta: Agent metadata
            
        Returns:
            Handler code
        """
        class_path = agent_meta.get("class_path", "")
        module_path = ".".join(class_path.split(".")[:-1])
        class_name = class_path.split(".")[-1]
        
        return f"""import json
import os
import importlib
import sys

def lambda_handler(event, context):
    \"\"\"AWS Lambda handler for {agent_name}.\"\"\"
    try:
        # Parse input
        body = event.get('body', '{{}}')
        if isinstance(body, str):
            body = json.loads(body)
        
        # Import the agent
        sys.path.append('/opt/python')
        module_path = "{module_path}"
        module = importlib.import_module(module_path)
        agent_class = getattr(module, "{class_name}")
        
        # Create and run the agent
        agent = agent_class()
        result = agent.run(body)
        
        # Return the result
        return {{
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {{
                'Content-Type': 'application/json'
            }}
        }}
    except Exception as e:
        return {{
            'statusCode': 500,
            'body': json.dumps({{
                'error': str(e)
            }}),
            'headers': {{
                'Content-Type': 'application/json'
            }}
        }}
"""