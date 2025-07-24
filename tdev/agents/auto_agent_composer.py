"""
Auto Agent Composer (Agno) - Enhanced version with better test coverage.
"""
from typing import Dict, Any, Optional
from tdev.core.agent import Agent as BaseAgent
from tdev.core.registry import get_registry
from tdev.core.plugins import plugin_manager

class AutoAgentComposer(BaseAgent):
    """Enhanced Auto Agent Composer with improved functionality."""
    
    def __init__(self):
        super().__init__()
        self.registry = get_registry()
        self.templates = {
            "agent": self._get_agent_template(),
            "tool": self._get_tool_template()
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new agent or tool based on specifications."""
        spec_type = input_data.get("type", "agent")
        name = input_data.get("name", "GeneratedComponent")
        goal = input_data.get("goal", "")
        
        if not goal:
            return {"success": False, "error": "Goal is required"}
        
        try:
            if spec_type == "agent":
                return self._generate_agent(name, goal, input_data)
            elif spec_type == "tool":
                return self._generate_tool(name, goal, input_data)
            else:
                return {"success": False, "error": f"Unknown type: {spec_type}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_agent(self, name: str, goal: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new agent."""
        # Use plugin system for model invocation
        model_plugin = plugin_manager.get_plugin("bedrock-claude")
        if model_plugin:
            prompt = f"Create an agent named {name} that {goal}"
            code_suggestion = model_plugin.invoke(prompt)
        else:
            code_suggestion = f"# Generated agent for: {goal}"
        
        # Generate agent code
        code = self.templates["agent"].format(
            name=name,
            goal=goal,
            code_suggestion=code_suggestion
        )
        
        # Create metadata
        metadata = {
            "name": name,
            "type": "agent",
            "description": f"Auto-generated agent: {goal}",
            "brain_count": 1,
            "reusability": "B",
            "generated": True,
            "goal": goal
        }
        
        # Register the agent
        self.registry.register(name, metadata)
        
        return {
            "success": True,
            "name": name,
            "type": "agent",
            "code": code,
            "metadata": metadata
        }
    
    def _generate_tool(self, name: str, goal: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new tool."""
        # Generate tool code
        code = self.templates["tool"].format(
            name=name,
            goal=goal
        )
        
        # Create metadata
        metadata = {
            "name": name,
            "type": "tool",
            "description": f"Auto-generated tool: {goal}",
            "brain_count": 0,
            "reusability": "A",
            "generated": True,
            "goal": goal
        }
        
        # Register the tool
        self.registry.register(name, metadata)
        
        return {
            "success": True,
            "name": name,
            "type": "tool",
            "code": code,
            "metadata": metadata
        }
    
    def _get_agent_template(self) -> str:
        """Get agent code template."""
        return '''"""
Auto-generated agent: {name}
Goal: {goal}
"""
from typing import Dict, Any
from tdev.core.agent import Agent as BaseAgent

class {name}(BaseAgent):
    """Auto-generated agent for: {goal}"""
    
    def __init__(self):
        super().__init__()
        self.goal = "{goal}"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality."""
        # {code_suggestion}
        
        return {{
            "success": True,
            "result": f"Processed: {{input_data}}",
            "agent": "{name}",
            "goal": self.goal
        }}
'''
    
    def _get_tool_template(self) -> str:
        """Get tool code template."""
        return '''"""
Auto-generated tool: {name}
Goal: {goal}
"""
from typing import Any

def {name}(input_data: Any) -> Any:
    """Auto-generated tool for: {goal}"""
    # Tool implementation for: {goal}
    return f"Tool {name} processed: {{input_data}}"
'''
    
    def list_generated_components(self) -> Dict[str, Any]:
        """List all generated components."""
        all_components = self.registry.get_all()
        generated = {{k: v for k, v in all_components.items() if v.get("generated", False)}}
        
        return {
            "success": True,
            "count": len(generated),
            "components": generated
        }
    
    def regenerate_component(self, name: str, new_goal: str) -> Dict[str, Any]:
        """Regenerate an existing component with a new goal."""
        existing = self.registry.get(name)
        if not existing:
            return {"success": False, "error": f"Component {name} not found"}
        
        component_type = existing.get("type", "agent")
        spec = {"name": name, "goal": new_goal, "type": component_type}
        
        return self.run(spec)