# Workflow Guide

This guide explains how to define and use workflows in the T-Developer system.

## What is a Workflow?

In T-Developer, a **Workflow** is a sequence of steps, each referencing an agent or team to execute. Workflows define how data flows between steps and how components are combined to accomplish a task.

Workflows are stored as JSON or YAML files in the `.tdev/workflows/` directory.

## Workflow Definition Format

A workflow definition includes:

- **id**: A unique identifier for the workflow, often including a version suffix
- **steps**: An array of execution steps, each mapping an agent to part of the data flow
- **inputs**: The structure of input values received from the user
- **outputs**: The final output returned from the workflow
- **description**: A summary of the workflow's purpose and function

### Example Workflow Definition

```json
{
  "id": "summarize-upload-flow-v1",
  "description": "Summarize text and upload to S3",
  "inputs": {
    "text": "string"
  },
  "steps": [
    {
      "id": "summarize",
      "agent": "SummarizerAgent",
      "input_from": "text",
      "output_to": "summary"
    },
    {
      "id": "upload",
      "agent": "S3UploaderAgent",
      "input_from": "summary",
      "output_to": "s3_url"
    }
  ],
  "outputs": {
    "result": "s3_url"
  }
}
```

## Creating Workflows

### Using the Orchestrator

In Phase 3, you can use the orchestrator to automatically generate and execute workflows based on a goal:

```bash
tdev orchestrate "Summarize text and upload to S3"
```

This will:
1. Invoke the MetaAgent to coordinate the process
2. Use the PlannerAgent to generate a workflow plan
3. Use the EvaluatorAgent to assess the plan's quality
4. Use the WorkflowExecutorAgent to execute the workflow

If any required agents are missing, the AutoAgentComposer (Agno) will generate them automatically.

### Using the CLI

You can create a workflow using the CLI:

```bash
tdev compose --name summarize-upload --steps SummarizerAgent,S3UploaderAgent
```

This will create a basic workflow definition in `.tdev/workflows/summarize-upload.json`.

You can also include teams in your workflow:

```bash
tdev compose --name process-data --steps DataFetcherAgent,ProcessingTeam,StorageAgent
```

Teams are treated as single steps in the workflow, with their internal coordination logic hidden from the workflow definition.

### Manual Creation

You can also create workflow definitions manually:

1. Create a JSON or YAML file in the `.tdev/workflows/` directory
2. Define the workflow structure as shown in the example above
3. Ensure all referenced agents are registered in the registry

## Workflow Execution

To execute a workflow, use the `run` command:

```bash
tdev run summarize-upload
```

This will:
1. Load the workflow definition
2. Initialize the execution context with any provided inputs
3. Execute each step in sequence
4. Return the final output

### Execution Process

When a workflow is executed:

1. The WorkflowExecutorAgent loads the workflow definition
2. It resolves each agent reference through the registry
3. It executes each step in sequence, passing data between steps
4. The final output is returned to the user

## Data Flow Between Steps

Data flows between steps through the execution context:

1. Each step can read input from the context using `input_from`
2. Each step writes its output to the context using `output_to`
3. The final output is extracted from the context using the `outputs` mapping

### Example Data Flow

```
Input: {"text": "Long document..."}

Step 1: SummarizerAgent
  - Reads: context["text"]
  - Writes: context["summary"] = "Summary of document..."

Step 2: S3UploaderAgent
  - Reads: context["summary"]
  - Writes: context["s3_url"] = "s3://bucket/file.txt"

Output: {"result": "s3://bucket/file.txt"}
```

## Advanced Workflow Features

### Input Mapping

You can specify how inputs are mapped to steps:

```json
"steps": [
  {
    "id": "step1",
    "agent": "AgentA",
    "input_from": {
      "param1": "input.field1",
      "param2": "input.field2"
    },
    "output_to": "result1"
  }
]
```

### Conditional Steps (Future)

In future versions, workflows may support conditional execution of steps:

```json
"steps": [
  {
    "id": "step1",
    "agent": "AgentA",
    "input_from": "input",
    "output_to": "result1",
    "condition": "input.type == 'text'"
  }
]
```

### Parallel Execution (Future)

In future versions, workflows may support parallel execution of steps:

```json
"parallel": [
  {
    "id": "step1",
    "agent": "AgentA",
    "input_from": "input",
    "output_to": "result1"
  },
  {
    "id": "step2",
    "agent": "AgentB",
    "input_from": "input",
    "output_to": "result2"
  }
]
```

## Best Practices

1. **Version Workflows**: Include a version suffix in the workflow ID
2. **Clear Step Names**: Use descriptive names for steps
3. **Explicit Data Flow**: Clearly define how data flows between steps
4. **Error Handling**: Consider how errors in one step affect the workflow
5. **Testing**: Test workflows with various inputs to ensure they work as expected

## Example: Echo Workflow

Here's a complete example of a simple workflow:

```json
{
  "id": "echo-flow-v1",
  "description": "A simple workflow that echoes the input",
  "inputs": {
    "message": "string"
  },
  "steps": [
    {
      "id": "echo",
      "agent": "EchoAgent",
      "input_from": "message",
      "output_to": "result"
    }
  ],
  "outputs": {
    "result": "result"
  }
}
```

This workflow simply passes the input message to the EchoAgent and returns its output.

## Example: Using a Team in a Workflow

Here's an example of a workflow that includes a team:

```json
{
  "id": "double-echo-flow-v1",
  "description": "A workflow that uses the DoubleEchoTeam",
  "inputs": {
    "message": "string"
  },
  "steps": [
    {
      "id": "double-echo",
      "agent": "DoubleEchoTeam",
      "input_from": "message",
      "output_to": "result"
    }
  ],
  "outputs": {
    "result": "result"
  }
}
```

In this workflow, the DoubleEchoTeam is treated as a single step, even though internally it coordinates two EchoAgent instances. This encapsulation allows complex logic to be hidden behind a simple interface in the workflow.