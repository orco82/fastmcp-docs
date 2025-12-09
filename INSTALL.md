# Installation Guide

## Quick Install

From the devops_mcp_server directory:

```bash
pip install -e ./fastmcp-docs
```

## Verify Installation

```bash
python -c "from fastmcp_docs import FastMCPDocs; print('FastMCP Docs installed successfully!')"
```

## Usage in Your Project

After installation, you can import and use the library:

```python
from fastmcp_docs import FastMCPDocs

# In your server.py or main file
docs = FastMCPDocs(mcp, title="My Tools")
await docs.setup()
```

## Development Installation

If you want to contribute or modify the library:

```bash
# Install with development dependencies
pip install -e "./fastmcp-docs[dev]"

# Run tests
cd fastmcp-docs
pytest

# Format code
black fastmcp_docs/
```

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError: No module named 'fastmcp_docs'`:

1. Make sure you're in the correct directory
2. Re-run the installation: `pip install -e ./fastmcp-docs`
3. Check that fastmcp-docs directory exists

### FastMCP Not Found

If you get `ModuleNotFoundError: No module named 'fastmcp'`:

```bash
pip install fastmcp
```

### Starlette Not Found

If you get `ModuleNotFoundError: No module named 'starlette'`:

```bash
pip install starlette
```

## Uninstall

```bash
pip uninstall fastmcp-docs
```
