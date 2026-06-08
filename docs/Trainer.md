---
layout: default
title: Trainer Guide (Build Your Own)
---

# 🏗️ Trainer Guide: Build Your Own Agentic Architecture

This guide is designed for developers who want to use the **ExpSolver** architecture as a base layer to build their own multi-agent AI systems from scratch. 

By following this tutorial in order, you will learn how to replicate our architecture—combining **LangGraph**, **Model Context Protocol (MCP)**, **Chainlit**, and **Langfuse Observability**—but with your own custom Agents and Planner tailored to your specific scenarios.

---

## 1. Prerequisites & Project Setup

First, initialize your project structure and install the necessary dependencies.

### Folder Structure
Create a new directory and mirror this clean base layer:
```bash
mkdir my-agentic-app && cd my-agentic-app
mkdir -p src/agents tests
touch src/__init__.py src/state.py src/graph.py src/mcp_server.py src/chainlit_app.py .env
```

### Virtual Environment & Dependencies
Set up your Python environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install langgraph langchain langchain-openai langchain-community mcp chainlit langfuse
```

---

## 2. Defining the State Base Layer (`src/state.py`)

In LangGraph, all agents communicate by reading from and writing to a shared **State**. You need to define this state structure first.

```python
# src/state.py
from typing import TypedDict, Annotated, List, Optional
import operator

# The reducer function `operator.add` ensures that lists are appended to, not overwritten.
class AgentState(TypedDict):
    input_task: str
    current_status: str
    agent_history: Annotated[List[str], operator.add]
    next_action: Optional[str]
    final_result: Optional[str]
```

---

## 3. Building the Planner Agent (`src/agents/planner.py`)

The **Planner** acts as the orchestrator. It looks at the current `input_task` and the `agent_history` to determine which worker agent should act next.

```python
# src/agents/planner.py
from src.state import AgentState

def planner_node(state: AgentState):
    task = state["input_task"]
    history = state["agent_history"]
    
    # Custom Logic: Decide what to do next based on your scenario.
    # For example, if no history exists, send to 'researcher'.
    if not history:
        return {"next_action": "research", "agent_history": ["Planner routed to Researcher"]}
    
    # If research is done, send to 'writer'.
    if "research_done" in state.get("current_status", ""):
        return {"next_action": "write", "agent_history": ["Planner routed to Writer"]}
    
    # If everything is done, finish the graph.
    return {"next_action": "finish", "final_result": "Task completed successfully."}
```

---

## 4. Creating Custom Worker Agents (`src/agents/workers.py`)

Worker agents execute specific domain tasks. You can create as many as your scenario requires.

```python
# src/agents/workers.py
from src.state import AgentState

def researcher_node(state: AgentState):
    # LLM or API call goes here
    result = f"Researched context for: {state['input_task']}"
    
    return {
        "current_status": "research_done",
        "agent_history": [f"Researcher found data."]
    }

def writer_node(state: AgentState):
    # LLM or API call goes here
    draft = "This is the final drafted document."
    
    return {
        "current_status": "writing_done",
        "agent_history": [f"Writer finished drafting."]
    }
```

---

## 5. Orchestrating the Graph (`src/graph.py`)

Now, connect your Planner and Workers using **LangGraph**. This creates the cyclical flow of your multi-agent system.

```python
# src/graph.py
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.planner import planner_node
from src.agents.workers import researcher_node, writer_node

# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

# 3. Define the Router Function
def route_next_step(state: AgentState):
    action = state.get("next_action")
    if action == "research":
        return "researcher"
    elif action == "write":
        return "writer"
    else:
        return END

# 4. Connect Edges
workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", route_next_step)
workflow.add_edge("researcher", "planner") # Route back to planner after work
workflow.add_edge("writer", "planner")     # Route back to planner after work

# 5. Compile
app_graph = workflow.compile()

# Helper function to trigger execution
def run_custom_graph(task: str):
    initial_state = {"input_task": task, "agent_history": []}
    result = app_graph.invoke(initial_state)
    return result.get("final_result", "No result")
```

---

## 6. Exposing via MCP Server (`src/mcp_server.py`)

To make your graph accessible to modern frontends and IDEs, wrap it in a **Model Context Protocol (MCP)** server.

```python
# src/mcp_server.py
from mcp.server.fastmcp import FastMCP
from src.graph import run_custom_graph

# Initialize MCP Server
mcp = FastMCP("CustomAgentServer")

# Expose Graph as an MCP Tool
@mcp.tool()
def execute_agent_task(task_description: str) -> str:
    """Run the multi-agent orchestration for a given task."""
    try:
        return run_custom_graph(task_description)
    except Exception as e:
        return f"Error executing task: {str(e)}"

if __name__ == "__main__":
    # Start the server over Standard Input/Output
    mcp.run_stdio()
```

---

## 7. Building the Chainlit Frontend (`src/chainlit_app.py`)

Finally, create a UI that connects to your MCP server.

```python
# src/chainlit_app.py
import chainlit as cl
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@cl.on_chat_start
async def start_chat():
    # Setup MCP connection to your local server
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp_server.py"]
    )
    
    # Store the connection in the Chainlit user session
    cl.user_session.set("mcp_params", server_params)
    await cl.Message("✅ Custom Agentic MCP Server Connected. What task should I execute?").send()

@cl.on_message
async def main(message: cl.Message):
    server_params = cl.user_session.get("mcp_params")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call the tool exposed by your MCP server
            result = await session.call_tool(
                "execute_agent_task", 
                arguments={"task_description": message.content}
            )
            
            # Send the result back to the user
            await cl.Message(content=result.content[0].text).send()
```

---

## 8. Running Your System

With the code in place, you can bring your architecture online.

**1. Set up Observability (Optional but recommended):**
Ensure your Langfuse credentials are in `.env`, and start your local logging databases:
```bash
docker compose up -d
```

**2. Start the Chainlit Application:**
Run the Chainlit frontend with hot-reloading enabled. Chainlit will automatically start the underlying MCP server process.
```bash
PYTHONPATH=. chainlit run src/chainlit_app.py -w
```

**3. Interact!**
Open `http://localhost:8000` in your browser and type your task. Watch your Planner and Agents work together seamlessly over MCP!
