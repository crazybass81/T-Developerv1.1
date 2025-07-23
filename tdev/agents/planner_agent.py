from typing import Dict, Any, List, Optional
import re
import json
from tdev.core.agent import Agent
from tdev.core.workflow import Workflow
from tdev.core.registry import get_registry

class PlannerAgent(Agent):
    """
    Agent responsible for planning workflows.
    
    The PlannerAgent takes a goal and breaks it into a sequence of steps,
    selecting appropriate agents for each step.
    """
    
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
        
        # Parse the goal to identify key tasks and required capabilities
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
    
    def _analyze_goal(self, goal: str, available_agents: List[Dict], available_tools: List[Dict]) -> List[Dict]:
        """
        Analyze the goal and break it down into steps.
        
        This is a simplified implementation that uses keyword matching.
        In a production system, this would use an LLM to analyze the goal.
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
        available_agent_names = [agent["name"] for agent in available_agents]
        
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