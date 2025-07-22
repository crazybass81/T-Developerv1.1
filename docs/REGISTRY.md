# T-Developer Registry

This document explains how the registry works in T-Developer and how it integrates with the Agent Squad orchestrator.

## Overview

The **AgentRegistry** is the central directory of all available components in T-Developer. It maintains metadata about each agent, tool, and team, and provides methods to retrieve and instantiate them.

## Registry Structure

The registry is stored as a JSON file in the `.tdev` directory:

```json
{
  "EchoAgent": {
    "type": "agent",
    "class": "tdev.agents.echo_agent.EchoAgent",
    "brain_count": 1,
    "reusability": "B"
  },
  "EchoTool": {
    "type": "tool",
    "class": "tdev.tools.echo_tool.echo_tool",
    "brain_count": 0,
    "reusability": "A"
  }
}
```

Each entry in the registry includes:
- **name**: The name of the component (the key in the JSON)
- **type**: The type of component (agent, tool, or team)
- **class**: The import path to the component's class or function
- **brain_count**: The number of decision points (0 for tools, 1 for agents, 2+ for teams)
- **reusability**: The reusability tier (A for tools, B for agents, D for teams)

## Registry API

The registry provides the following methods:

- **get_instance(name)**: Get an instance of a component by name
- **register(name, metadata)**: Register a new component with metadata
- **unregister(name)**: Remove a component from the registry
- **get_all()**: Get all registered components
- **get_by_type(type)**: Get all components of a specific type

## Integration with Agent Squad

The registry is dynamically integrated with the Agent Squad orchestrator:

### Dynamic Registration

When a new component is registered via `tdev register` or programmatically, it is automatically made available to the Agent Squad orchestrator. This is done through a synchronization mechanism that updates the orchestrator's agent list whenever the registry changes.

```python
# When a new agent is registered
def register(name, metadata):
    # Add to registry
    registry[name] = metadata
    # Sync with Agent Squad
    sync_with_squad(registry)
```

### Component Wrapping

Type 'agent' components are automatically wrapped for inclusion in the Agent Squad system at runtime. This is done using the `SquadWrapperAgent` class, which adapts T-Developer agents to the Agent Squad interface:

```python
def sync_with_squad(registry):
    for name, metadata in registry.items():
        if metadata["type"] == "agent":
            # Get the agent instance
            agent = get_instance(name)
            # Wrap it for Agent Squad
            wrapped_agent = SquadWrapperAgent(agent)
            # Add it to the orchestrator
            orchestrator.add_agent(name, wrapped_agent)
```

### Single Source of Truth

The T-Developer AgentRegistry remains the single source of truth for available agents/tools. The Agent Squad orchestrator dynamically reflects the registry's contents, ensuring that any changes to the registry are immediately available to the orchestrator.

## Usage

### Registering a Component

Components can be registered via the CLI:

```bash
tdev register path/to/component.py
```

Or programmatically:

```python
from tdev.core.registry import get_registry
from tdev.core.schema import AgentMeta

registry = get_registry()
agent_meta = AgentMeta(
    name="MyAgent",
    class_path="tdev.agents.my_agent.MyAgent",
    description="My custom agent"
)
registry.register("MyAgent", agent_meta.to_dict())
```

### Getting a Component

Components can be retrieved from the registry:

```python
from tdev.core.registry import get_registry

registry = get_registry()
agent = registry.get_instance("MyAgent")
result = agent.run(input_data)
```

## Benefits of Integration

The integration of the registry with Agent Squad provides several benefits:

1. **Dynamic Discovery**: New agents and tools are automatically available to the orchestrator
2. **Consistent Naming**: Components have the same names in both systems
3. **Single Source of Truth**: The registry remains the authoritative source of component information
4. **Simplified Management**: Components only need to be registered once to be available everywhere