# CLI Usage Guide

The T-Developer Command Line Interface (CLI) provides tools for creating, managing, and running components in the system. This guide covers the main commands and their usage.

## Installation

The CLI is installed as part of the T-Developer package:

```bash
# Install the package
cd T-Developerv1.1
pip install -e .
```

## Basic Commands

### Initialize the Registry

```bash
# Initialize the registry with core components
tdev init-registry
```

### Component Management

#### Creating Components

```bash
# Create a new agent
tdev init agent --name MyAgent

# Create a new tool
tdev init tool --name MyTool

# Create a new team
tdev init team --name MyTeam
```

#### Registering Components

```bash
# Register a component
tdev register path/to/component.py

# Register all components in a directory
tdev register-all path/to/directory
```

#### Listing Components

```bash
# List all registered components
tdev list

# List components by type
tdev list agents
tdev list tools
tdev list teams
```

### Workflow Management

#### Creating Workflows

```bash
# Create a simple workflow
tdev compose --name echo-flow --steps EchoAgent

# Create a multi-step workflow
tdev compose --name process-flow --steps "DataFetchAgent,ProcessorAgent,OutputAgent"

# Create a workflow from a JSON definition
tdev compose --file workflow-definition.json
```

#### Running Workflows

```bash
# Run a workflow by name
tdev run echo-flow

# Run a workflow with specific input
tdev run process-flow --input '{"data": "input value"}'

# Run a workflow and save the output
tdev run process-flow --output results.json
```

### Agent Generation

```bash
# Generate a new agent using Agno
tdev generate agent --name CustomAgent --goal "A custom agent that does something specific"

# Generate a new tool
tdev generate tool --name CustomTool --goal "A tool that performs a specific operation"

# Generate with specific plugin
tdev generate agent --name AIAgent --goal "AI-powered analysis" --plugin bedrock-claude
```

### Phase 4 Features

#### Agent Versioning

```bash
# Add a new version of an agent
tdev version add MyAgent 2.0 --metadata '{"description": "Enhanced version"}'

# Promote a version to active
tdev version promote MyAgent 2.0

# List all versions of an agent
tdev version list MyAgent

# Compare agent versions (A/B testing)
tdev version compare MyAgent 1.0 2.0
```

#### Authentication & Multi-Tenancy

```bash
# Generate API key for authentication
tdev auth generate-key --user john.doe --permissions read,write,deploy

# Authenticate with API key
tdev auth login --api-key your-api-key-here

# Check current user permissions
tdev auth whoami
```

#### Internationalization

```bash
# Set language preference
tdev config set language ko

# Get localized help
tdev --help --lang ko

# Run orchestration with language preference
tdev orchestrate "데이터를 분석해주세요" --lang ko
```

#### Plugin Management

```bash
# List available plugins
tdev plugins list

# Install a plugin
tdev plugins install bedrock-claude

# Use specific plugin for generation
tdev generate agent --plugin bedrock-claude --goal "Advanced analysis"
```

### Orchestration

```bash
# Use the orchestrator to fulfill a goal
tdev orchestrate "Echo the input data"

# Provide additional context or constraints
tdev orchestrate "Create a dashboard for the data" --context '{"data_source": "api", "format": "web"}'
```

### Testing

```bash
# Test a component
tdev test MyAgent

# Test with specific input
tdev test MyAgent --input '{"key": "value"}'

# Run all tests for a component
tdev test MyAgent --all
```

### Deployment

```bash
# Deploy an agent to AWS Lambda
tdev deploy agent MyAgent --target lambda

# Deploy an agent to Bedrock Agent Core
tdev deploy agent MyAgent --target bedrock --region us-east-1

# Deploy a service (workflow)
tdev deploy service my-service --target lambda

# Check deployment status
tdev status my-service

# Deploy infrastructure using CloudFormation
python scripts/deploy_infrastructure.py --stack-name t-developer --environment dev
```

## Advanced Usage

### Environment Configuration

```bash
# Set the environment
tdev config set environment development

# Set AWS credentials
tdev config set aws.region ap-northeast-2
```

### Monitoring and Feedback

```bash
# Get metrics for a deployed agent
tdev monitor metrics MyAgent --time-range 1h

# Get logs for a deployed agent
tdev monitor logs MyAgent --time-range 1h --limit 10

# Submit feedback for an agent
tdev feedback MyAgent --rating 5 --comment "Works great!"
```

### API Server

```bash
# Start the API server
tdev serve --port 8000
```

### Debugging

```bash
# Enable debug mode
tdev --debug run my-workflow

# View logs
tdev logs my-service --tail
```

### Batch Operations

```bash
# Execute multiple commands from a file
tdev batch commands.txt
```

## Help and Documentation

```bash
# Get general help
tdev --help

# Get help for a specific command
tdev orchestrate --help
```