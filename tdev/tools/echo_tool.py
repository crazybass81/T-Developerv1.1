from tdev.core.tool import tool

@tool
def echo_tool(input_data):
    """
    A simple tool that returns the input data unchanged.
    
    Args:
        input_data: The input data
        
    Returns:
        The same input data
    """
    return input_data