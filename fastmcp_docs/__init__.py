"""FastMCP Documentation Generator

A reusable library for generating Swagger-style documentation for FastMCP servers.
"""
from .config import FastMCPDocsConfig, DocsLink
from .extractor import ToolExtractor
from .routes import RouteRegistrar
from typing import Optional, List, Dict


__version__ = "0.1.0"
__all__ = ["FastMCPDocs", "FastMCPDocsConfig", "DocsLink"]


class FastMCPDocs:
    """FastMCP Documentation Generator

    Automatically generates Swagger-style documentation for FastMCP servers.

    Example:
        ```python
        from fastmcp import FastMCP
        from fastmcp_docs import FastMCPDocs

        mcp = FastMCP("My Server")

        # Initialize documentation
        docs = FastMCPDocs(
            mcp=mcp,
            title="My MCP Tools",
            version="1.0.0",
            description="API documentation for my MCP server",
            base_url="https://api.example.com",
            page_title_emoji="🚀",
            docs_links=[
                {"text": "GitHub", "url": "https://github.com/..."},
                {"text": "Documentation", "url": "https://docs.example.com"}
            ]
        )

        # Setup documentation routes (async)
        await docs.setup()

        # Run server
        mcp.run()
        ```
    """

    def __init__(
        self,
        mcp,
        title: str = "MCP Tools Documentation",
        version: str = "1.0.0",
        description: str = "Auto-generated API documentation for MCP Server tools",
        base_url: str = "http://localhost:8000",
        docs_links: Optional[List[Dict[str, str]]] = None,
        page_title_emoji: Optional[str] = None,
        favicon_url: Optional[str] = None,
        enable_cors: bool = True,
        verbose: bool = True,
        config: Optional[FastMCPDocsConfig] = None
    ):
        """Initialize FastMCP documentation generator

        Args:
            mcp: FastMCP server instance
            title: Documentation title
            version: API version
            description: API description
            base_url: Base URL for the API
            docs_links: List of documentation links (dicts with 'text' and 'url')
            page_title_emoji: Optional emoji to display before title
            favicon_url: Custom favicon URL (default: green circle with M)
            enable_cors: Enable CORS headers
            verbose: Print verbose output during setup
            config: Optional FastMCPDocsConfig instance (overrides other params)
        """
        self.mcp = mcp

        # Create config from parameters or use provided config
        if config is None:
            self.config = FastMCPDocsConfig(
                title=title,
                version=version,
                description=description,
                base_url=base_url,
                docs_links=docs_links or [],
                page_title_emoji=page_title_emoji,
                favicon_url=favicon_url,
                enable_cors=enable_cors,
                verbose=verbose
            )
        else:
            self.config = config

        self.extractor = ToolExtractor(verbose=self.config.verbose)
        self.tools_registry = {}

    async def setup(self):
        """Setup documentation by extracting tools and registering routes

        This method should be called after all tools are registered with the MCP server.
        It's async because it needs to call async methods on the FastMCP server.

        Example:
            ```python
            import asyncio

            # After registering all tools
            asyncio.run(docs.setup())
            ```
        """
        # Extract tool documentation
        self.tools_registry = await self.extractor.extract_tools(self.mcp)

        # Register routes
        registrar = RouteRegistrar(self.mcp, self.config, self.tools_registry)
        registrar.register_all_routes()

        # if self.config.verbose:
        print("\n✓ Documentation setup complete")
        print(f"  - Documented {len(self.tools_registry)} tools")
        print(f"  - Docs UI: {self.config.base_url}{self.config.docs_ui_route}")
        print(f"  - OpenAPI: {self.config.base_url}{self.config.openapi_route}")
        print(f"  - API: {self.config.base_url}{self.config.api_tools_route}")

    def get_tools_registry(self) -> Dict:
        """Get the tools registry

        Returns:
            Dictionary of documented tools
        """
        return self.tools_registry
