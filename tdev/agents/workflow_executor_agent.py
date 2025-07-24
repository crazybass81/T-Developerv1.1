from typing import Dict, Any, Optional

from tdev.core.agent import Agent
from tdev.core.registry import get_registry
from tdev.core.workflow import Workflow, load_workflow, get_workflow_path

class WorkflowExecutorAgent(Agent):
    """
    Agent responsible for executing workflows.
    
    The WorkflowExecutorAgent loads a workflow definition and executes
    each step in sequence, passing data between steps as needed.
    """
    
    def run(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a workflow.
        
        Args:
            request: A dictionary containing:
                - workflow: The workflow definition (dict) or workflow_id (str)
                - input: Optional input data for the workflow
            
        Returns:
            The output data from the workflow
        """
        # Handle both workflow dict and workflow_id
        workflow_data = request.get("workflow")
        input_data = request.get("input", {})
        
        if isinstance(workflow_data, str):
            # It's a workflow ID
            workflow_id = workflow_data
            print(f"WorkflowExecutorAgent: Running workflow {workflow_id}")
            workflow_path = get_workflow_path(workflow_id)
            workflow = load_workflow(workflow_path)
        elif isinstance(workflow_data, dict):
            # It's a workflow definition
            print(f"WorkflowExecutorAgent: Running workflow {workflow_data}")
            workflow = workflow_data
        else:
            return {"error": "Invalid workflow data provided"}
        
        # Initialize context with input data
        context = input_data or {}
        
        if not workflow:
            return {"error": "Workflow not found or invalid"}
        
        # Handle both Workflow objects and dict workflows
        if hasattr(workflow, 'id'):
            workflow_id = workflow.id
            steps = workflow.steps
            outputs = workflow.outputs
        else:
            workflow_id = workflow.get('id', 'unknown')
            steps = workflow.get('steps', [])
            outputs = workflow.get('outputs', {})
        
        print(f"WorkflowExecutorAgent: Loaded workflow {workflow_id}")
        
        # Get the registry
        registry = get_registry()
        
        # Execute each step
        for i, step in enumerate(steps):
            agent_name = step.get('agent')
            if not agent_name:
                print(f"WorkflowExecutorAgent: Step {i+1} has no agent specified")
                continue
            
            print(f"WorkflowExecutorAgent: Step {i+1}: Running {agent_name}")
            
            # Get the agent
            agent = registry.get_instance(agent_name)
            if not agent:
                print(f"WorkflowExecutorAgent: Agent not found: {agent_name}")
                continue
            
            # Get input for this step
            step_input = context.get(step.get('input_from', 'input'), {})
            
            # Run the agent
            try:
                step_output = agent.run(step_input)
                print(f"WorkflowExecutorAgent: Step {i+1}: {agent_name} completed")
                
                # Store the output in the context
                output_key = step.get('output_to', 'output')
                context[output_key] = step_output
            except Exception as e:
                print(f"WorkflowExecutorAgent: Error executing {agent_name}: {e}")
                context[f"error_{i}"] = str(e)
        
        # Extract the final output
        output = {}
        for output_name, source_key in outputs.items():
            output[output_name] = context.get(source_key)
        
        # If no outputs defined, return the entire context
        if not output:
            output = context
        
        print(f"WorkflowExecutorAgent: Workflow {workflow_id} completed")
        return output