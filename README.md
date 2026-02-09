# ADK Sample Agent Project

This repository contains a reference implementation for a local LLM agent built using the Google ADK (Agent Development Kit) and LiteLLM. It is configured to run efficiently using uv for dependency management and Ollama or OpenAI models depending on the agent.

## 🚀 Quick Start

### Prerequisites
* uv installed on your system.
* Ollama running locally with the `gemma3` model pulled (for agents that use Ollama).
* OpenAI API key configured in your environment (for agents that use OpenAI models, e.g. `employee_email_agent`).

## ADK Agent Setup Guide

This guide outlines the steps to initialize a project, install dependencies, and configure a basic LLM agent using the Google ADK and LiteLLM.

### 1. Project Initialization

Run the following commands in your terminal to create the project directory and set up the environment using uv.

```bash
mkdir agentdir
cd agentdir
uv init
uv add google-adk
uv add litellm  
adk create sample_agent
```

### 2. Configure the Agent (agent.py)

Locate the agent.py file within your project and use the following code to define your agent. This example utilizes the gemma3 model via Ollama for the sample agent.

```python
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm('ollama/gemma3'),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

### 3. Register the Agent (__init__.py)

To ensure the agent is recognized by the ADK, add the agent's name to the __init__.py file:

```text
__all__ = ["root_agent"]
```

### 4. Running the Agent

You can execute your agent using either the command line or a web-based interface.

#### Via Terminal

```bash
adk run sample_agent/
```

#### Via Web Interface

```bash
adk web
```

## Employee Email Agent

A new agent, `employee_email_agent`, has been added to this repository. It drafts employee-facing emails (announcements, reminders, onboarding messages) using ADK + LiteLLM with an OpenAI model.

### Purpose

- Generate professional, concise internal emails from a short prompt (purpose, audience, tone, required points).

### Location

- The agent lives in `employee_email_agent/` and includes `agent.py` and `__init__.py`.

### Quick Run

From the repository root run:

```bash
adk run employee_email_agent/
```

### Implementation note

The `employee_email_agent` is configured to use an OpenAI model via LiteLLM. Make sure your OpenAI credentials are set in the environment before running this agent.

### Example agent snippet (matches `employee_email_agent/agent.py`):

```python
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

email_agent = Agent(
    model=LiteLlm('openai/gpt-5'),
    name='employee_email_agent',
    description='Queries SQLite DB for employees by department + geography + role and sends emails.',
    instruction='Generate a professional internal email tailored to the provided purpose, audience, and tone.',
)
```

### Notes

- Review generated drafts before sending. The agent assists with writing but does not replace human review.
- If you need to customize templates or add more examples, edit `employee_email_agent/agent.py` and add tests or sample prompts.

## 🔌 MCP Server Setup for Claude Desktop

The `employee_email_agent` can be exposed as a Model Context Protocol (MCP) server, allowing Claude Desktop to directly query the employee database and send emails through natural language commands.

### Step 1: Create the MCP Server

Create a file named `mcp_server.py` in the `employee_email_agent/` directory:

```python
import uvicorn
from fastmcp import FastMCP
from typing import List, Dict, Any, Optional

from agent import get_employees as get_employees_from_db
from agent import send_email as send_email_to_employee

app = FastMCP(
    name="Employee Email Agent MCP Server",
    instructions="""
    Use get_employees_tool to find employees by department (e.g. Sales, Engineering), 
    geo_location (e.g. US, New York, EU), and/or role.
    Any parameter can be left out (pass None or omit) to get broader results.
    
    Only call send_email_tool when the user explicitly asks to send an email or clearly confirms.
    
    Always present the list of found employees (names and emails) in a clear, readable way 
    before suggesting to send email.
    Be professional, polite, and confirm before sending any message.
    """)

@app.tool
def get_employees_tool(
    department: Optional[str] = None,
    geo_location: Optional[str] = None,
    role: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetches employees from the database based on optional filters.
    Args:
        department (str, optional): The department to filter employees by.
        geo_location (str, optional): The geographical location to filter employees by.
        role (str, optional): The role to filter employees by.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing employee names and emails.
    """
    return get_employees_from_db(department, geo_location, role)

@app.tool
def send_email_tool(
    name: str,
    email: str,
    subject: str,
    body: str
) -> str:
    """
    Simulates sending an email to an employee.
    Args:
        name (str): The name of the email recipient.
        email (str): Email address to send to.
        subject (str): The subject of the email.
        body (str): The body content of the email.
    Returns:
        str: A confirmation message indicating the email was sent.
    """
    return send_email_to_employee(name, email, subject, body)

if __name__ == "__main__":
    app.run(transport="stdio")
```

### Step 2: Add FastMCP Dependency

Make sure `fastmcp` is added to your project dependencies. Add it to your `pyproject.toml` or install it using:

```bash
uv add fastmcp
```

### Step 3: Configure Claude Desktop

**For Windows:**

1. Locate the Claude Desktop configuration file:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   (Typically: `C:\Users\YourUsername\AppData\Roaming\Claude\claude_desktop_config.json`)

2. Edit the file to add the MCP server configuration:

```json
{
  "preferences": {
    "sidebarMode": "chat"
  },
  "mcpServers": {
    "employee-email-agent": {
      "command": "C:\\Path\\To\\Your\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Path\\To\\Your\\employee_email_agent\\mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**For macOS/Linux:**

1. Locate the Claude Desktop configuration file:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json  # macOS
   ~/.config/Claude/claude_desktop_config.json                      # Linux
   ```

2. Edit the file to add the MCP server configuration:

```json
{
  "preferences": {
    "sidebarMode": "chat"
  },
  "mcpServers": {
    "employee-email-agent": {
      "command": "/path/to/your/.venv/bin/python",
      "args": [
        "/path/to/your/employee_email_agent/mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**Important Notes:**
- Replace `C:\\Path\\To\\Your\\` with the actual path to your project
- Use double backslashes (`\\`) in Windows paths within JSON
- Use the full path to your virtual environment's Python executable
- Ensure all paths are absolute, not relative

### Step 4: Restart Claude Desktop

Completely quit and restart Claude Desktop for the changes to take effect. The MCP server should now be connected and available.

### Step 5: Verify Connection

After restarting Claude Desktop:
1. Look for the 🔨 (hammer/tools) icon in the chat interface
2. Click it to see available tools
3. You should see `get_employees_tool` and `send_email_tool` listed

### Testing the MCP Server

You can test your MCP server manually before integrating with Claude Desktop:

```bash
cd employee_email_agent
python mcp_server.py
```

The server should start and wait for input (this is normal for stdio transport).

### Demo: Using the MCP Server in Claude Desktop

Once configured, you can interact with the employee database directly through Claude Desktop using natural language:

**Example Query:**
```
List all the employees from Engineering Department, in geo location of New York and Role as Software Engineer.
```

**Claude's Response:**

Claude will automatically use the `get_employees_tool` to query your database and display the results. You'll see:

1. Claude recognizes the query and requests permission to use the MCP tool
2. A tool usage dialog appears showing the parameters being sent
3. Claude presents the results in a clear, readable format

![MCP Demo Screenshot](./GetEmployees.png)

**Additional Example Queries:**
- "Show me all Sales employees in the US"
- "Find all Marketing Managers"
- "List employees in the HR department"
- "Send an email to all Engineering employees in EU about the team meeting"

The MCP integration allows Claude to seamlessly interact with your local employee database without requiring you to manually format queries or use specific commands.

### Troubleshooting

If the MCP server doesn't connect:

1. **Check Logs:** View Claude Desktop logs at:
   - Windows: `%APPDATA%\Claude\logs\`
   - macOS: `~/Library/Logs/Claude/`
   - Linux: `~/.config/Claude/logs/`

2. **Verify Python Path:** Ensure the Python executable path is correct and accessible

3. **Test Manually:** Run the MCP server directly to check for errors:
   ```bash
   python employee_email_agent/mcp_server.py
   ```

4. **Check Dependencies:** Ensure all required packages are installed:
   ```bash
   uv sync
   ```

5. **Review Documentation:** Visit [MCP Debugging Documentation](https://modelcontextprotocol.io/docs/tools/debugging) for more help

## 📂 Project Structure

```
agentdir/
├── pyproject.toml      # Project dependencies managed by uv
├── sample_agent/
│   ├── __init__.py     # Exports the agent to the ADK
│   └── agent.py        # Contains agent definitions and instructions
├── employee_email_agent/
│   ├── __init__.py     # Exports the employee email agent
│   ├── agent.py        # Generates employee-facing emails using OpenAI
│   ├── mcp_server.py   # MCP server for Claude Desktop integration
│   ├── GetEmployees.png # Demo screenshot
│   └── employees.db    # SQLite database (auto-generated)
└── ...
```