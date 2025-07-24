from typing import Dict, Any, List, Optional
import re
import json
import os
from tdev.core.agent import Agent
from tdev.core.workflow import Workflow
from tdev.core.registry import get_registry
from tdev.agent_core.bedrock_client import BedrockClient

class PlannerAgent(Agent):
    """
    Agent responsible for planning workflows.
    
    The PlannerAgent takes a goal and breaks it into a sequence of steps,
    selecting appropriate agents for each step. It uses AWS Bedrock to generate
    intelligent plans based on natural language goals.
    """
    
    def __init__(self):
        """Initialize the PlannerAgent."""
        super().__init__()
        self.bedrock_client = None
        try:
            self.bedrock_client = BedrockClient()
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
    
    def run(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Plan a workflow to achieve a goal.
        
        Args:
            goal: The goal to achieve
            context: Optional context information (available agents, constraints, etc.)
            
        Returns:
            A workflow definition
        """
        print(f"PlannerAgent: Planning workflow for goal: {goal}")
        
        # Get available agents from registry
        registry = get_registry()
        available_agents = registry.get_by_type("agent")
        available_tools = registry.get_by_type("tool")
        
        # Use Bedrock for intelligent planning if available
        if self.bedrock_client:
            workflow_steps = self._plan_with_bedrock(goal, available_agents, available_tools)
        else:
            # Fallback to rule-based planning
            workflow_steps = self._analyze_goal(goal, available_agents, available_tools)
        
        # Create workflow with the identified steps
        workflow = Workflow(
            id=f"goal-workflow-{self._generate_id(goal)}",
            steps=workflow_steps,
            inputs={"input": "string"},  # This could be enhanced based on first step's requirements
            outputs={"result": "output"},  # This could be enhanced based on last step's output
            description=f"Workflow for goal: {goal}"
        )
        
        # Check if we have all required agents/tools
        missing_capabilities = self._identify_missing_capabilities(workflow_steps, available_agents, available_tools)
        
        result = {
            "workflow": workflow.to_dict(),
            "missing_capabilities": missing_capabilities
        }
        
        return result
    
    def _plan_with_bedrock(self, goal: str, available_agents: List[Dict], available_tools: List[Dict]) -> List[Dict]:
        """
        Use AWS Bedrock to generate an intelligent plan for the goal.
        
        Args:
            goal: The goal to achieve
            available_agents: List of available agents
            available_tools: List of available tools
            
        Returns:
            List of workflow steps
        """
        # Prepare the prompt for Bedrock
        agent_names = [agent.get("name", str(agent)) for agent in available_agents if isinstance(agent, dict)]
        tool_names = [tool.get("name", str(tool)) for tool in available_tools if isinstance(tool, dict)]
        
        prompt = f"""You are an AI workflow planner. Your task is to create a workflow plan to achieve a goal.

Goal: {goal}

Available agents:
{', '.join(agent_names)}

Available tools:
{', '.join(tool_names)}

Create a workflow plan with 2-5 steps to achieve the goal. Each step should use one of the available agents.
For each step, specify:
1. The agent to use
2. How the input for this step relates to previous steps' outputs

Format your response as a JSON array of steps, where each step is an object with 'agent' and optionally 'input' fields.
Example: [{{'agent': 'AgentName', 'input': {{'data': '${{0.result}}'}}}}

Workflow plan:
"""
        
        try:
            # Call Bedrock to generate the plan
            model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v2")
            response = self.bedrock_client.invoke_model(
                model_id=model_id,
                prompt=prompt,
                parameters={
                    "maxTokens": 1000,
                    "temperature": 0.2,
                    "topP": 0.9
                }
            )
            
            # Extract the workflow steps from the response
            if "anthropic" in model_id.lower():
                completion = response.get("completion", "")
            else:
                completion = response.get("outputText", "")
            
            # Try to parse the JSON response
            try:
                # Find JSON array in the response
                json_start = completion.find('[')
                json_end = completion.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = completion[json_start:json_end]
                    steps = json.loads(json_str)
                    return steps
            except Exception as e:
                print(f"Error parsing Bedrock response: {e}")
                # Fall back to rule-based planning
        except Exception as e:
            print(f"Error calling Bedrock: {e}")
        
        # Fallback to rule-based planning if Bedrock fails
        return self._analyze_goal(goal, available_agents, available_tools)
    
    def _analyze_goal(self, goal: str, available_agents: List[Dict], available_tools: List[Dict]) -> List[Dict]:
        """
        Analyze the goal and break it down into steps using rule-based matching.
        
        This is a simplified implementation that uses keyword matching as a fallback
        when the Bedrock LLM is not available.
        """
        steps = []
        
        # Common patterns and corresponding agents
        patterns = [
            (r"\becho\b|\brepeat\b|\bsay\b", "EchoAgent"),
            (r"\btest\b|\bvalidate\b|\bverify\b", "AgentTesterAgent"),
            (r"\bclassify\b|\bidentify\b|\bcategorize\b", "ClassifierAgent"),
            (r"\bevaluate\b|\bscore\b|\bassess\b", "EvaluatorAgent"),
            (r"\bexecute\b|\brun\b|\bperform\b", "WorkflowExecutorAgent"),
            (r"\bgenerate\b|\bcreate\b|\bcompose\b", "AutoAgentComposerAgent"),
            # Add more patterns as needed
        ]
        
        # Check for matches in the goal
        matched_agents = []
        for pattern, agent in patterns:
            if re.search(pattern, goal.lower()):
                matched_agents.append(agent)
        
        # If no specific agents matched, use a default sequence
        if not matched_agents:
            # For data processing goals, use a standard pipeline
            if any(term in goal.lower() for term in ["data", "process", "analyze", "report"]):
                matched_agents = ["EchoAgent", "EvaluatorAgent"]
            else:
                # Default fallback
                matched_agents = ["EchoAgent"]
        
        # Convert matched agents to workflow steps
        for i, agent_name in enumerate(matched_agents):
            step = {"agent": agent_name}
            
            # If not the first step, connect input to previous step's output
            if i > 0:
                step["input"] = {"data": f"${{{i-1}.result}}"}
            
            steps.append(step)
        
        return steps
    
    def _identify_missing_capabilities(self, steps: List[Dict], available_agents: List[Dict], available_tools: List[Dict]) -> List[Dict]:
        """
        Identify any capabilities (agents/tools) that are needed but not available.
        """
        missing = []
        # Handle both registry formats - some have 'name' key, others use the key as name
        available_agent_names = []
        for agent in available_agents:
            if isinstance(agent, dict):
                # Try 'name' field first, then use the key itself
                name = agent.get("name") or agent.get("id") or str(agent)
                available_agent_names.append(name)
        
        for step in steps:
            agent_name = step.get("agent")
            if agent_name and agent_name not in available_agent_names:
                missing.append({
                    "type": "agent",
                    "name": agent_name,
                    "description": f"Agent needed for workflow step: {agent_name}"
                })
        
        return missing
    
    def _generate_id(self, goal: str) -> str:
        """
        Generate a simple ID based on the goal.
        """
        # Create a simplified slug from the goal
        slug = re.sub(r'[^\w\s]', '', goal.lower())
        slug = re.sub(r'\s+', '-', slug)[:20]  # Limit length
        return f"{slug}-{hash(goal) % 10000:04d}"