from abc import ABC, abstractmethod

class Agent(ABC):
    """
    Base class for all agents in T-Developer.
    
    An agent has a single decision point (1 brain) and performs a specific role.
    It may use tools internally.
    """
    
    @abstractmethod
    def run(self, input_data):
        """
        Run the agent with the given input data.
        
        Args:
            input_data: The input data for the agent
            
        Returns:
            The output data from the agent
        """
        raise NotImplementedError("Agent must implement run method")
    
    @property
    def name(self):
        """Get the name of the agent."""
        return self.__class__.__name__
    
    @property
    def description(self):
        """Get the description of the agent."""
        return self.__doc__ or "No description available"