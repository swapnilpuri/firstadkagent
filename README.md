# ADK Sample Agent Project

This repository contains a reference implementation for a local LLM agent built using the Google ADK (Agent Development Kit) and LiteLLM. It is configured to run efficiently using uv for dependency management and Ollama for local model hosting.

## 🚀 Quick Start

### Prerequisites
* uv installed on your system.
* Ollama running locally with the `gemma3` model pulled.

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

Locate the agent.py file within your project and use the following code to define your agent. This example utilizes the gemma3 model via Ollama.

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

```python
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

## 📂 Project Structure

```
agentdir/
├── pyproject.toml      # Project dependencies managed by uv
├── sample_agent/
│   ├── __init__.py     # Exports the agent to the ADK
│   └── agent.py        # Contains agent definitions and instructions
└── ...
```