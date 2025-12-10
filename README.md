# FastMCP Docs

Swagger-style documentation generator for FastMCP servers. Automatically creates beautiful, interactive API documentation from your FastMCP tools.

## Features

- 🎨 **Swagger-Style UI** - Clean, modern interface similar to Swagger UI
- 🔍 **Search Functionality** - Quickly find tools by name, description, or tags
- 🏷️ **Tag-Based Organization** - Tools grouped by tags for easy navigation
- 📝 **Auto-Generated** - Extracts documentation from your FastMCP tools automatically
- ⚙️ **Highly Configurable** - Customize title, description, links, and more
- 🚀 **Easy Integration** - Simple 3-line setup
- 📚 **OpenAPI Compatible** - Generates OpenAPI 3.1.0 schema

## Installation

```bash
pip install fastmcp-docs
```

## Quick Start

```python
from fastmcp import FastMCP
from fastmcp_docs import FastMCPDocs
import asyncio

# Create your FastMCP server
mcp = FastMCP("My MCP Server")

# Register your tools
@mcp.tool(tags=["example"])
def hello_world(name: str = "World"):
    """Say hello to someone"""
    return f"Hello, {name}!"

# Setup documentation (3 lines!)
docs = FastMCPDocs(mcp, title="My MCP Tools")
asyncio.run(docs.setup())

# Run server
mcp.run()
```

That's it! Your documentation is now available at:
- **UI**: http://localhost:8000/docs
- **OpenAPI**: http://localhost:8000/openapi.json
- **Tools API**: http://localhost:8000/api/tools

## Configuration

### Basic Configuration

```python
from fastmcp_docs import FastMCPDocs

docs = FastMCPDocs(
    mcp=mcp,
    title="My MCP Tools",
    version="1.0.0",
    description="API documentation for my awesome MCP server",
    base_url="https://api.example.com",
    page_title_emoji="🚀"
)
```

### Adding Documentation Links

```python
docs = FastMCPDocs(
    mcp=mcp,
    title="My MCP Tools",
    docs_links=[
        {"text": "GitHub Repository", "url": "https://github.com/..."},
        {"text": "User Guide", "url": "https://docs.example.com"},
        {"text": "API Reference", "url": "https://api.example.com/reference"}
    ]
)
```

### Advanced Configuration

```python
from fastmcp_docs import FastMCPDocs, FastMCPDocsConfig, DocsLink

# Create custom configuration
config = FastMCPDocsConfig(
    title="My MCP Tools",
    version="2.0.0",
    description="Advanced API documentation",
    base_url="https://api.example.com",
    docs_links=[
        DocsLink(text="GitHub", url="https://github.com/..."),
        DocsLink(text="Docs", url="https://docs.example.com")
    ],
    page_title_emoji="🤖",

    # Customize route paths
    api_tools_route="/api/tools",
    openapi_route="/openapi.json",
    docs_ui_route="/docs",

    # OpenAPI settings
    openapi_version="3.1.0",
    openapi_servers=[
        {"url": "https://api.example.com", "description": "Production"},
        {"url": "https://staging.example.com", "description": "Staging"}
    ],

    # Options
    enable_cors=True,
    verbose=True
)

# Use custom config
docs = FastMCPDocs(mcp, config=config)
```

## Adding Descriptions to Tool Parameters

To get parameter descriptions in the documentation, use Pydantic models:

```python
from typing import Annotated

@mcp.tool(tags=["greetings"])
def greet(
    name: Annotated[str, "Name of the person to greet"],
    greeting: Annotated[str, "Greeting to use"] = "Hello"
) -> str:
    """Greet someone with a custom message"""
    return f"{greeting}, {name}!"
```

## Complete Example

```python
from fastmcp import FastMCP
from fastmcp_docs import FastMCPDocs
from typing import Annotated
import asyncio

# Create server
mcp = FastMCP("My MCP Server")


@mcp.tool(tags=["deployment"], annotations={"title": "Deploy Application"})
def deploy(
    environment: Annotated[str, "Target environment (dev, staging, prod)"],
    version: Annotated[str, "Version to deploy"],
    dry_run: Annotated[bool = "Perform dry run without actual deployment"] = False
) -> str:
    """Deploy application to specified environment

    This tool deploys the application to the target environment
    with the specified version. Use dry_run to test without deploying.
    """
    if dry_run:
        return f"DRY RUN: Would deploy v{version} to {environment}"
    return f"Deployed v{version} to {environment}"

# Setup documentation
docs = FastMCPDocs(
    mcp=mcp,
    title="My FastMCP Tools",
    version="1.0.0",
    description="This is my FastMCP Tools Documention",
    base_url="https://mcp.example.com",
    page_title_emoji="🛠️",
    docs_links=[
        {"text": "Tools Guide", "url": "https://docs.example.com/tools-guide"}
    ]
)

# Run setup
asyncio.run(docs.setup())

# Start server
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

## API Routes

FastMCP Docs automatically creates the following routes:

| Route | Description |
|-------|-------------|
| `/docs` | Interactive Swagger-style UI |
| `/openapi.json` | OpenAPI 3.1.0 schema |
| `/api/tools` | List all tools with metadata |
| `/api/tools/{tool_name}` | Get specific tool details |

## Development

### Local Installation

```bash
# Clone repository
git clone https://github.com/orco82/fastmcp-docs.git
cd fastmcp-docs

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black fastmcp_docs/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues and questions:
- GitHub Issues: https://github.com/orco82/fastmcp-docs/issues
- Documentation: https://github.com/orco82/fastmcp-docs/blob/main/README.md
