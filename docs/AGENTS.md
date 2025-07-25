# Agent Development Guide

## What is an Agent?

In T-Developer, an **Agent** is a component with a single decision-making point ("1 brain"). Agents are more complex than Tools but simpler than Teams. They can make decisions, process inputs, and produce outputs based on their specialized functionality.

## Core System Agents

T-Developer includes several built-in agents that form the backbone of the orchestration system:

### Phase 3 Core Agents
1. **ClassifierAgent**: Analyzes code to determine its type (Tool/Agent/Team)
2. **PlannerAgent**: Breaks down goals into steps and selects appropriate agents using AWS Bedrock
3. **EvaluatorAgent**: Scores workflows for quality and efficiency using AWS Bedrock
4. **WorkflowExecutorAgent**: Runs the composed workflows step by step
5. **AutoAgentComposer (Agno)**: Generates new agents and tools based on specifications using AWS Bedrock

### Phase 4 Enterprise Agents ✅
6. **LearningAgent**: Analyzes feedback and suggests improvements
7. **ObserverAgent**: Monitors deployed agents and collects metrics
8. **FeedbackCollector**: Collects and processes user feedback for continuous improvement

## Creating a New Agent

### Using the CLI

```bash
# Create a new agent
tdev init agent --name MyAgent

# Edit the agent file
vim tdev/agents/my_agent.py

# Register the agent
tdev register tdev/agents/my_agent.py

# Test the agent
tdev test MyAgent
```

### Agent Structure

A basic agent follows this structure:

```python
from tdev.core import agent

@agent
def my_agent(input_data):
    """
    My custom agent that does something specific.
    
    Args:
        input_data: The input data for the agent
        
    Returns:
        The processed output
    """
    # Agent logic here
    result = process_data(input_data)
    return result
```

### Using Tools within Agents

Agents can use Tools to perform specific functions:

```python
from tdev.core import agent
from tdev.tools import some_tool, another_tool

@agent
def my_agent(input_data):
    # Use tools within your agent
    intermediate_result = some_tool(input_data)
    final_result = another_tool(intermediate_result)
    return final_result
```

## Agent Metadata

Each agent has associated metadata that describes its capabilities:

### Basic Metadata
- **name**: Unique identifier for the agent
- **description**: What the agent does
- **input_schema**: Expected input format
- **output_schema**: Expected output format
- **tools**: List of tools used by the agent
- **brain_count**: Always 1 for agents
- **reusability**: Rating of how reusable the agent is (A-D)

### Phase 4 Enhanced Metadata ✅
- **version**: Agent version (e.g., "1.0", "2.0")
- **status**: Version status (ACTIVE, DEPRECATED, EXPERIMENTAL)
- **tenant_id**: Multi-tenancy support
- **plugin_dependencies**: Required plugins
- **performance_metrics**: Historical performance data
- **feedback_score**: User satisfaction rating

## Testing Agents

Agents should be tested to ensure they work as expected:

```bash
# Test an agent with specific input
tdev test MyAgent --input '{"key": "value"}'

# Run all tests for an agent
tdev test MyAgent --all
```

## Phase 4 Agent Features

### Agent Versioning

```bash
# Create a new version of an agent
tdev version add MyAgent 2.0 --metadata '{"improvements": "Enhanced performance"}'

# Promote version to active
tdev version promote MyAgent 2.0

# A/B test different versions
tdev version compare MyAgent 1.0 2.0 --metrics performance,accuracy
```

### Multi-Tenant Agents

```python
@agent
def tenant_aware_agent(input_data, context=None):
    """Agent with tenant isolation support."""
    tenant_id = context.get('tenant_id') if context else None
    
    # Process data with tenant isolation
    result = process_with_tenant_context(input_data, tenant_id)
    return result
```

### Plugin-Enhanced Agents

```python
from tdev.core.plugins import plugin_manager

@agent
def ai_enhanced_agent(input_data):
    """Agent using AI plugins for enhanced capabilities."""
    # Use specific AI model plugin
    plugin = plugin_manager.get_plugin("bedrock-claude")
    enhanced_result = plugin.invoke(f"Analyze: {input_data}")
    return enhanced_result
```

### Continuous Learning Integration

```python
@agent
def learning_enabled_agent(input_data, feedback_enabled=True):
    """Agent that learns from feedback."""
    result = process_data(input_data)
    
    if feedback_enabled:
        # Log for learning system
        learning_agent = get_registry().get_instance("LearningAgent")
        learning_agent.log_execution({
            "agent": "learning_enabled_agent",
            "input": input_data,
            "output": result,
            "timestamp": datetime.now()
        })
    
    return result
```

## Best Practices

### Core Practices
1. **Single Responsibility**: Each agent should have a clear, focused purpose
2. **Clear Documentation**: Document inputs, outputs, and behavior
3. **Error Handling**: Handle exceptions gracefully
4. **Tool Composition**: Use existing tools rather than reimplementing functionality
5. **Statelessness**: Design agents to be stateless when possible
6. **Testing**: Create comprehensive tests for your agent

### Phase 4 Enterprise Practices ✅
7. **Version Management**: Use semantic versioning for agent updates
8. **Tenant Isolation**: Ensure proper data isolation in multi-tenant environments
9. **Plugin Integration**: Leverage plugins for enhanced capabilities
10. **Feedback Integration**: Enable continuous learning through feedback collection
11. **Performance Monitoring**: Track and optimize agent performance metrics
12. **Internationalization**: Support multiple languages where applicable