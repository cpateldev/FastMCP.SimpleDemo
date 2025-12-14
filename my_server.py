# server.py
from fastmcp import FastMCP

mcp = FastMCP("Temp Conversion MCP Server")

@mcp.tool
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

@mcp.tool
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

if __name__ == "__main__":
    # Expose via HTTP transport
    #mcp.run(host="0.0.0.0", port=8000)
    mcp.run(transport="http", port=8000)