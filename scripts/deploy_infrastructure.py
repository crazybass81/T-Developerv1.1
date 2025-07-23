#!/usr/bin/env python
"""
Deploy T-Developer infrastructure to AWS.

This script deploys the CloudFormation template to create the necessary
AWS resources for T-Developer v1.1.
"""
import os
import sys
import argparse
import boto3
import time
from botocore.exceptions import ClientError

def deploy_stack(stack_name, template_file, environment):
    """
    Deploy a CloudFormation stack.
    
    Args:
        stack_name: Name of the stack
        template_file: Path to the CloudFormation template
        environment: Deployment environment (dev, staging, prod)
        
    Returns:
        Stack ID if successful, None otherwise
    """
    # Read the template
    with open(template_file, 'r') as f:
        template_body = f.read()
    
    # Create CloudFormation client
    cf_client = boto3.client('cloudformation')
    
    # Check if stack exists
    try:
        cf_client.describe_stacks(StackName=stack_name)
        stack_exists = True
    except ClientError as e:
        if "does not exist" in str(e):
            stack_exists = False
        else:
            print(f"Error checking stack: {e}")
            return None
    
    # Create or update the stack
    try:
        if stack_exists:
            print(f"Updating stack {stack_name}...")
            response = cf_client.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=[
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': environment
                    }
                ],
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            stack_id = response['StackId']
            print(f"Stack update initiated: {stack_id}")
        else:
            print(f"Creating stack {stack_name}...")
            response = cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=[
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': environment
                    }
                ],
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            stack_id = response['StackId']
            print(f"Stack creation initiated: {stack_id}")
        
        # Wait for stack to complete
        print("Waiting for stack operation to complete...")
        waiter = cf_client.get_waiter('stack_update_complete' if stack_exists else 'stack_create_complete')
        waiter.wait(StackName=stack_name)
        
        # Get stack outputs
        response = cf_client.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0]['Outputs']
        print("\nStack outputs:")
        for output in outputs:
            print(f"  {output['OutputKey']}: {output['OutputValue']}")
        
        return stack_id
    
    except ClientError as e:
        if "No updates are to be performed" in str(e):
            print("No changes to apply to the stack.")
            return stack_name
        else:
            print(f"Error deploying stack: {e}")
            return None

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Deploy T-Developer infrastructure")
    parser.add_argument("--stack-name", default="t-developer", help="CloudFormation stack name")
    parser.add_argument("--template", default="deployment/cloudformation.yaml", help="Path to CloudFormation template")
    parser.add_argument("--environment", default="dev", choices=["dev", "staging", "prod"], help="Deployment environment")
    
    args = parser.parse_args()
    
    # Check if template exists
    if not os.path.exists(args.template):
        print(f"Error: Template file {args.template} not found")
        sys.exit(1)
    
    # Deploy the stack
    stack_id = deploy_stack(args.stack_name, args.template, args.environment)
    if stack_id:
        print(f"\nStack deployment successful: {stack_id}")
        sys.exit(0)
    else:
        print("\nStack deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()