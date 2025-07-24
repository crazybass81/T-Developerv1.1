# T-Developer Agent Core Module

This module provides integration with AWS Bedrock Agent Core for T-Developer v1.1. It includes components for deploying agents to AWS Lambda and Bedrock, and for interacting with Bedrock models.

## Components

### Bedrock Client

The `BedrockClient` class provides a client for interacting with AWS Bedrock services. It can:

- Invoke Bedrock models with prompts
- Create Bedrock agents
- Deploy Lambda functions as agent actions

Example usage:

```python
from tdev.agent_core.bedrock_client import BedrockClient

# Create a client
client = BedrockClient(region_name="us-east-1")

# Invoke a model
response = client.invoke_model(
    model_id="anthropic.claude-v2",
    prompt="Hello, how are you?",
    parameters={"maxTokens": 100}
)

# Print the response
print(response)
```

### Agent Deployer

The `AgentDeployer` class provides functionality to deploy agents to AWS Lambda and Bedrock Agent Core. It can:

- Create deployment packages for agents
- Deploy agents to AWS Lambda
- Create Bedrock agents and connect them to Lambda functions

Example usage:

```python
from tdev.agent_core.deployer import AgentDeployer

# Create a deployer
deployer = AgentDeployer(region_name="us-east-1")

# Deploy an agent
result = deployer.deploy_agent("MyAgent")

# Print the result
print(result)
```

## Deployment Process

The deployment process involves several steps:

1. **Create Deployment Package**: The deployer creates a deployment package for the agent, including the agent code, dependencies, and a Lambda handler.

2. **Deploy to Lambda**: The deployer deploys the package to AWS Lambda, creating or updating a Lambda function.

3. **Create Bedrock Agent**: The deployer creates a Bedrock agent with the agent's description and instructions.

4. **Connect Lambda to Bedrock**: The deployer connects the Lambda function to the Bedrock agent as an action.

5. **Update Registry**: The deployer updates the agent registry with the deployment information.

## Lambda Handler

The deployer generates a Lambda handler for each agent. The handler:

- Parses the input from the Lambda event
- Imports and instantiates the agent
- Runs the agent with the input
- Returns the result as a Lambda response

## Integration with AWS Bedrock

The module integrates with AWS Bedrock to:

- Use Bedrock models for intelligent planning, evaluation, and code generation
- Deploy agents to Bedrock Agent Core for serverless execution
- Connect agents to other AWS services via Bedrock's tool gateway

## CLI Commands

The agent_core module provides the following CLI commands:

```bash
# Deploy an agent to AWS Lambda
tdev deploy agent MyAgent --target lambda

# Deploy an agent to Bedrock Agent Core
tdev deploy agent MyAgent --target bedrock
```

## Required AWS Permissions

The module requires the following AWS permissions:

- `lambda:CreateFunction`, `lambda:UpdateFunctionCode`, `lambda:GetFunction`
- `bedrock:InvokeModel`
- `bedrock-agent:CreateAgent`, `bedrock-agent:CreateAgentActionGroup`
- `iam:PassRole`

These permissions are included in the CloudFormation template in the `LambdaExecutionRole`.