# Orchestrator

## Overview

The **Agent Squad Orchestrator** (also called **DevCoordinator** or **SupervisorAgent**) is the central coordinator of the T-Developer system. It acts as the "brain of the operation," controlling the flow of tasks and information among various specialized agents.

## Core Responsibilities

1. **Workflow Management**: Initiates and manages end-to-end workflows for user requests
2. **Task Delegation**: Assigns tasks to appropriate agents and collects their outputs
3. **Decision Making**: Evaluates agent outputs and determines next steps
4. **Exception Handling**: Manages errors and unexpected situations
5. **Coordination**: Ensures proper sequencing and data flow between agents

## Orchestration Process

When a user submits a request, the Orchestrator follows this general process:

1. **Request Analysis**: The Orchestrator receives the user request and determines if it contains code or a goal
2. **Classification**: If code is provided, the Orchestrator calls the ClassifierAgent to determine its type
3. **Planning**: For goals, the Orchestrator calls the PlannerAgent to create a workflow plan
4. **Evaluation**: The EvaluatorAgent reviews the plan for quality and feasibility
5. **Execution**: If the plan is approved, the WorkflowExecutorAgent carries out the steps
6. **Result Delivery**: The final output is returned to the user

## Implementation

The Orchestrator is implemented as a MetaAgent that embodies the logic of coordinating other agents. It uses the **DevCoordinatorAgent** which leverages AWS Bedrock for intelligent coordination. The DevCoordinatorAgent uses the Agent Squad pattern with a SupervisorAgent that coordinates the core agents.

```python
from tdev.core.agent import Agent
from tdev.core.registry import get_registry
from tdev.agent_core.bedrock_client import BedrockClient
from tdev.agent_squad.agents import SupervisorAgent, SupervisorAgentOptions, BedrockAgent

class DevCoordinatorAgent(Agent):
    """The central orchestrator using AWS Bedrock."""
    
    def __init__(self):
        """Initialize the DevCoordinatorAgent."""
        self.registry = get_registry()
        self.bedrock_client = BedrockClient()
        self.supervisor = self._create_supervisor()
    
    def _create_supervisor(self):
        """Create a SupervisorAgent with AWS Bedrock."""
        # Create a lead agent using Bedrock
        lead_agent = BedrockAgent(
            AgentOptions(
                name="LeadAgent",
                description="The lead agent that coordinates the team",
                model_id="anthropic.claude-v2"
            )
        )
        
        # Wrap the core agents
        wrapped_agents = []
        core_agents = [
            "ClassifierAgent", 
            "PlannerAgent", 
            "EvaluatorAgent", 
            "WorkflowExecutorAgent"
        ]
        
        for agent_name in core_agents:
            agent = self.registry.get_instance(agent_name)
            if agent:
                wrapped_agents.append(SquadWrapperAgent(agent))
        
        # Create the SupervisorAgent
        options = SupervisorAgentOptions(
            name="DevCoordinator",
            description="Coordinates T-Developer workflow",
            lead_agent=lead_agent,
            team=wrapped_agents
        )
        
        return SupervisorAgent(options)
    
    def run(self, request):
        """Process a user request."""
        # Extract request details
        goal = request.get("goal", "")
        code = request.get("code")
        
        # Handle code or goal request
        if code:
            return self._handle_code_request(code, request.get("options", {}))
        else:
            return self._handle_goal_request(goal, request.get("options", {}))
```

## Dynamic Agent Generation

If the Orchestrator identifies that no existing component can fulfill a required functionality, it invokes **Agno (AutoAgentComposer)** to generate a new agent or tool on demand using AWS Bedrock for intelligent code generation:

```python
def handle_missing_capability(self, capability_spec):
    """Handle a missing capability by generating a new agent."""
    # Enhance the capability spec with more details using Bedrock
    if self.bedrock_client:
        capability_spec = self._enhance_capability_spec(capability_spec, goal)
    
    # Generate the new agent using Agno
    composer = self.registry.get_instance("AutoAgentComposerAgent")
    result = composer.run(capability_spec)
    
    # Test the newly generated agent
    if result.get("success", False):
        agent_name = result.get("metadata", {}).get("name")
        if agent_name:
            tester = self.registry.get_instance("AgentTesterAgent")
            test_result = tester.run(agent_name)
            result["test_result"] = test_result
    
    return result
```

## Using the Orchestrator

The Orchestrator can be invoked via the CLI:

```bash
# Use the orchestrator to fulfill a goal
tdev orchestrate "Echo the input data"

# Provide additional context or constraints
tdev orchestrate "Create a dashboard for the data" --context '{"data_source": "api", "format": "web"}'
```

## Advanced Features

### Core Orchestration (Phase 3)
- **Intelligent Coordination**: Use AWS Bedrock for intelligent coordination of agents
- **Dynamic Agent Generation**: Generate new agents on-demand using AWS Bedrock
- **Parallel Orchestration**: Coordinate multiple agent workflows simultaneously
- **Adaptive Planning**: Adjust workflows based on intermediate results
- **Feedback Integration**: Incorporate user feedback to improve future orchestration
- **Resource Management**: Optimize resource allocation for efficient execution
- **Deployment Integration**: Deploy agents to AWS Lambda and Bedrock Agent Core
- **Monitoring and Feedback**: Monitor deployed agents and collect user feedback

### Enterprise Features (Phase 4) ✅
- **Agent Versioning**: Manage multiple versions with A/B testing capabilities
- **Multi-Tenant Orchestration**: Tenant-isolated workflows with authentication
- **Internationalized Responses**: Multi-language support (English/Korean)
- **Plugin-Based Orchestration**: Extensible model and tool integration
- **Continuous Learning**: Self-improvement through feedback analysis
- **Enhanced API Integration**: WebSocket support for real-time orchestration updates

### Phase 4 Orchestration Enhancements

```python
# Version-aware orchestration
result = orchestrator.run({
    "goal": "Process data",
    "agent_version": "2.0",  # Use specific version
    "tenant_id": "company-a",  # Multi-tenant support
    "language": "ko"  # Internationalization
})

# Plugin-enhanced orchestration
result = orchestrator.run({
    "goal": "Generate advanced analysis",
    "preferred_plugin": "bedrock-claude",
    "learning_enabled": True  # Enable continuous learning
})
```