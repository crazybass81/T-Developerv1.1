# Workflow Guide

## What is a Workflow?

In T-Developer, a **Workflow** is a sequence of steps involving agents and tools that work together to achieve a specific goal. Workflows define the execution flow, data passing between components, and overall process for completing tasks.

## Creating Workflows

### Using the CLI

```bash
# Create a simple workflow using the EchoAgent
tdev compose --name echo-flow --steps EchoAgent

# Create a multi-step workflow
tdev compose --name process-flow --steps "DataFetchAgent,ProcessorAgent,OutputAgent"

# Create a workflow from a JSON definition
tdev compose --file workflow-definition.json
```

### Workflow Definition Format

Workflows can be defined in JSON format:

```json
{
  "id": "workflow-name-v1",
  "steps": [
    {
      "id": "step1",
      "agent": "XAgent",
      "input": { "param": "value" }
    },
    {
      "id": "step2",
      "agent": "YTool",
      "input": { "data": "${step1.result}" }
    }
  ]
}
```

## Executing Workflows

```bash
# Run a workflow by name
tdev run echo-flow

# Run a workflow with specific input
tdev run process-flow --input '{"data": "input value"}'

# Run a workflow and save the output
tdev run process-flow --output results.json
```

## Dynamic Workflow Generation

The PlannerAgent can automatically generate workflows based on goals:

```bash
# Generate and execute a workflow for a goal
tdev orchestrate "Process and analyze the data from the API"
```

## Workflow Components

A workflow consists of:

1. **Steps**: Individual actions performed by agents or tools
2. **Data Flow**: How data passes between steps
3. **Conditions**: Optional logic for branching or looping
4. **Error Handling**: How to handle failures in steps

## Advanced Workflow Features

### Core Features (Phase 3)
- **Parallel Execution**: Run multiple steps simultaneously
- **Conditional Branching**: Execute different steps based on conditions
- **Error Recovery**: Define fallback steps or retry logic
- **Workflow Versioning**: Track changes to workflows over time

### Phase 4 Enterprise Features ✅
- **Multi-Tenant Workflows**: Tenant-isolated workflow execution
- **Agent Version Selection**: Specify agent versions in workflows
- **Plugin-Enhanced Steps**: Use AI plugins for enhanced capabilities
- **Internationalized Workflows**: Multi-language workflow support
- **Continuous Learning**: Workflows that improve through feedback
- **Real-Time Monitoring**: WebSocket-based workflow progress tracking

## Phase 4 Workflow Enhancements

### Multi-Tenant Workflows

```json
{
  "id": "tenant-aware-workflow",
  "tenant_id": "company-a",
  "steps": [
    {
      "id": "step1",
      "agent": "DataProcessor",
      "version": "2.0",
      "input": { "data": "${input.data}" }
    }
  ]
}
```

### Plugin-Enhanced Workflows

```json
{
  "id": "ai-enhanced-workflow",
  "steps": [
    {
      "id": "analysis",
      "agent": "AIAnalyzer",
      "plugin": "bedrock-claude",
      "input": { "text": "${input.text}" }
    }
  ]
}
```

### Internationalized Workflows

```bash
# Run workflow with language preference
tdev run my-workflow --input '{"data": "test"}' --lang ko

# Create workflow with localized descriptions
tdev compose --name "분석-워크플로" --steps "DataAnalyzer" --lang ko
```

### Real-Time Workflow Monitoring

```python
# WebSocket connection for real-time updates
import asyncio
import websockets

async def monitor_workflow():
    uri = "ws://localhost:8000/ws/workflow-123"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            progress = json.loads(message)
            print(f"Step {progress['step']}: {progress['status']}")
```

## Best Practices

### Core Practices
1. **Clear Step Naming**: Use descriptive names for workflow steps
2. **Data Validation**: Validate inputs and outputs at each step
3. **Modularity**: Design workflows to be composable and reusable
4. **Documentation**: Document the purpose and expected behavior of workflows
5. **Testing**: Test workflows with various inputs and edge cases

### Phase 4 Enterprise Practices ✅
6. **Version Pinning**: Specify agent versions for reproducible workflows
7. **Tenant Isolation**: Ensure proper data isolation in multi-tenant workflows
8. **Plugin Strategy**: Choose appropriate plugins for enhanced capabilities
9. **Feedback Integration**: Enable workflow improvement through user feedback
10. **Performance Monitoring**: Track workflow execution metrics and optimize
11. **Internationalization**: Design workflows for global deployment
12. **Real-Time Updates**: Implement progress tracking for long-running workflows