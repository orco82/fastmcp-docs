"""Configuration classes for FastMCP documentation"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class DocsLink:
    """Documentation link configuration"""
    text: str
    url: str


@dataclass
class FastMCPDocsConfig:
    """Configuration for FastMCP documentation generator"""

    # Basic information
    title: str = "MCP Tools Documentation"
    version: str = "1.0.0"
    description: str = "Auto-generated API documentation for MCP Server tools"
    base_url: str = "http://localhost:8000"

    # Additional documentation links
    docs_links: List[DocsLink] = field(default_factory=list)

    # API route paths
    api_tools_route: str = "/api/tools"
    api_tool_detail_route: str = "/api/tools/{tool_name}"
    openapi_route: str = "/openapi.json"
    docs_ui_route: str = "/docs"

    # OpenAPI configuration
    openapi_version: str = "3.1.0"
    openapi_servers: List[Dict[str, str]] = field(default_factory=lambda: [
        {"url": "http://localhost:8000", "description": "MCP Server"}
    ])

    # UI customization
    page_title_emoji: Optional[str] = None
    favicon_url: Optional[str] = None  # Custom favicon URL or path
    enable_cors: bool = True
    verbose: bool = True

    def __post_init__(self):
        """Convert dicts to DocsLink objects if needed"""
        if self.docs_links:
            self.docs_links = [
                DocsLink(**link) if isinstance(link, dict) else link
                for link in self.docs_links
            ]
