# Execution Flow

This document details the end-to-end execution flow in the T-Developer system, from user request to final output.

## Overview

The execution flow in T-Developer follows these general stages:

1. **Request Submission**: User submits a request via CLI, UI, or API
2. **Request Processing**: The Orchestrator analyzes and processes the request
3. **Planning**: The system creates a plan to fulfill the request
4. **Execution**: The plan is executed step by step
5. **Result Delivery**: The final output is returned to the user

## Detailed Flow

### 1. Request Submission

A request can be submitted in several ways:

- **CLI Command**: `tdev orchestrate "Create a data processing pipeline"`
- **Web UI**: Entering a request in the Agent UI Launcher
- **API Call**: Sending a POST request to the orchestration endpoint

The request typically includes:
- A goal or objective in natural language
- Optional code or context
- Optional constraints or parameters

### 2. Request Processing

When the Orchestrator receives a request:

1. **Request Parsing**: The request is parsed to extract the goal, code, or other parameters
2. **Context Loading**: Any relevant context (project settings, available components) is loaded
3. **Request Classification**: The Orchestrator determines if the request contains code or a goal
   - If code is provided, it's sent to the ClassifierAgent
   - If a goal is provided, it proceeds to planning

### 3. Planning

For goal-based requests, the planning phase involves:

1. **Goal Analysis**: The PlannerAgent analyzes the goal to understand requirements
2. **Component Selection**: The Planner identifies which agents or tools can fulfill parts of the goal
3. **Workflow Creation**: The Planner creates a workflow plan with specific steps
4. **Plan Evaluation**: The EvaluatorAgent reviews the plan for quality and feasibility
5. **Plan Refinement**: If the evaluation score is low, the plan may be refined

If the plan requires components that don't exist:
1. **Gap Identification**: The Planner identifies missing capabilities
2. **Component Generation**: Agno is invoked to generate new agents or tools
3. **Registration**: New components are registered in the system
4. **Plan Update**: The plan is updated to include the new components

### 4. Execution

Once a plan is approved:

1. **Workflow Initialization**: The WorkflowExecutorAgent prepares to execute the plan
2. **Step Execution**: Each step in the workflow is executed in sequence
   - The appropriate agent or tool is invoked with the required inputs
   - Outputs from each step may be used as inputs for subsequent steps
3. **Progress Tracking**: The execution progress is tracked and may be reported to the user
4. **Error Handling**: If a step fails, the system may attempt recovery or report the error

### 5. Result Delivery

After execution completes:

1. **Result Compilation**: The final output is compiled from the workflow execution
2. **Formatting**: The result is formatted according to the request requirements
3. **Delivery**: The result is returned to the user via the original interface (CLI, UI, API)
4. **Logging**: The execution details are logged for future reference

## Example Flow

For a request like `tdev orchestrate "Create a weather dashboard for Seoul"`:

1. **Request Submission**: User submits the request via CLI
2. **Request Processing**: The Orchestrator identifies this as a goal-based request
3. **Planning**:
   - PlannerAgent analyzes the goal and determines it needs:
     - A weather data fetching component
     - A data processing component
     - A visualization component
   - It creates a workflow with these steps
   - EvaluatorAgent reviews and approves the plan
4. **Execution**:
   - WorkflowExecutorAgent runs the workflow:
     - WeatherDataAgent fetches Seoul weather data
     - DataProcessorAgent formats the data
     - DashboardGeneratorAgent creates the visualization
5. **Result Delivery**:
   - The dashboard URL or file is returned to the user
   - Execution logs are stored

## Advanced Flow Patterns

### Parallel Execution

For complex workflows, multiple steps may execute in parallel:

```
Step A -----> Step C
       \
Step B -----> Step D
```

### Conditional Branching

Workflows may include conditional logic:

```
Step A ---[if condition]---> Step B
       \
        [else]------------> Step C
```

### Feedback Loops

Some workflows may include feedback loops for refinement:

```
Step A --> Step B --> Evaluation
                         |
                         v
                     [if score < threshold]
                         |
                         v
                      Refinement
                         |
                         v
                      Step B (retry)
```

## Monitoring and Debugging

Throughout the execution flow, the system provides monitoring and debugging capabilities:

- **Logs**: Detailed logs of each step's execution
- **Progress Updates**: Real-time updates on workflow progress
- **Error Reports**: Detailed error information if steps fail
- **Execution Traces**: Complete traces of the execution path