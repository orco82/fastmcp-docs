"""Tool documentation extraction from FastMCP server"""
import inspect
from typing import Any, Dict


class ToolExtractor:
    """Extract documentation information from FastMCP tools"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.tools_registry: Dict[str, Any] = {}

    async def extract_tools(self, mcp) -> Dict[str, Any]:
        """
        Extract documentation from registered MCP tools

        Args:
            mcp: The FastMCP server instance

        Returns:
            Dictionary of tool information
        """
        try:
            tool_names = await mcp.get_tools()
            if self.verbose:
                print(f"\nFound {len(tool_names)} tools to document")
        except Exception as e:
            if self.verbose:
                print(f"  ⚠ Error getting tools: {e}")
                import traceback
                traceback.print_exc()
            return {}

        if not tool_names:
            if self.verbose:
                print("  ⚠ Warning: No tools found in MCP server")
            return {}

        # Process each tool
        for tool_name in tool_names:
            try:
                tool = await mcp.get_tool(tool_name)
                tool_info = self._extract_tool_info(tool_name, tool)
                self.tools_registry[tool_name] = tool_info

                if self.verbose:
                    print(f"  ✓ Documented tool: {tool_name}")

            except Exception as e:
                if self.verbose:
                    print(f"  ⚠ Could not document tool {tool_name}: {e}")

        return self.tools_registry

    def _extract_tool_info(self, tool_name: str, tool) -> Dict[str, Any]:
        """Extract all information from a single tool"""
        if self.verbose:
            print(f"\n  Processing tool: {tool_name}")

        # Extract description
        description = ""
        if hasattr(tool, 'description'):
            description = tool.description
            if self.verbose:
                short = description.partition("\n")[0]
                print(f"  Description: {short}..." if "\n" in description else f"  Description: {description}")

        # Extract tags and title
        tags = []
        title = tool_name

        if hasattr(tool, 'tags'):
            tags = list(tool.tags) if tool.tags else []
            if self.verbose and tags:
                print(f"  Tags: {tags}")

        if hasattr(tool, 'annotations') and tool.annotations is not None:
            if hasattr(tool.annotations, 'title') and tool.annotations.title:
                title = tool.annotations.title
                if self.verbose:
                    print(f"  Title: {title}")

        # Get input schema
        input_schema = self._extract_input_schema(tool)

        # Extract parameters
        parameters = self._extract_parameters(input_schema)

        return {
            "name": tool_name,
            "title": title,
            "description": description or "No description available",
            "parameters": parameters,
            "tags": tags
        }

    def _extract_input_schema(self, tool) -> Dict[str, Any]:
        """Extract input schema from tool"""
        input_schema = {}

        # Try to get input_schema directly
        if hasattr(tool, 'input_schema'):
            input_schema = tool.input_schema
            if self.verbose:
                print(f"  Found input_schema with {len(input_schema.get('properties', {}))} properties")
            return input_schema

        if hasattr(tool, 'parameters'):
            input_schema = tool.parameters
            if self.verbose:
                print("  Found parameters schema")
            return input_schema

        # Fallback: inspect function signature
        func = self._get_underlying_function(tool)
        if func and callable(func):
            input_schema = self._build_schema_from_function(func)

        return input_schema

    def _get_underlying_function(self, tool):
        """Get the underlying function from a tool object"""
        for attr in ['fn', 'func', '_fn']:
            if hasattr(tool, attr):
                if self.verbose:
                    print(f"  Found {attr} attribute")
                return getattr(tool, attr)
        return None

    def _build_schema_from_function(self, func) -> Dict[str, Any]:
        """Build JSON schema from function signature"""
        sig = inspect.signature(func)
        if self.verbose:
            print(f"  Function has {len(sig.parameters)} parameters")

        properties = {}
        required_params = []

        for param_name, param in sig.parameters.items():
            param_type = self._get_type_from_annotation(param.annotation)
            param_default = None
            param_required = param.default == inspect.Parameter.empty

            if param.default != inspect.Parameter.empty:
                param_default = str(param.default)

            if param_required:
                required_params.append(param_name)

            properties[param_name] = {
                "type": param_type,
                "default": param_default
            }

        if self.verbose:
            print(f"  Built schema with {len(properties)} properties")

        return {
            "properties": properties,
            "required": required_params
        }

    @staticmethod
    def _get_type_from_annotation(annotation) -> str:
        """Convert Python type annotation to JSON schema type"""
        if annotation == inspect.Parameter.empty:
            return "string"

        annotation_str = str(annotation)
        type_mapping = {
            "str": "string",
            "int": "integer",
            "bool": "boolean",
            "float": "number",
            "list": "array",
            "dict": "object"
        }

        for py_type, json_type in type_mapping.items():
            if py_type in annotation_str:
                return json_type

        return "string"

    @staticmethod
    def _extract_parameters(input_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract parameter information from input schema"""
        parameters = {}

        if not isinstance(input_schema, dict):
            return parameters

        properties = input_schema.get('properties', {})
        required_params = input_schema.get('required', [])

        for param_name, param_info in properties.items():
            param_type = param_info.get('type', 'any')
            param_default = param_info.get('default')
            param_desc = param_info.get('description', '')

            parameters[param_name] = {
                "type": param_type,
                "description": param_desc,
                "default": param_default,
                "required": param_name in required_params
            }

        return parameters
