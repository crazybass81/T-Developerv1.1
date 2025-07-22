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
    
    def run(self, workflow_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run a workflow.
        
        Args:
            workflow_id: The ID of the workflow to run
            input_data: Optional input data for the workflow
            
        Returns:
            The output data from the workflow
        """
        print(f"WorkflowExecutorAgent: Running workflow {workflow_id}")
        
        # Initialize context with input data
        context = input_data or {}
        
        # Load the workflow
        workflow_path = get_workflow_path(workflow_id)
        workflow = load_workflow(workflow_path)
        
        if not workflow:
            print(f"WorkflowExecutorAgent: Workflow not found: {workflow_id}")
            return {"error": f"Workflow not found: {workflow_id}"}
        
        print(f"WorkflowExecutorAgent: Loaded workflow {workflow.id}")
        
        # Get the registry
        registry = get_registry()
        
        # Execute each step
        for i, step in enumerate(workflow.steps):
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
        for output_name, source_key in workflow.outputs.items():
            output[output_name] = context.get(source_key)
        
        # If no outputs defined, return the entire context
        if not output:
            output = context
        
        print(f"WorkflowExecutorAgent: Workflow {workflow.id} completed")
        return output