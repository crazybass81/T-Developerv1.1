import functools

def tool(func):
    """
    Decorator to mark a function as a tool.
    
    A tool is a pure function with no decision logic (0 brains).
    
    Args:
        func: The function to mark as a tool
        
    Returns:
        The decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Mark the function as a tool
    wrapper._is_tool = True
    wrapper._name = func.__name__
    wrapper._description = func.__doc__ or "No description available"
    
    return wrapper

class Tool:
    """
    Base class for tools that are implemented as classes rather than functions.
    
    A tool is a pure function with no decision logic (0 brains).
    """
    
    def run(self, input_data):
        """
        Run the tool with the given input data.
        
        Args:
            input_data: The input data for the tool
            
        Returns:
            The output data from the tool
        """
        raise NotImplementedError("Tool must implement run method")
    
    @property
    def name(self):
        """Get the name of the tool."""
        return self.__class__.__name__
    
    @property
    def description(self):
        """Get the description of the tool."""
        return self.__doc__ or "No description available"