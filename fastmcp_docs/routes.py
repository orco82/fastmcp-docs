"""Route registration for FastMCP documentation"""
from starlette.responses import JSONResponse, HTMLResponse, Response
from typing import Dict, Any
from .templates import get_docs_ui_template, get_default_favicon_svg
from .config import FastMCPDocsConfig


class RouteRegistrar:
    """Registers documentation routes with FastMCP server"""

    def __init__(self, mcp, config: FastMCPDocsConfig, tools_registry: Dict[str, Any]):
        self.mcp = mcp
        self.config = config
        self.tools_registry = tools_registry

    def register_all_routes(self):
        """Register all documentation routes"""
        self._register_api_tools_route()
        self._register_api_tool_detail_route()
        self._register_openapi_route()
        self._register_docs_ui_route()
        self._register_favicon_route()

        if self.config.verbose:
            print("✓ Documentation routes registered")

    def _register_api_tools_route(self):
        """Register /api/tools endpoint"""
        @self.mcp.custom_route(self.config.api_tools_route, methods=["GET"])
        async def list_all_mcp_tools(_request):
            """Get a comprehensive list of all MCP tools with their schemas"""
            return JSONResponse({
                "server": self.mcp.name,
                "total_tools": len(self.tools_registry),
                "tools": self.tools_registry
            })

    def _register_api_tool_detail_route(self):
        """Register /api/tools/{tool_name} endpoint"""
        @self.mcp.custom_route(self.config.api_tool_detail_route, methods=["GET"])
        async def get_tool_info(request):
            """Get detailed information about a specific MCP tool"""
            tool_name = request.path_params.get("tool_name")
            if tool_name not in self.tools_registry:
                return JSONResponse(
                    {"error": f"Tool '{tool_name}' not found"},
                    status_code=404
                )
            return JSONResponse(self.tools_registry[tool_name])

    def _register_openapi_route(self):
        """Register /openapi.json endpoint"""
        @self.mcp.custom_route(self.config.openapi_route, methods=["GET", "OPTIONS"])
        async def openapi_schema(request):
            """Generate OpenAPI schema for all MCP tools"""

            # Handle CORS preflight
            if request.method == "OPTIONS":
                headers = self._get_cors_headers() if self.config.enable_cors else {}
                return JSONResponse({}, headers=headers)

            # Collect all unique tags
            all_tags = set()
            for tool_info in self.tools_registry.values():
                all_tags.update(tool_info.get("tags", []))

            # Create tag definitions
            tag_definitions = [
                {
                    "name": tag,
                    "description": f"{tag.capitalize()} related tools"
                }
                for tag in sorted(all_tags)
            ]

            schema = {
                "openapi": self.config.openapi_version,
                "info": {
                    "title": self.config.title,
                    "description": self.config.description,
                    "version": self.config.version
                },
                "servers": self.config.openapi_servers,
                "tags": tag_definitions,
                "paths": self._build_openapi_paths(),
                "components": {
                    "schemas": {}
                }
            }

            headers = self._get_cors_headers() if self.config.enable_cors else {}
            return JSONResponse(schema, headers=headers)

    def _register_docs_ui_route(self):
        """Register /docs UI endpoint"""
        @self.mcp.custom_route(self.config.docs_ui_route, methods=["GET"])
        async def swagger_ui(_request):
            """Serve Swagger-style API documentation UI"""
            html_content = get_docs_ui_template(self.config)
            return HTMLResponse(content=html_content)

    def _register_favicon_route(self):
        """Register /favicon.svg endpoint (only if no custom favicon)"""
        if self.config.favicon_url is None:
            @self.mcp.custom_route("/favicon.svg", methods=["GET"])
            async def favicon(_request):
                """Serve default favicon SVG"""
                svg_content = get_default_favicon_svg()
                return Response(
                    content=svg_content,
                    media_type="image/svg+xml",
                    headers={"Cache-Control": "public, max-age=86400"}
                )

    def _build_openapi_paths(self) -> Dict[str, Any]:
        """Build OpenAPI paths from tools registry"""
        paths = {
            self.config.api_tools_route: {
                "get": {
                    "summary": "List all MCP tools",
                    "description": "Get a comprehensive list of all MCP tools with their schemas",
                    "operationId": "list_all_mcp_tools",
                    "tags": ["MCP Tools"],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "server": {"type": "string"},
                                            "total_tools": {"type": "integer"},
                                            "tools": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        # Add tool endpoints
        for tool_name, tool_info in self.tools_registry.items():
            path = self.config.api_tool_detail_route.replace("{tool_name}", tool_name)

            tool_tags = tool_info.get("tags", [])
            if not tool_tags:
                tool_tags = ["Tools"]

            summary = tool_info.get("title", f"Get {tool_name} tool info")

            paths[path] = {
                "get": {
                    "summary": summary,
                    "description": tool_info.get("description", ""),
                    "operationId": f"get_tool_{tool_name}",
                    "tags": tool_tags,
                    "responses": {
                        "200": {
                            "description": "Tool information",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "title": {"type": "string"},
                                            "description": {"type": "string"},
                                            "parameters": {"type": "object"},
                                            "tags": {"type": "array", "items": {"type": "string"}}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

        return paths

    @staticmethod
    def _get_cors_headers() -> Dict[str, str]:
        """Get CORS headers"""
        return {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
