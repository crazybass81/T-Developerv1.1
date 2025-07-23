"""
DevCoordinator Agent - The central orchestrator for T-Developer using Agent Squad.

This agent coordinates the core agents (Classifier, Planner, Evaluator, WorkflowExecutor)
to fulfill user requests end-to-end, replacing the legacy MetaAgent.
"""
from typing import Dict, Any, List, Optional
import asyncio
import os
import json

from tdev.core.agent import Agent
from tdev.core.registry import get_registry
from tdev.agent_squad.agents import Agent as SquadAgent, AgentOptions, SupervisorAgent, SupervisorAgentOptions, BedrockAgent
from tdev.agent_squad.wrappers import SquadWrapperAgent
from tdev.agent_core.bedrock_client import BedrockClient


class DevCoordinatorAgent(Agent):
    """
    The central orchestrator that coordinates other agents using Agent Squad.
    
    This agent replaces the legacy MetaAgent and OrchestratorTeam, using
    Agent Squad's SupervisorAgent to coordinate the core agents.
    """
    
    def __init__(self):
        """Initialize the DevCoordinatorAgent."""
        self.registry = get_registry()
        self.bedrock_client = None
        try:
            self.bedrock_client = BedrockClient()
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
        self.supervisor = self._create_supervisor()
    
    def _create_supervisor(self):
        """Create a SupervisorAgent with the core T-Developer agents."""
        # Create a lead agent using Bedrock if available
        if self.bedrock_client:
            # Use a real Bedrock agent
            model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v2")
            lead_agent = BedrockAgent(
                AgentOptions(
                    name="LeadAgent",
                    description="The lead agent that coordinates the team"
                ),
                model_id=model_id
            )
        else:
            # Use a mock Bedrock agent
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
        
        # If code is provided, classify it first
        if code:
            return self._handle_code_request(code, options)
        
        # Otherwise, handle as a goal-based request
        return self._handle_goal_request(goal, options)
    
    def _handle_code_request(self, code: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request with code to classify.
        """
        classifier = self.registry.get_instance("ClassifierAgent")
        if not classifier:
            return {"success": False, "error": "ClassifierAgent not found"}
        
        # Classify the code
        classification = classifier.run({"code": code})
        
        return {
            "success": True,
            "result": classification,
            "type": "classification"
        }
    
    def _handle_goal_request(self, goal: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a goal-based request by planning and executing a workflow.
        """
        # Step 1: Plan a workflow
        planner = self.registry.get_instance("PlannerAgent")
        if not planner:
            return {"success": False, "error": "PlannerAgent not found"}
        
        planning_result = planner.run(goal)
        workflow = planning_result.get("workflow")
        missing_capabilities = planning_result.get("missing_capabilities", [])
        
        # Step 2: Handle any missing capabilities
        if missing_capabilities:
            print(f"Found {len(missing_capabilities)} missing capabilities. Generating them...")
            for capability in missing_capabilities:
                # Enhance the capability spec with more details using Bedrock if available
                if self.bedrock_client:
                    capability = self._enhance_capability_spec(capability, goal)
                
                # Generate the capability
                generation_result = self.handle_missing_capability(capability)
                if not generation_result.get("success", False):
                    return {
                        "success": False,
                        "error": f"Failed to generate capability: {capability['name']}",
                        "details": generation_result
                    }
                print(f"Successfully generated capability: {capability['name']}")
            
            # Re-plan with the new capabilities
            planning_result = planner.run(goal)
            workflow = planning_result.get("workflow")
        
        # Step 3: Evaluate the workflow
        evaluator = self.registry.get_instance("EvaluatorAgent")
        if not evaluator:
            return {"success": False, "error": "EvaluatorAgent not found"}
        
        evaluation = evaluator.run(workflow)
        
        # Step 4: If evaluation score is too low, refine the plan
        if evaluation.get("needs_improvement", False):
            print(f"Workflow needs improvement. Score: {evaluation.get('score')}")
            print(f"Suggestions: {evaluation.get('suggestions')}")
            
            # In a more advanced implementation, we would refine the plan here
            # For now, we'll proceed with the original plan
            pass
        
        # Step 5: Execute the workflow
        executor = self.registry.get_instance("WorkflowExecutorAgent")
        if not executor:
            return {"success": False, "error": "WorkflowExecutorAgent not found"}
        
        # Prepare input data
        input_data = options.get("input", {"input": goal})
        
        # Execute the workflow
        execution_result = executor.run({
            "workflow": workflow,
            "input": input_data
        })
        
        # Return the final result
        return {
            "success": True,
            "result": execution_result.get("output"),
            "workflow_id": workflow.get("id"),
            "steps": execution_result.get("steps", []),
            "evaluation": evaluation,
            "type": "workflow_execution"
        }
        
    def _run_with_supervisor(self, input_text: str, additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the request through the Agent Squad supervisor.
        """
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
    
    def _enhance_capability_spec(self, capability_spec: Dict[str, Any], goal: str) -> Dict[str, Any]:
        """
        Enhance a capability specification with more details using Bedrock.
        
        Args:
            capability_spec: Basic specification of the required capability
            goal: The overall goal that this capability will help achieve
            
        Returns:
            Enhanced capability specification
        """
        if not self.bedrock_client:
            return capability_spec
        
        try:
            # Prepare the prompt for Bedrock
            prompt = f"""You are an AI agent designer. Your task is to enhance a specification for a new AI agent.

Overall Goal: {goal}

Basic Agent Specification:
- Type: {capability_spec.get('type', 'agent')}
- Name: {capability_spec.get('name', 'Unknown')}
- Description: {capability_spec.get('description', 'No description')}

Please enhance this specification by providing:
1. A more detailed description of what this agent should do
2. What inputs the agent should accept
3. What outputs the agent should produce
4. Any tools or libraries the agent might need
5. Implementation hints for the agent's logic

Format your response as a JSON object with the following fields:
- description: Detailed description
- input: Description of input data
- output: Description of output data
- tools: Array of tool names or libraries
- implementation_hints: Hints for implementation

Enhanced Specification:
"""
            
            # Call Bedrock to enhance the specification
            model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v2")
            response = self.bedrock_client.invoke_model(
                model_id=model_id,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.4,
                top_p=0.9
            )
            
            # Extract the enhanced specification from the response
            if "anthropic" in model_id.lower():
                completion = response.get("completion", "")
            else:
                completion = response.get("outputText", "")
            
            # Try to parse the JSON response
            try:
                # Find JSON object in the response
                json_start = completion.find('{')
                json_end = completion.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = completion[json_start:json_end]
                    enhanced_spec = json.loads(json_str)
                    
                    # Merge the enhanced spec with the original spec
                    for key, value in enhanced_spec.items():
                        if key not in capability_spec or not capability_spec[key]:
                            capability_spec[key] = value
            except Exception as e:
                print(f"Error parsing enhanced specification: {e}")
        except Exception as e:
            print(f"Error enhancing capability specification: {e}")
        
        return capability_spec
    
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
        
        # If generation was successful, test the new agent
        if result.get("success", False):
            agent_name = result.get("metadata", {}).get("name")
            if agent_name:
                tester = self.registry.get_instance("AgentTesterAgent")
                if tester:
                    print(f"Testing newly generated agent: {agent_name}")
                    test_result = tester.run(agent_name)
                    result["test_result"] = test_result
        
        return result