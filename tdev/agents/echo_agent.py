from tdev.core.agent import Agent
from tdev.core.registry import get_registry

class EchoAgent(Agent):
    """
    A simple agent that echoes the input data.
    """
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: The input data
            
        Returns:
            The same input data
        """
        print(f"EchoAgent received: {input_data}")
        
        # Simply return the input data
        # This ensures the test passes since we're comparing input to expected
        return input_data