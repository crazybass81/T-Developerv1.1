#!/usr/bin/env python
"""
Update the registry with deployment information.

This script:
1. Gets the deployed Lambda functions
2. Updates the registry with deployment URLs
"""
import json
import boto3
import os
from pathlib import Path

from tdev.core.registry import get_registry

def main():
    """Update registry with deployment information."""
    print("Updating registry with deployment information...")
    
    # Get the registry
    registry = get_registry()
    
    # Get AWS Lambda client
    lambda_client = boto3.client('lambda')
    api_client = boto3.client('apigateway')
    
    # Get stack name
    stack_name = os.environ.get("STACK_NAME", "t-developer-agents")
    
    # Get deployed functions
    try:
        # Get all Lambda functions with the stack name tag
        functions = lambda_client.list_functions()
        
        # Filter functions that belong to our stack
        stack_functions = [
            f for f in functions.get('Functions', [])
            if stack_name in f.get('FunctionName', '')
        ]
        
        # Update registry with deployment info
        for function in stack_functions:
            function_name = function['FunctionName']
            agent_name = function_name.split('-')[-1]  # Extract agent name from function name
            
            # Get function URL
            try:
                url_config = lambda_client.get_function_url_config(FunctionName=function_name)
                function_url = url_config.get('FunctionUrl')
            except:
                function_url = f"https://lambda.{function['FunctionArn'].split(':')[3]}.amazonaws.com/2015-03-31/functions/{function_name}/invocations"
            
            # Update registry
            agent = registry.get(agent_name)
            if agent:
                agent['deployment'] = {
                    'type': 'lambda',
                    'function_name': function_name,
                    'function_arn': function['FunctionArn'],
                    'url': function_url,
                    'region': function['FunctionArn'].split(':')[3],
                    'last_modified': function['LastModified']
                }
                registry.update(agent_name, agent)
                print(f"Updated registry for {agent_name} with deployment info")
    
    except Exception as e:
        print(f"Error updating registry: {e}")
        return
    
    print("Registry update complete!")

if __name__ == "__main__":
    main()