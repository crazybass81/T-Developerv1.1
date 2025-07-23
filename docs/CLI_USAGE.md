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
# Deploy a service
tdev deploy --service-id my-service --target lambda

# Check deployment status
tdev status my-service

# Rollback a deployment
tdev rollback my-service --version previous
```

## Advanced Usage

### Environment Configuration

```bash
# Set the environment
tdev config set environment development

# Set AWS credentials
tdev config set aws.region ap-northeast-2
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