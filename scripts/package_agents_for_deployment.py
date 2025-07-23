#!/usr/bin/env python
"""
Package agents for deployment to AWS Lambda.

This script:
1. Reads the agent registry
2. Creates deployment packages for each agent
3. Generates AWS SAM template for deployment
"""
import os
import json
import shutil
from pathlib import Path

from tdev.core.registry import get_registry

def main():
    """Package agents for deployment."""
    print("Packaging agents for deployment...")
    
    # Get the registry
    registry = get_registry()
    agents = registry.get_by_type("agent")
    
    # Create deployment directory
    deployment_dir = Path("deployment")
    agents_dir = deployment_dir / "agents"
    os.makedirs(agents_dir, exist_ok=True)
    
    # Generate SAM template
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Transform": "AWS::Serverless-2016-10-31",
        "Resources": {}
    }
    
    # Package each agent
    for agent in agents:
        agent_name = agent["name"]
        print(f"Packaging {agent_name}...")
        
        # Skip internal agents that shouldn't be deployed
        if agent_name in ["DevCoordinatorAgent", "MetaAgent"]:
            continue
        
        # Create agent directory
        agent_dir = agents_dir / agent_name.lower()
        os.makedirs(agent_dir, exist_ok=True)
        
        # Create handler.py
        with open(agent_dir / "handler.py", "w") as f:
            f.write(generate_handler(agent_name))
        
        # Create requirements.txt
        with open(agent_dir / "requirements.txt", "w") as f:
            f.write("boto3>=1.28.0\n")
        
        # Add to SAM template
        template["Resources"][agent_name] = {
            "Type": "AWS::Serverless::Function",
            "Properties": {
                "CodeUri": f"agents/{agent_name.lower()}/",
                "Handler": "handler.lambda_handler",
                "Runtime": "python3.9",
                "Timeout": 30,
                "MemorySize": 256,
                "Environment": {
                    "Variables": {
                        "AGENT_NAME": agent_name
                    }
                },
                "Events": {
                    "ApiEvent": {
                        "Type": "Api",
                        "Properties": {
                            "Path": f"/agents/{agent_name.lower()}",
                            "Method": "post"
                        }
                    }
                }
            }
        }
    
    # Write SAM template
    with open(deployment_dir / "template.yaml", "w") as f:
        f.write(yaml_dump(template))
    
    print("Packaging complete!")

def generate_handler(agent_name):
    """Generate Lambda handler for an agent."""
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
        module_path = "tdev.agents.{agent_name.lower()}"
        module = importlib.import_module(module_path)
        agent_class = getattr(module, "{agent_name}")
        
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

def yaml_dump(data):
    """Simple YAML dumper for SAM template."""
    import yaml
    return yaml.dump(data, default_flow_style=False)

if __name__ == "__main__":
    main()