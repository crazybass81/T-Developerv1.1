import os
import sys
import json
import click
from pathlib import Path

from tdev.core import config
from tdev.core.init_registry import initialize_registry
from tdev.core.registry import get_registry

@click.group()
def main():
    """T-Developer CLI - Agent orchestration system."""
    # Ensure the config directory exists
    config.get_config_dir()
    # Ensure registry exists
    config.ensure_registry_exists()

@main.command()
@click.argument('type', type=click.Choice(['agent', 'tool', 'team']))
@click.option('--name', required=True, help='Name of the agent or tool')
@click.option('--tool', help='Tool to use (for agents only)')
def init(type, name, tool):
    """Initialize a new agent, tool, or team."""
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
        
    elif type == 'team':
        click.echo(f"Initializing team: {name}")
        # Ensure teams directory exists
        teams_dir = Path('tdev/teams')
        teams_dir.mkdir(exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = teams_dir / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write("")
        
        # Create team file
        team_path = teams_dir / f"{name.lower()}_team.py"
        with open(team_path, 'w') as f:
            f.write(f'''from tdev.core.team import Team

class {name}Team(Team):
    """
    {name} team.
    """
    
    def __init__(self):
        super().__init__()
        # TODO: add member agents, e.g. self.add_agent("agent1", AgentClass())
    
    def run(self, input_data):
        """
        Coordinate the team agents.
        
        Args:
            input_data: The input data
            
        Returns:
            The output data
        """
        # TODO: implement sequence of agent calls
        return input_data
''')
        click.echo(f"Created team at {team_path}")

@main.command()
@click.argument('file', type=click.Path(exists=True))
def classify(file):
    """Classify a file as agent, tool, or team."""
    click.echo(f"Classifying {file}")
    
    # Get the registry
    from tdev.core.registry import get_registry
    registry = get_registry()
    
    # Get the ClassifierAgent
    classifier = registry.get_instance("ClassifierAgent")
    if not classifier:
        click.echo("ClassifierAgent not found in registry")
        # Fallback to simple classification
        if "team" in file:
            click.echo("Classification: team")
            return "team"
        elif "tool" in file:
            click.echo("Classification: tool")
            return "tool"
        else:
            click.echo("Classification: agent")
            return "agent"
    
    # Run the classifier
    result = classifier.run(file)
    
    # Display the result
    click.echo(f"Classification: {result['type']}")
    return result['type']

@main.command()
@click.argument('file', type=click.Path(exists=True))
def register(file):
    """Register an agent, tool, or team in the registry."""
    click.echo(f"Registering {file}")
    
    # Get file name without extension
    file_path = Path(file)
    name = file_path.stem
    
    # Determine type based on directory
    if "agent" in str(file_path):
        type = "agent"
    elif "tool" in str(file_path):
        type = "tool"
    elif "team" in str(file_path):
        type = "team"
    else:
        type = "unknown"
    
    # Add to registry
    registry_path = config.get_registry_path()
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Set appropriate class path based on type
    if type == "team":
        class_path = f"tdev.teams.{name}.{name.capitalize()}Team"
        brain_count = 2
        reusability = "D"
    elif type == "agent":
        class_path = f"tdev.agents.{name}.{name.capitalize()}Agent"
        brain_count = 1
        reusability = "B"
    elif type == "tool":
        class_path = f"tdev.tools.{name}.{name.lower()}_tool"
        brain_count = 0
        reusability = "A"
    else:
        class_path = f"tdev.{name}.{name}"
        brain_count = 1
        reusability = "B"
    
    registry[name] = {
        "type": type,
        "class": class_path,
        "brain_count": brain_count,
        "reusability": reusability
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
@click.argument('team_name')
@click.option('--input', '-i', help='Input data as JSON string')
def run_team(team_name, input):
    """Run a team by name."""
    click.echo(f"Running team: {team_name}")
    
    # Get the registry
    from tdev.core.registry import get_registry
    registry = get_registry()
    
    # Get the team
    team = registry.get_instance(team_name)
    if not team:
        click.echo(f"Team not found: {team_name}")
        return
    
    # Parse input data
    if input:
        try:
            input_data = json.loads(input)
        except json.JSONDecodeError:
            input_data = {"input": input}
    else:
        input_data = {}
    
    # Run the team
    click.echo(f"Executing team {team_name}...")
    result = team.run(input_data)
    
    # Display the result
    click.echo("Team execution completed.")
    click.echo(f"Result: {result}")
    
    return result

@main.command()
@click.argument('goal')
@click.option('--code', help='Path to code file to classify')
@click.option('--options', help='Options as JSON string')
def orchestrate(goal, code, options):
    """Orchestrate agents to fulfill a goal."""
    click.echo(f"Orchestrating to fulfill goal: {goal}")
    
    # Get the registry
    from tdev.core.registry import get_registry
    registry = get_registry()
    
    # Get the OrchestratorTeam
    team = registry.get_instance("OrchestratorTeam")
    if not team:
        click.echo("OrchestratorTeam not found")
        return
    
    # Prepare input data
    input_data = {"goal": goal}
    
    if code:
        input_data["code"] = code
    
    if options:
        try:
            input_data["options"] = json.loads(options)
        except json.JSONDecodeError:
            click.echo("Invalid JSON in options")
            return
    
    # Run the team
    click.echo("Starting orchestration...")
    result = team.run(input_data)
    
    # Display the result
    click.echo("Orchestration completed.")
    click.echo(f"Result: {result}")
    
    return result

@main.command()
@click.argument('goal')
@click.option('--code', help='Path to code file to classify')
@click.option('--options', help='Options as JSON string')
def orchestrate(goal, code, options):
    """Orchestrate agents to fulfill a goal."""
    click.echo(f"Orchestrating to fulfill goal: {goal}")
    
    # Get the registry
    from tdev.core.registry import get_registry
    registry = get_registry()
    
    # Get the OrchestratorTeam
    team = registry.get_instance("OrchestratorTeam")
    if not team:
        click.echo("OrchestratorTeam not found")
        return
    
    # Prepare input data
    input_data = {"goal": goal}
    
    if code:
        input_data["code"] = code
    
    if options:
        try:
            input_data["options"] = json.loads(options)
        except json.JSONDecodeError:
            click.echo("Invalid JSON in options")
            return
    
    # Run the team
    click.echo("Starting orchestration...")
    result = team.run(input_data)
    
    # Display the result
    click.echo("Orchestration completed.")
    click.echo(f"Result: {result}")
    
    return result

@main.command()
def init_registry():
    """Initialize the registry with core components."""
    initialize_registry()

@main.group()
def generate():
    """Generate new components using Agno."""
    pass

@generate.command()
@click.option('--name', required=True, help='Name of the agent')
@click.option('--goal', required=True, help='Description of what the agent should do')
@click.option('--tool', help='Tool to use (for tool wrapper agents)')
@click.option('--spec', type=click.Path(exists=True), help='Path to a JSON specification file')
def agent(name, goal, tool, spec):
    """Generate a new agent using Agno."""
    click.echo(f"Generating agent: {name}")
    
    # Get the registry
    registry = get_registry()
    
    # Get the AutoAgentComposer
    composer = registry.get_instance("AutoAgentComposerAgent")
    if not composer:
        click.echo("AutoAgentComposerAgent not found in registry")
        return
    
    # Prepare the specification
    if spec:
        with open(spec, 'r') as f:
            specification = json.load(f)
    else:
        specification = {
            "type": "agent",
            "name": name,
            "goal": goal
        }
        if tool:
            specification["tools"] = [tool]
            specification["template"] = "tool_wrapper"
    
    # Run the composer
    result = composer.run(specification)
    
    # Display the result
    if result.get("success"):
        click.echo(f"Generated agent at {result.get('path')}")
    else:
        click.echo(f"Failed to generate agent: {result.get('error')}")

@generate.command()
@click.option('--name', required=True, help='Name of the tool')
@click.option('--goal', required=True, help='Description of what the tool should do')
@click.option('--spec', type=click.Path(exists=True), help='Path to a JSON specification file')
def tool(name, goal, spec):
    """Generate a new tool using Agno."""
    click.echo(f"Generating tool: {name}")
    
    # Get the registry
    registry = get_registry()
    
    # Get the AutoAgentComposer
    composer = registry.get_instance("AutoAgentComposerAgent")
    if not composer:
        click.echo("AutoAgentComposerAgent not found in registry")
        return
    
    # Prepare the specification
    if spec:
        with open(spec, 'r') as f:
            specification = json.load(f)
    else:
        specification = {
            "type": "tool",
            "name": name,
            "goal": goal
        }
    
    # Run the composer
    result = composer.run(specification)
    
    # Display the result
    if result.get("success"):
        click.echo(f"Generated tool at {result.get('path')}")
    else:
        click.echo(f"Failed to generate tool: {result.get('error')}")

if __name__ == '__main__':
    main()