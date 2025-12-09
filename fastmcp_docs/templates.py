"""HTML templates for FastMCP documentation UI"""


def get_docs_ui_template(config) -> str:
    """Generate the HTML documentation UI

    Args:
        config: FastMCPDocsConfig instance with configuration

    Returns:
        Complete HTML template string
    """
    title_with_emoji = f"{config.page_title_emoji} {config.title}" if config.page_title_emoji else config.title

    # Build documentation links HTML
    docs_links_html = ""
    if config.docs_links:
        links_items = "\n".join([
            f'<li><a href="{link.url}">{link.text}</a></li>'
            for link in config.docs_links
        ])
        docs_links_html = f"""
        <p style="margin-bottom:0px;"><strong>Documentation:</strong></p>
        <ul style="margin-left: 20px;">
            {links_items}
        </ul>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config.title}</title>
    <style>{_get_css()}</style>
</head>
<body>
    <div class="swagger-ui">
        <div class="header">
            <div class="header-content">
                <h1>{title_with_emoji}</h1>
                <div class="version">Version {config.version}</div>
            </div>
        </div>

        <div class="info">
            <p>{config.description}</p>
            <p style="margin-bottom:0px;"><strong>Base URL:</strong> {config.base_url}</p>
            {docs_links_html}
        </div>

        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search operations...">
        </div>

        <div id="tagsContainer">
            <div class="loading">Loading tools...</div>
        </div>
    </div>

    <script>{_get_javascript(config)}</script>
</body>
</html>"""


def _get_css() -> str:
    """Get CSS styles for the documentation UI"""
    return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: sans-serif;
    color: #3b4151;
}

.swagger-ui {
    max-width: 1460px;
    margin: 0 auto;
}

.header {
    background: #fff;
    padding: 50px 0px 20px;
}

.header-content {
    max-width: 1460px;
    margin: 0 auto;
    padding: 0 20px;
}

.header h1 {
    font-size: 36px;
    margin-bottom: 0px;
    color: #3b4151;
}

.header .version {
    color: #3b4151;
    font-size: 14px;
}

.info {
    padding: 0 20px;
    font-size: 14px;
}

.info p {
    line-height: 1.6;
    margin-bottom: 10px;
}

.search-box {
    background: #fff;
    padding: 7px 20px;
    margin: 20px;
    border-radius: 4px;
    border: 1px solid #d3d3d3;
}

.search-box input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: unset;
    outline: none;
}

.tag-section {
    margin: 0 20px;
}

.tag-header {
    padding: 5px 5px 10px;
    cursor: pointer;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid rgba(59,65,81, 0.3);
}

.tag-header:hover {
    background: rgba(0,0,0,.02);
}

.tag-header h2 {
    font-size: 24px;
    color: #3b4151;
    flex: 1;
}

.tag-count {
    background: lightsteelblue;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}

.tag-arrow {
    font-size: 20px;
    transition: transform 0.3s;
    color: #3b4151;
    font-weight: normal;
}

.tag-arrow.open {
    transform: rotate(90deg);
}

.tools-container {
    display: none;
    margin-bottom: 20px;
}

.tools-container.open {
    display: block;
}

.operation {
    background: rgba(73, 204, 144, 0.1);
    border: 1px solid rgba(59, 65, 81, 0.3);
    border-radius: 4px;
    margin-bottom: 10px;
    overflow: hidden;
}

.operation-header {
    display: flex;
    align-items: center;
    padding: 15px 20px;
    cursor: pointer;
    gap: 15px;
}

.operation-header:hover {
    background: rgba(73, 204, 144, 0.2);
}

.http-method {
    background: #49cc90;
    color: white;
    padding: 6px 15px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: bold;
    min-width: 60px;
    text-align: center;
}

.operation-path {
    font-family: monospace;
    font-size: 14px;
    color: #3b4151;
    flex: 1;
}

.operation-summary {
    color: #3b4151;
    font-size: 14px;
}

.operation-expand {
    font-size: 20px;
    color: #3b4151;
    transition: transform 0.3s;
    font-weight: normal;
}

.operation-expand.open {
    transform: rotate(90deg);
}

.operation-body {
    border-top: 1px solid rgba(59, 65, 81, 0.1);
    padding: 20px;
    background: #fafafa;
    display: none;
}

.operation-body.open {
    display: block;
}

.operation-section {
    margin-bottom: 20px;
}

.operation-section h3 {
    font-size: 16px;
    margin-bottom: 10px;
    color: #3b4151;
}

.description {
    color: #3b4151;
    line-height: 1.6;
    margin-bottom: 15px;
    white-space: pre-wrap;
}

.parameters-table {
    width: 100%;
    border-collapse: collapse;
    background: #fff;
    border-radius: 4px;
    overflow: hidden;
}

.parameters-table th {
    background: #fafafa;
    padding: 12px;
    text-align: left;
    font-weight: 600;
    color: #3b4151;
    border-bottom: 1px solid #d3d3d3;
    font-size: 12px;
    text-transform: uppercase;
}

.parameters-table td {
    padding: 12px;
    border-bottom: 1px solid #ebebeb;
    color: #3b4151;
    font-size: 14px;
}

.parameters-table tr:last-child td {
    border-bottom: none;
}

.param-name {
    font-family: monospace;
    font-weight: 600;
}

.param-required {
    color: #f93e3e;
    font-size: 12px;
    margin-left: 5px;
}

.param-type {
    font-family: monospace;
    font-size: 12px;
    color: #3b4151;
}

.no-params {
    color: #999;
    font-style: italic;
    padding: 20px;
    text-align: center;
    background: #fff;
    border-radius: 4px;
}

.loading {
    text-align: center;
    padding: 40px;
    color: #3b4151;
}

.error {
    background: #f93e3e;
    color: white;
    padding: 20px;
    margin: 20px;
    border-radius: 4px;
}
"""


def _get_javascript(config) -> str:
    """Get JavaScript for the documentation UI"""
    # Use relative URL so it works with the actual server, not the configured base_url
    api_tools_route = config.api_tools_route

    return f"""
let toolsData = {{}};
let allTools = [];

async function loadTools() {{
    try {{
        const response = await fetch('{api_tools_route}');
        const data = await response.json();

        toolsData = data.tools || {{}};
        allTools = Object.values(toolsData);

        renderToolsByTags();
    }} catch (error) {{
        console.error('Error loading tools:', error);
        document.getElementById('tagsContainer').innerHTML =
            '<div class="error">Error loading tools. Please make sure the server is running.</div>';
    }}
}}

function renderToolsByTags() {{
    const container = document.getElementById('tagsContainer');

    // Group tools by tags
    const tagGroups = {{}};

    allTools.forEach(tool => {{
        const tags = tool.tags && tool.tags.length > 0 ? tool.tags : ['Untagged'];

        tags.forEach(tag => {{
            if (!tagGroups[tag]) {{
                tagGroups[tag] = [];
            }}
            tagGroups[tag].push(tool);
        }});
    }});

    // Sort tags alphabetically
    const sortedTags = Object.keys(tagGroups).sort();

    // Build HTML
    let html = '';
    sortedTags.forEach(tag => {{
        const tools = tagGroups[tag];
        html += `
            <div class="tag-section">
                <div class="tag-header" onclick="toggleTag('${{tag}}')">
                    <h2>${{tag}}</h2>
                    <span class="tag-count">${{tools.length}}</span>
                    <span class="tag-arrow open" id="arrow-${{tag}}">›</span>
                </div>
                <div class="tools-container open" id="tools-${{tag}}">
                    ${{tools.map(tool => renderToolOperation(tool)).join('')}}
                </div>
            </div>
        `;
    }});

    container.innerHTML = html;
}}

function renderToolOperation(tool) {{
    const params = tool.parameters || {{}};
    const paramCount = Object.keys(params).length;
    const toolId = tool.name.replace(/[^a-zA-Z0-9]/g, '_');

    let paramsHtml = '';
    if (paramCount === 0) {{
        paramsHtml = '<div class="no-params">No parameters</div>';
    }} else {{
        paramsHtml = `
            <table class="parameters-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    ${{Object.entries(params).map(([paramName, paramInfo]) => `
                        <tr>
                            <td>
                                <span class="param-name">${{paramName}}</span>
                                ${{paramInfo.required ? '<span class="param-required">* required</span>' : ''}}
                                ${{paramInfo.default ? `<br><small style="color: #999;">Default: ${{paramInfo.default}}</small>` : ''}}
                            </td>
                            <td>
                                <span class="param-type">${{paramInfo.type || 'any'}}</span>
                            </td>
                            <td>${{paramInfo.description || '-'}}</td>
                        </tr>
                    `).join('')}}
                </tbody>
            </table>
        `;
    }}

    return `
        <div class="operation">
            <div class="operation-header" onclick="toggleOperation('${{toolId}}')">
                <span class="http-method">TOOL</span>
                <span class="operation-path">${{tool.name}}</span>
                <span class="operation-summary">${{tool.title || tool.name}}</span>
                <span class="operation-expand" id="expand-${{toolId}}">›</span>
            </div>
            <div class="operation-body" id="body-${{toolId}}">
                <div class="operation-section">
                    <h3>Description</h3>
                    <div class="description">${{tool.description || 'No description available'}}</div>
                </div>
                <div class="operation-section">
                    <h3>Parameters</h3>
                    ${{paramsHtml}}
                </div>
            </div>
        </div>
    `;
}}

function toggleTag(tag) {{
    const container = document.getElementById(`tools-${{tag}}`);
    const arrow = document.getElementById(`arrow-${{tag}}`);

    container.classList.toggle('open');
    arrow.classList.toggle('open');
}}

function toggleOperation(toolId) {{
    const body = document.getElementById(`body-${{toolId}}`);
    const expand = document.getElementById(`expand-${{toolId}}`);

    body.classList.toggle('open');
    expand.classList.toggle('open');
}}

// Search functionality
document.getElementById('searchInput').addEventListener('input', (e) => {{
    const searchTerm = e.target.value.toLowerCase();

    if (searchTerm === '') {{
        renderToolsByTags();
        return;
    }}

    const filteredTools = allTools.filter(tool =>
        tool.name.toLowerCase().includes(searchTerm) ||
        (tool.title && tool.title.toLowerCase().includes(searchTerm)) ||
        (tool.description && tool.description.toLowerCase().includes(searchTerm)) ||
        (tool.tags && tool.tags.some(tag => tag.toLowerCase().includes(searchTerm)))
    );

    // Render filtered tools under "Search Results" tag
    const container = document.getElementById('tagsContainer');
    if (filteredTools.length === 0) {{
        container.innerHTML = '<div class="no-params" style="margin: 20px;">No tools found matching your search.</div>';
    }} else {{
        container.innerHTML = `
            <div class="tag-section">
                <div class="tag-header" onclick="toggleTag('search')">
                    <h2>Search Results</h2>
                    <span class="tag-count">${{filteredTools.length}}</span>
                    <span class="tag-arrow open" id="arrow-search">›</span>
                </div>
                <div class="tools-container open" id="tools-search">
                    ${{filteredTools.map(tool => renderToolOperation(tool)).join('')}}
                </div>
            </div>
        `;
    }}
}});

// Load tools on page load
loadTools();
"""
