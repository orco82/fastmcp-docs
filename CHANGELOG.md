# Changelog

## [0.1.0] - 2025-12-10

### Added
- Initial release of fastmcp-docs library
- `FastMCPDocs` main class for easy integration
- `FastMCPDocsConfig` for comprehensive configuration
- Automatic tool documentation extraction from FastMCP servers
- Swagger-style UI with modern design
- OpenAPI 3.1.0 schema generation
- Tag-based tool organization
- Search functionality across tools
- Support for parameter descriptions via Pydantic Field
- CORS support
- Customizable page title with emoji support
- Documentation links support
- Comprehensive README with examples
- Basic usage example
- Installation guide

### Features
- Clean separation of concerns (config, extractor, routes, templates)
- Full type hints throughout codebase
- Async/await support
- Configurable route paths
- Verbose logging option
- Multiple OpenAPI server definitions
- Auto-detection of tool metadata (name, title, description, tags, parameters)
- Fallback to function signature inspection
- Parameter type detection
- Required/optional parameter handling
- Default value extraction

### Documentation
- Complete README.md with usage examples
- INSTALL.md with installation instructions
- PACKAGE_SUMMARY.md with architecture overview
- Inline docstrings for all classes and functions
- Working example in examples/basic_usage.py

### Integration
- Successfully integrated with existing devops_mcp_server
- Replaced docs_api.py with cleaner library approach
- Updated server.py to use new library
