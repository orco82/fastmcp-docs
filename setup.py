"""Setup configuration for fastmcp-docs package"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="fastmcp-docs",
    version="0.1.0",
    author="CDC DevOps Team",
    author_email="orco82@gmail.com",
    description="Swagger-style documentation generator for FastMCP servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orco82/fastmcp-docs",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastmcp>=0.1.0",
        "starlette>=0.27.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "mypy>=1.0",
        ],
    },
    keywords="fastmcp documentation swagger openapi api-docs mcp",
    project_urls={
        "Bug Reports": "https://github.com/orco82/fastmcp-docs/issues",
        "Source": "https://github.com/orco82/fastmcp-docs",
        "Documentation": "https://github.com/orco82/fastmcp-docs/blob/main/README.md",
    },
)
