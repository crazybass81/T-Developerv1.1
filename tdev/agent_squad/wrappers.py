"""
Wrapper classes for integrating T-Developer agents with Agent Squad.

This module provides wrapper classes that adapt T-Developer agents
to the Agent Squad interface.
"""
from typing import Dict, Any, List, Optional

from tdev.agent_squad.agents import Agent, AgentOptions
from tdev.core.agent import Agent as TDevAgent
from tdev.core.tool import Tool as TDevTool


class SquadWrapperAgent(Agent):
    """
    Wrapper that adapts a T-Developer agent to the Agent Squad interface.
    
    This wrapper encapsulates a T-Developer agent and exposes it as an
    Agent Squad agent, bridging the two interfaces.
    """
    
    def __init__(self, tdev_agent: TDevAgent):
        """
        Initialize the wrapper with a T-Developer agent.
        
        Args:
            tdev_agent: The T-Developer agent to wrap
        """
        opts = AgentOptions(
            name=tdev_agent.name,
            description=tdev_agent.description
        )
        super().__init__(opts)
        self._tdev_agent = tdev_agent
    
    async def process_request(self, input_text: str, user_id: str = None, 
                             session_id: str = None, chat_history: List[Dict] = None, 
                             additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a request by delegating to the wrapped T-Developer agent.
        
        Args:
            input_text: The input text from the user
            user_id: Optional user identifier
            session_id: Optional session identifier
            chat_history: Optional chat history
            additional_params: Optional additional parameters
            
        Returns:
            A dictionary containing the response
        """
        # Convert input to the format expected by the T-Developer agent
        # This might need to be customized based on the specific agent
        
        # For now, we'll just pass the input text directly
        result = self._tdev_agent.run(input_text)
        
        # Convert the result to the format expected by Agent Squad
        if isinstance(result, dict):
            # If the result is already a dict, return it with a text field
            if "text" not in result:
                result["text"] = str(result)
            return result
        else:
            # Otherwise, wrap the result in a dict
            return {"text": str(result)}


class SquadWrapperTool:
    """
    Wrapper that adapts a T-Developer tool to the Agent Squad tool interface.
    
    This wrapper encapsulates a T-Developer tool and exposes it as an
    Agent Squad tool, bridging the two interfaces.
    """
    
    def __init__(self, name: str, description: str, tdev_tool_func):
        """
        Initialize the wrapper with a T-Developer tool function.
        
        Args:
            name: The name of the tool
            description: A description of the tool
            tdev_tool_func: The T-Developer tool function to wrap
        """
        self.name = name
        self.description = description
        self._tdev_tool_func = tdev_tool_func
    
    async def execute(self, **kwargs) -> Any:
        """
        Execute the wrapped T-Developer tool function.
        
        Args:
            **kwargs: Arguments to pass to the tool function
            
        Returns:
            The result of the tool function
        """
        # Call the T-Developer tool function
        return self._tdev_tool_func(**kwargs)