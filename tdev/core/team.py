from abc import ABC, abstractmethod
from tdev.core.agent import Agent

class Team(Agent):
    """
    Base class for teams in T-Developer.
    
    A team is a composite agent with multiple decision points (2+ brains)
    and internal coordination logic.
    """
    
    def __init__(self):
        """Initialize the team."""
        self.agents = {}
    
    def add_agent(self, name, agent):
        """
        Add an agent to the team.
        
        Args:
            name: The name to assign to the agent within the team
            agent: The agent instance
        """
        self.agents[name] = agent
    
    @abstractmethod
    def run(self, input_data):
        """
        Run the team with the given input data.
        
        Args:
            input_data: The input data for the team
            
        Returns:
            The output data from the team
        """
        raise NotImplementedError("Team must implement run method")