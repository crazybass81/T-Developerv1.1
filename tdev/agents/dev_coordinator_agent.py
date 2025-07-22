"""
DevCoordinator Agent - The central orchestrator for T-Developer using Agent Squad.

This agent coordinates the core agents (Classifier, Planner, Evaluator, WorkflowExecutor)
to fulfill user requests end-to-end, replacing the legacy MetaAgent.
"""
from typing import Dict, Any, List, Optional
import asyncio

from tdev.core.agent import Agent
from tdev.core.registry import get_registry
from tdev.agent_squad.agents import Agent as SquadAgent, AgentOptions, SupervisorAgent, SupervisorAgentOptions, BedrockAgent
from tdev.agent_squad.wrappers import SquadWrapperAgent


class DevCoordinatorAgent(Agent):
    """
    The central orchestrator that coordinates other agents using Agent Squad.
    
    This agent replaces the legacy MetaAgent and OrchestratorTeam, using
    Agent Squad's SupervisorAgent to coordinate the core agents.
    """
    
    def __init__(self):
        """Initialize the DevCoordinatorAgent."""
        self.registry = get_registry()
        self.supervisor = self._create_supervisor()
    
    def _create_supervisor(self):
        """Create a SupervisorAgent with the core T-Developer agents."""
        # Create a lead agent (in a real implementation, this would be a Bedrock LLM)
        lead_agent = BedrockAgent(
            AgentOptions(
                name="LeadAgent",
                description="The lead agent that coordinates the team"
            )
        )
        
        # Wrap the core T-Developer agents
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
            description="Coordinates T-Developer workflow (Classifier->Planner->Evaluator->Executor)",
            lead_agent=lead_agent,
            team=wrapped_agents
        )
        
        return SupervisorAgent(options)
    
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
        # Extract request details
        goal = request.get("goal", "")
        code = request.get("code")
        options = request.get("options", {})
        
        # Prepare the input for the supervisor
        input_text = f"Goal: {goal}"
        if code:
            input_text += f"\nCode: {code}"
        
        additional_params = {"options": options}
        
        # Run the supervisor asynchronously
        try:
            # Create an event loop if one doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the supervisor
            result = loop.run_until_complete(
                self.supervisor.process_request(
                    input_text=input_text,
                    additional_params=additional_params
                )
            )
            
            # Extract the result
            return {
                "success": True,
                "result": result.get("text", ""),
                "context": result.get("context", {})
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
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