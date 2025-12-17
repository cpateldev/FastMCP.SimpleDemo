# server.py
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP("Temp Conversion MCP Server")

@mcp.tool
async def celsius_to_fahrenheit(
    celsius: Annotated[float, "Celsius unit to covert to Fahrenheit"]) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

@mcp.tool
async def fahrenheit_to_celsius(
    fahrenheit: Annotated[float, "Fahrenheit unit to covert to Celsius"]) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

if __name__ == "__main__":
    # Expose via HTTP transport and listen on port 8001    
    mcp.run(transport="http", port=8001)    