import os
import sys
import json
import click
from pathlib import Path
from datetime import datetime

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
@click.argument('component_type', type=click.Choice(['agent', 'tool', 'team']))
@click.option('--name', required=True, help='Name of the agent or tool')
@click.option('--tool', help='Tool to use (for agents only)')
def init(component_type, name, tool):
    """Initialize a new agent, tool, or team."""
    if component_type == 'agent':
        click.echo(f"Initializing agent: {name}")
        # Create agent file
        agent_path = Path('tdev/agents') / f"{name.lower()}_agent.py"
        with open(agent_path, 'w', encoding='utf-8') as f:
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
    
    elif component_type == 'tool':
        click.echo(f"Initializing tool: {name}")
        # Create tool file
        tool_path = Path('tdev/tools') / f"{name.lower()}_tool.py"
        with open(tool_path, 'w', encoding='utf-8') as f:
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
        
    elif component_type == 'team':
        click.echo(f"Initializing team: {name}")
        # Ensure teams directory exists
        teams_dir = Path('tdev/teams')
        teams_dir.mkdir(exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = teams_dir / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write("")
        
        # Create team file
        team_path = teams_dir / f"{name.lower()}_team.py"
        with open(team_path, 'w', encoding='utf-8') as f:
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
        component_type = "agent"
    elif "tool" in str(file_path):
        component_type = "tool"
    elif "team" in str(file_path):
        component_type = "team"
    else:
        component_type = "unknown"
    
    # Add to registry
    registry_path = config.get_registry_path()
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    # Set appropriate class path based on type
    if component_type == "team":
        class_path = f"tdev.teams.{name}.{name.capitalize()}Team"
        brain_count = 2
        reusability = "D"
    elif component_type == "agent":
        class_path = f"tdev.agents.{name}.{name.capitalize()}Agent"
        brain_count = 1
        reusability = "B"
    elif component_type == "tool":
        class_path = f"tdev.tools.{name}.{name.lower()}_tool"
        brain_count = 0
        reusability = "A"
    else:
        class_path = f"tdev.{name}.{name}"
        brain_count = 1
        reusability = "B"
    
    registry[name] = {
        "type": component_type,
        "class": class_path,
        "brain_count": brain_count,
        "reusability": reusability
    }
    
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    
    click.echo(f"Registered {name} as {component_type}")

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
    
    with open(workflow_path, 'w', encoding='utf-8') as f:
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
    with open(workflow_path, 'r', encoding='utf-8') as f:
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

@build.command()
def package():
    """Package the application (not implemented)."""
    click.echo("Not implemented: build package")

@main.group()
def deploy():
    """Deployment commands for agents and services."""

@deploy.command()
@click.argument('agent_name')
@click.option(
    '--target', 
    default='lambda', 
    type=click.Choice(['lambda', 'bedrock']), 
    help='Deployment target'
)
@click.option('--region', help='AWS region')
def agent(agent_name, target, region):
    """Deploy an agent to AWS."""
    click.echo(f"Deploying agent {agent_name} to {target}...")
    
    # Get the registry
    registry = get_registry()
    
    # Check if agent exists
    agent_meta = registry.get(agent_name)
    if not agent_meta:
        click.echo(f"Agent {agent_name} not found in registry")
        return
    
    if target == 'lambda':
        # Import the Lambda deployer
        try:
            from tdev.agent_core.deployer import AgentDeployer
            deployer = AgentDeployer(region_name=region)
            result = deployer.deploy_agent(agent_name)
            
            if result.get("success"):
                click.echo(f"Successfully deployed {agent_name} to Lambda")
                click.echo(f"Lambda ARN: {result.get('lambda_arn')}")
            else:
                click.echo(f"Failed to deploy {agent_name}: {result.get('error')}")
        except ImportError:
            click.echo("Agent Core module not found. Please install the required dependencies.")
            return
    elif target == 'bedrock':
        # Import the Bedrock deployer
        try:
            from tdev.agent_core.deployer import AgentDeployer
            deployer = AgentDeployer(region_name=region)
            result = deployer.deploy_agent(agent_name)
            
            if result.get("success"):
                click.echo(f"Successfully deployed {agent_name} to Bedrock Agent Core")
                click.echo(f"Bedrock Agent ID: {result.get('bedrock_agent_id')}")
            else:
                click.echo(f"Failed to deploy {agent_name}: {result.get('error')}")
        except ImportError:
            click.echo("Agent Core module not found. Please install the required dependencies.")
            return

@deploy.command()
@click.argument('service_id')
@click.option(
    '--target', 
    default='lambda', 
    type=click.Choice(['lambda', 'ecs', 'local']), 
    help='Deployment target'
)
def service(service_id, target):
    """Deploy a composed service to AWS."""
    click.echo(f"Deploying service {service_id} to {target}...")
    
    # Get the registry
    registry = get_registry()
    
    # Check if service exists
    workflows_dir = config.get_workflows_dir()
    workflow_path = workflows_dir / f"{service_id}.json"
    
    if not workflow_path.exists():
        click.echo(f"Service {service_id} not found")
        return
    
    # Load workflow
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    # Deploy service (stub implementation)
    click.echo(f"Packaging service {service_id}...")
    click.echo(f"Deploying to {target}...")
    click.echo(f"Service {service_id} deployed successfully")
    
    # Update registry with deployment info
    service_meta = registry.get(service_id) or {}
    service_meta["deployment"] = {
        "type": target,
        "status": "deployed",
        "timestamp": str(datetime.now())
    }
    registry.update(service_id, service_meta)

@main.command()
@click.argument('service_id', required=False)
def status(service_id):
    """Check status of deployed services."""
    # Get the registry
    registry = get_registry()
    
    if service_id:
        # Check specific service
        service_meta = registry.get(service_id)
        if not service_meta:
            click.echo(f"Service {service_id} not found")
            return
        
        deployment = service_meta.get("deployment", {})
        if not deployment:
            click.echo(f"Service {service_id} is not deployed")
            return
        
        click.echo(f"Status of {service_id}:")
        click.echo(f"  Type: {deployment.get('type', 'unknown')}")
        click.echo(f"  Status: {deployment.get('status', 'unknown')}")
        click.echo(f"  Deployed at: {deployment.get('timestamp', 'unknown')}")
        
        # If deployed to Lambda, get more details
        if deployment.get('type') == 'lambda' and deployment.get('function_name'):
            try:
                import boto3
                lambda_client = boto3.client('lambda')
                function = lambda_client.get_function(FunctionName=deployment.get('function_name'))
                click.echo(f"  Runtime: {function['Configuration']['Runtime']}")
                click.echo(f"  Memory: {function['Configuration']['MemorySize']} MB")
                click.echo(f"  Timeout: {function['Configuration']['Timeout']} seconds")
                click.echo(f"  Last Modified: {function['Configuration']['LastModified']}")
            except Exception as e:
                click.echo(f"  Error getting Lambda details: {e}")
    else:
        # List all deployed services
        deployed_services = []
        for name, meta in registry.get_all().items():
            if "deployment" in meta:
                deployed_services.append((name, meta["deployment"]))
        
        if not deployed_services:
            click.echo("No deployed services found")
            return
        
        click.echo("Deployed services:")
        for name, deployment in deployed_services:
            status_str = f"  {name}: {deployment.get('type', 'unknown')} - {deployment.get('status', 'unknown')}"
            click.echo(status_str)

@main.group()
def monitor():
    """Monitoring commands for deployed agents."""

@monitor.command()
@click.argument('agent_name', required=False)
@click.option('--time-range', default='1h', help='Time range (e.g., 1h, 1d)')
@click.option(
    '--metrics', 
    default='invocations,errors,duration', 
    help='Comma-separated list of metrics'
)
def metrics(agent_name, time_range, metrics):
    """Get metrics for deployed agents."""
    # Get the registry
    registry = get_registry()
    
    # Get the ObserverAgent
    try:
        from tdev.monitoring.observer import ObserverAgent
        observer = ObserverAgent()
    except ImportError:
        click.echo("Monitoring module not found. Please install the required dependencies.")
        return
    
    # Parse metrics
    metrics_list = metrics.split(',')
    
    # Run the observer
    result = observer.run({
        "agent_name": agent_name,
        "time_range": time_range,
        "metrics": metrics_list
    })
    
    # Display the results
    click.echo(f"Metrics for time range: {time_range}")
    for agent_name, agent_data in result.get("results", {}).items():
        click.echo(f"\nAgent: {agent_name}")
        
        # Display metrics
        for metric_name, metric_data in agent_data.get("metrics", {}).items():
            if "error" in metric_data:
                click.echo(f"  {metric_name}: Error - {metric_data['error']}")
            else:
                total = metric_data.get("total")
                average = metric_data.get("average")
                if total is not None:
                    click.echo(f"  {metric_name}: Total = {total}")
                if average is not None:
                    click.echo(f"  {metric_name}: Average = {average:.2f}")
        
        # Display log count
        logs = agent_data.get("logs", {})
        if "error" in logs:
            click.echo(f"  Logs: Error - {logs['error']}")
        else:
            click.echo(f"  Logs: {logs.get('count', 0)} entries")

@monitor.command()
@click.argument('agent_name')
@click.option('--time-range', default='1h', help='Time range (e.g., 1h, 1d)')
@click.option('--limit', default=10, help='Maximum number of log entries')
def logs(agent_name, time_range, limit):
    """Get logs for a deployed agent."""
    # Get the registry
    registry = get_registry()
    
    # Get the ObserverAgent
    try:
        from tdev.monitoring.observer import ObserverAgent
        observer = ObserverAgent()
    except ImportError:
        click.echo("Monitoring module not found. Please install the required dependencies.")
        return
    
    # Run the observer
    result = observer.run({
        "agent_name": agent_name,
        "time_range": time_range
    })
    
    # Display the logs
    agent_data = result.get("results", {}).get(agent_name, {})
    logs = agent_data.get("logs", {})
    
    if "error" in logs:
        click.echo(f"Error getting logs: {logs['error']}")
        return
    
    events = logs.get("events", [])
    if not events:
        click.echo(f"No logs found for {agent_name} in the last {time_range}")
        return
    
    log_count = len(events)
    shown_count = min(limit, log_count)
    click.echo(f"Logs for {agent_name} (last {time_range}, showing {shown_count} of {log_count} entries):")
    for event in events[:limit]:
        timestamp = datetime.fromtimestamp(event.get("timestamp", 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        click.echo(f"[{timestamp}] {event.get('message', '')}")

@main.command()
@click.option('--port', default=8000, help='Port to run the server on')
def serve(port):
    """Start the API server for UI integration."""
    click.echo(f"Starting API server on port {port}...")
    
    try:
        from tdev.api.server import start_server
        os.environ["PORT"] = str(port)
        start_server()
    except ImportError:
        click.echo("API module not found. Please install the required dependencies.")
        return

@main.command()
@click.argument('team_name')
@click.option('--input', '-i', help='Input data as JSON string')
def run_team(team_name, input):
    """Run a team by name."""
    click.echo(f"Running team: {team_name}")
    
    # Get the registry
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
    """Orchestrate agents to fulfill a goal using Agent Squad."""
    click.echo(f"Orchestrating to fulfill goal: {goal}")
    
    # Get the registry
    registry = get_registry()
    
    # Get the DevCoordinatorAgent directly
    coordinator = registry.get_instance("DevCoordinatorAgent")
    if not coordinator:
        # Fall back to OrchestratorTeam if DevCoordinatorAgent is not found
        click.echo("DevCoordinatorAgent not found, falling back to OrchestratorTeam")
        team = registry.get_instance("OrchestratorTeam")
        if not team:
            click.echo("OrchestratorTeam not found")
            return
        
        # Prepare input data for team
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
        click.echo("Starting orchestration with OrchestratorTeam...")
        result = team.run(input_data)
    else:
        # Prepare request for DevCoordinatorAgent
        request = {"goal": goal}
        
        if code:
            request["code"] = code
        
        if options:
            try:
                request["options"] = json.loads(options)
            except json.JSONDecodeError:
                click.echo("Invalid JSON in options")
                return
        
        # Run the DevCoordinatorAgent
        click.echo("Starting orchestration with DevCoordinatorAgent...")
        result = coordinator.run(request)
    
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

@generate.command()
@click.option('--name', required=True, help='Name of the agent')
@click.option('--goal', required=True, help='Description of what the agent should do')
@click.option('--tool', help='Tool to use (for tool wrapper agents)')
@click.option('--spec', type=click.Path(exists=True), help='Path to a JSON specification file')
def generate_agent(name, goal, tool, spec):
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
        with open(spec, 'r', encoding='utf-8') as f:
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
        with open(spec, 'r', encoding='utf-8') as f:
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