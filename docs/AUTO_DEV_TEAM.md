# AutoDevTeam Assembly

## Overview

The **AutoDevTeam** is the core assembly of agents that work together to automate the software development process in T-Developer v1.1. This document explains how these agents collaborate to form a virtual development team capable of understanding requirements, planning solutions, generating code, and deploying applications.

## Team Composition

The AutoDevTeam consists of the following specialized agents:

1. **SupervisorAgent (DevCoordinator)**: The team lead that coordinates all other agents
2. **ClassifierAgent**: Analyzes code to determine its type and characteristics
3. **PlannerAgent**: Breaks down goals into actionable steps
4. **EvaluatorAgent**: Reviews plans and code for quality and correctness
5. **WorkflowExecutorAgent**: Executes the planned steps
6. **AutoAgentComposer (Agno)**: Generates new agents and tools as needed

## Roles and Responsibilities

### SupervisorAgent (DevCoordinator)

- Acts as the team lead and central coordinator
- Manages the overall workflow and decision-making process
- Delegates tasks to specialized agents
- Handles exceptions and adjusts plans as needed
- Ensures the final output meets the user's requirements

### ClassifierAgent

- Analyzes code to determine if it's a Tool, Agent, or Team
- Identifies the "brain count" of components
- Extracts metadata from code (name, description, inputs, outputs)
- Helps maintain the component registry by classifying new additions

### PlannerAgent

- Interprets user goals and requirements
- Breaks down complex tasks into smaller, manageable steps
- Identifies which agents or tools are needed for each step
- Creates a structured workflow plan with proper sequencing
- Identifies gaps where new components might be needed

### EvaluatorAgent

- Reviews workflow plans for quality, efficiency, and correctness
- Scores plans based on predefined criteria
- Provides feedback and suggestions for improvement
- Validates that plans will meet the user's requirements
- May also evaluate generated code or components

### WorkflowExecutorAgent

- Executes workflow plans step by step
- Manages data flow between steps
- Handles errors and exceptions during execution
- Tracks progress and provides status updates
- Collects and formats the final output

### AutoAgentComposer (Agno)

- Generates new agents or tools based on specifications
- Analyzes requirements for new components
- Creates code that follows system conventions and best practices
- Registers new components in the system
- Enables the team to extend its capabilities dynamically

## Collaboration Process

The AutoDevTeam follows this general collaboration process:

1. **Request Intake**: The SupervisorAgent receives a user request
2. **Analysis**: 
   - If code is provided, the ClassifierAgent analyzes it
   - If a goal is provided, the PlannerAgent creates a plan
3. **Quality Check**: The EvaluatorAgent reviews the plan
4. **Capability Assessment**: The team checks if all required components exist
5. **Component Generation**: If needed, Agno creates new components
6. **Execution**: The WorkflowExecutorAgent carries out the plan
7. **Delivery**: The final result is returned to the user

## Example Scenario

For a request like "Create an API that fetches weather data and returns it as JSON":

1. **SupervisorAgent** receives the request and identifies it as a goal
2. **PlannerAgent** creates a plan with steps:
   - Fetch weather data from a service
   - Process the data into the required format
   - Create an API endpoint to serve the data
3. **EvaluatorAgent** reviews and approves the plan
4. The team discovers it needs a WeatherDataFetcherAgent that doesn't exist
5. **Agno** generates the missing WeatherDataFetcherAgent
6. **WorkflowExecutorAgent** executes the plan:
   - The new WeatherDataFetcherAgent gets weather data
   - A DataProcessorAgent formats it as JSON
   - An APIGeneratorAgent creates the endpoint
7. **SupervisorAgent** returns the completed API to the user

## Phase 3 Enhancements

In Phase 3 of T-Developer, the AutoDevTeam has been enhanced with:

1. **Improved Coordination**: Better communication between agents
2. **Dynamic Team Assembly**: More flexible team composition based on needs
3. **Advanced Planning**: More sophisticated planning capabilities
4. **Parallel Execution**: Ability to run multiple agents simultaneously
5. **Feedback Integration**: Better incorporation of evaluation results

These enhancements enable the AutoDevTeam to handle more complex development tasks with greater efficiency and quality.