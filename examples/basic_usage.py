#!/usr/bin/env python3
"""
Basic usage example for fastmcp-docs
"""
from fastmcp import FastMCP
from fastmcp_docs import FastMCPDocs
from pydantic import BaseModel, Field
import asyncio


# Create FastMCP server
mcp = FastMCP("Example MCP Server")


# Define some example tools
@mcp.tool(tags=["greetings"])
def hello_world(name: str = "World") -> str:
    """Say hello to someone

    Args:
        name: Name of the person to greet
    """
    return f"Hello, {name}!"


class MathParams(BaseModel):
    """Parameters for math operations"""
    a: float = Field(description="First number")
    b: float = Field(description="Second number")


@mcp.tool(tags=["math"], annotations={"title": "Add Two Numbers"})
def add_numbers(params: MathParams) -> str:
    """Add two numbers together

    This tool takes two numbers and returns their sum.
    """
    result = params.a + params.b
    return f"{params.a} + {params.b} = {result}"


@mcp.tool(tags=["math"], annotations={"title": "Multiply Two Numbers"})
def multiply_numbers(params: MathParams) -> str:
    """Multiply two numbers together

    This tool takes two numbers and returns their product.
    """
    result = params.a * params.b
    return f"{params.a} × {params.b} = {result}"


class WeatherParams(BaseModel):
    """Parameters for weather lookup"""
    city: str = Field(description="City name")
    units: str = Field(default="celsius", description="Temperature units (celsius or fahrenheit)")


@mcp.tool(tags=["weather"], annotations={"title": "Get Weather"})
def get_weather(params: WeatherParams) -> str:
    """Get weather for a city

    This is a demo tool that returns mock weather data.
    """
    return f"Weather in {params.city}: 72°{params.units[0].upper()}, Sunny"


async def main():
    """Main function to setup and run server"""

    # Setup documentation
    docs = FastMCPDocs(
        mcp=mcp,
        title="Example MCP Tools",
        version="1.0.0",
        description="Example API documentation showing fastmcp-docs capabilities",
        base_url="http://localhost:8000",
        page_title_emoji="🚀",
        docs_links=[
            {"text": "GitHub", "url": "https://github.com/example/example"},
            {"text": "Documentation", "url": "https://docs.example.com"}
        ]
    )

    # Setup documentation (extracts tools and registers routes)
    await docs.setup()

    print("\n" + "=" * 60)
    print("Example MCP Server with FastMCP Docs")
    print("=" * 60)
    print("\nServer will start on http://localhost:8000")
    print("\nAvailable endpoints:")
    print("  📚 Documentation UI: http://localhost:8000/docs")
    print("  📄 OpenAPI Schema:   http://localhost:8000/openapi.json")
    print("  🔧 Tools API:        http://localhost:8000/api/tools")
    print("\n" + "=" * 60 + "\n")

    # Run server
    mcp.run(transport="sse", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    asyncio.run(main())
