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
adk web ```

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

## 📂 Project Structure

```
agentdir/
├── pyproject.toml      # Project dependencies managed by uv
├── sample_agent/
│   ├── __init__.py     # Exports the agent to the ADK
│   └── agent.py        # Contains agent definitions and instructions
├── employee_email_agent/
│   ├── __init__.py     # Exports the employee email agent
│   └── agent.py        # Generates employee-facing emails using OpenAI
└── ...
```