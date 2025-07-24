from tdev.core.agent import Agent

class TestEchoAgent(Agent):
    """
    A test agent that echoes the input data
    """
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: Any data to echo
            
        Returns:
            The same data that was provided as input
        """
        # TODO: Implement agent logic
        result = input_data  # Simple echo implementation
        return result
