"""
MetaAgent (Orchestrator) - The central orchestrator for T-Developer.

This agent coordinates the core agents (Classifier, Planner, Evaluator, WorkflowExecutor)
to fulfill user requests end-to-end.
"""
from typing import Dict, Any, Optional, Union, List
import json

from tdev.core.agent import Agent
from tdev.core.registry import get_registry

class MetaAgent(Agent):
    """
    The central orchestrator that coordinates other agents to fulfill user requests.
    
    This agent implements the orchestration logic described in the Agent Squad Architecture.
    """
    
    def __init__(self):
        """Initialize the MetaAgent."""
        self.registry = get_registry()
    
    def run(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user request by orchestrating the appropriate agents.
        
        Args:
            request: A dictionary containing the user request:
                - goal: The user's goal or request
                - code: Optional code to classify
                - options: Optional configuration options
                
        Returns:
            A dictionary containing the result of processing the request:
                - success: Whether the request was successfully processed
                - result: The final output
                - workflow_id: ID of the workflow that was executed
                - steps: List of steps that were executed
        """
        goal = request.get("goal", "")
        code = request.get("code")
        options = request.get("options", {})
        
        # Step 1: If code is provided, classify it
        classification_result = None
        if code:
            classifier = self.registry.get_instance("ClassifierAgent")
            if classifier:
                classification_result = classifier.run(code)
                print(f"Classification result: {classification_result}")
        
        # Step 2: Plan a workflow to fulfill the goal
        planner = self.registry.get_instance("PlannerAgent")
        if not planner:
            return {"success": False, "error": "PlannerAgent not found"}
        
        planning_input = {
            "goal": goal,
            "classification": classification_result,
            "options": options
        }
        
        workflow_plan = planner.run(planning_input)
        print(f"Workflow plan: {workflow_plan}")
        
        # Step 3: Evaluate the workflow plan
        evaluator = self.registry.get_instance("EvaluatorAgent")
        if evaluator:
            evaluation = evaluator.run(workflow_plan)
            print(f"Evaluation: {evaluation}")
            
            # If the evaluation score is below threshold, request refinement
            if evaluation.get("score", 0) < 0.7:  # Threshold for acceptance
                print("Workflow plan needs refinement")
                # Request refinement from the planner
                planning_input["feedback"] = evaluation.get("feedback", [])
                workflow_plan = planner.run(planning_input)
                print(f"Refined workflow plan: {workflow_plan}")
        
        # Step 4: Execute the workflow
        executor = self.registry.get_instance("WorkflowExecutorAgent")
        if not executor:
            return {"success": False, "error": "WorkflowExecutorAgent not found"}
        
        execution_result = executor.run(workflow_plan)
        print(f"Execution result: {execution_result}")
        
        # Step 5: Return the final result
        return {
            "success": True,
            "result": execution_result.get("result"),
            "workflow_id": workflow_plan.get("id"),
            "steps": execution_result.get("steps", [])
        }
    
    def handle_missing_capability(self, capability_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a missing capability by generating a new agent.
        
        This method is called when the PlannerAgent identifies a missing capability.
        It uses the AutoAgentComposer to generate a new agent that fulfills the requirement.
        
        Args:
            capability_spec: Specification of the required capability
                
        Returns:
            Result of the agent generation
        """
        composer = self.registry.get_instance("AutoAgentComposerAgent")
        if not composer:
            return {"success": False, "error": "AutoAgentComposerAgent not found"}
        
        # Generate the new agent
        result = composer.run(capability_spec)
        
        return result