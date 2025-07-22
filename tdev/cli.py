import os
import sys
import json
import click
from pathlib import Path

from tdev.core import config
from tdev.core.init_registry import initialize_registry

@click.group()
def main():
    """T-Developer CLI - Agent orchestration system."""
    # Ensure the config directory exists
    config.get_config_dir()
    # Ensure registry exists
    config.ensure_registry_exists()

@main.command()
@click.argument('type', type=click.Choice(['agent', 'tool']))
@click.option('--name', required=True, help='Name of the agent or tool')
@click.option('--tool', help='Tool to use (for agents only)')
def init(type, name, tool):
    """Initialize a new agent or tool."""
    if type == 'agent':
        click.echo(f"Initializing agent: {name}")
        # Create agent file
        agent_path = Path('tdev/agents') / f"{name.lower()}_agent.py"
        with open(agent_path, 'w') as f:
            f.write(f'''from tdev.core.agent import Agent

class {name}Agent(Agent):
    """
    {name} agent.
    """
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: The input data
            
        Returns:
            The output data
        """
        # TODO: Implement agent logic
        return input_data
''')
        click.echo(f"Created agent at {agent_path}")
    
    elif type == 'tool':
        click.echo(f"Initializing tool: {name}")
        # Create tool file
        tool_path = Path('tdev/tools') / f"{name.lower()}_tool.py"
        with open(tool_path, 'w') as f:
            f.write(f'''from tdev.core.tool import tool

@tool
def {name.lower()}_tool(input_data):
    """
    {name} tool.
    
    Args:
        input_data: The input data
        
    Returns:
        The output data
    """
    # TODO: Implement tool logic
    return input_data
''')
        click.echo(f"Created tool at {tool_path}")

@main.command()
@click.argument('file', type=click.Path(exists=True))
def classify(file):
    """Classify a file as agent, tool, or team."""
    click.echo(f"Classifying {file}")
    # Stub implementation - always returns "agent"
    click.echo("Classification: agent")
    return "agent"

@main.command()
@click.argument('file', type=click.Path(exists=True))
def register(file):
    """Register an agent or tool in the registry."""
    click.echo(f"Registering {file}")
    
    # Get file name without extension
    file_path = Path(file)
    name = file_path.stem
    
    # Determine type based on directory
    if "agent" in str(file_path):
        type = "agent"
    elif "tool" in str(file_path):
        type = "tool"
    else:
        type = "unknown"
    
    # Add to registry
    registry_path = config.get_registry_path()
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    registry[name] = {
        "type": type,
        "class": f"tdev.{type}s.{name}.{name.capitalize()}"
    }
    
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    click.echo(f"Registered {name} as {type}")

@main.command()
@click.option('--name', required=True, help='Name of the workflow')
@click.option('--steps', required=True, help='Comma-separated list of agent names')
def compose(name, steps):
    """Compose a workflow from agents."""
    click.echo(f"Composing workflow: {name}")
    
    # Parse steps
    step_list = steps.split(',')
    
    # Create workflow definition
    workflow = {
        "id": f"{name}-v1",
        "steps": [{"agent": step} for step in step_list]
    }
    
    # Save workflow
    workflows_dir = config.get_workflows_dir()
    workflow_path = workflows_dir / f"{name}.json"
    
    with open(workflow_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    click.echo(f"Created workflow at {workflow_path}")

@main.command()
@click.argument('workflow_id')
def run(workflow_id):
    """Run a workflow."""
    click.echo(f"Running workflow: {workflow_id}")
    
    # Find workflow file
    workflows_dir = config.get_workflows_dir()
    workflow_path = workflows_dir / f"{workflow_id}.json"
    
    if not workflow_path.exists():
        click.echo(f"Workflow not found: {workflow_id}")
        return
    
    # Load workflow
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)
    
    # Execute steps (stub)
    click.echo(f"Executing workflow {workflow['id']}:")
    for i, step in enumerate(workflow['steps']):
        agent_name = step['agent']
        click.echo(f"  Step {i+1}: Executing {agent_name}... done.")
    
    click.echo("Workflow execution completed.")

@main.command()
@click.argument('agent_name')
def test(agent_name):
    """Test an agent."""
    click.echo(f"Testing agent: {agent_name}")
    
    # Get the registry
    from tdev.core.registry import get_registry
    registry = get_registry()
    
    # Get the AgentTesterAgent
    tester = registry.get_instance("AgentTesterAgent")
    if not tester:
        click.echo("AgentTesterAgent not found in registry")
        return False
    
    # Run the test
    result = tester.run(agent_name)
    
    # Display the result
    if result.get("success"):
        click.echo(f"Testing {agent_name}... PASSED")
    else:
        click.echo(f"Testing {agent_name}... FAILED")
        click.echo(f"Passed {result.get('passed', 0)}/{result.get('total', 0)} tests")
    
    return result.get("success", False)

@main.group()
def build():
    """Build commands (not implemented)."""
    pass

@build.command()
def package():
    """Package the application (not implemented)."""
    click.echo("Not implemented: build package")

@main.group()
def deploy():
    """Deployment commands (not implemented)."""
    pass

@deploy.command()
@click.argument('service_id')
def lambda_function(service_id):
    """Deploy to AWS Lambda (not implemented)."""
    click.echo(f"Not implemented: deploy {service_id} to Lambda")

@main.command()
@click.argument('service_id', required=False)
def status(service_id):
    """Check status of services (not implemented)."""
    if service_id:
        click.echo(f"Not implemented: status of {service_id}")
    else:
        click.echo("Not implemented: status of all services")

@main.command()
def init_registry():
    """Initialize the registry with core components."""
    initialize_registry()

if __name__ == '__main__':
    main()