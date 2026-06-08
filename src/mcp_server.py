import os
from fastmcp import FastMCP
from src.graph import run_calculation
from src.config import get_langfuse_handler

# Create the FastMCP Server instance
mcp = FastMCP("BODMAS_Calculation_Engine")

@mcp.tool()
def calculate_expression(expression: str) -> str:
    """
    Evaluates a string mathematical expression following BODMAS rules using a multi-agent system.
    
    Args:
        expression: The string containing numbers and operators (+, -, *, / or x, ÷).
    
    Returns:
        The evaluated numerical result as a string, or an error message if computation fails.
    """
    print(f"FastMCP received calculation request: {expression}")
    try:
        result = run_calculation(expression)
        return result
    except Exception as e:
        return f"System Error: {str(e)}"

import sys
if __name__ == "__main__":
    print("Starting FastMCP server over stdio...", file=sys.stderr)
    mcp.run()
