# Multi-Agent BODMAS Calculation Engine

A production-grade, highly resilient calculation engine using LangChain, LangGraph, and FastMCP with full Langfuse observability.

## Overview
This system evaluates raw string mathematical expressions (e.g., `10 ÷ (3 + 2)`) using a state-reduction loop powered by 5 independent agents (Planner, Adder, Subtractor, Multiplier, Divider). It uses a local Ollama endpoint by default, with graceful fallbacks to OpenAI or Anthropic API providers.

## System Prerequisites
- Python 3.10+
- Docker & Docker Compose (for PostgreSQL & Langfuse)
- Optional: Local Ollama instance running

## Quick Execution Recipe
1. **Clone the repository.**
2. **Setup virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your specific API keys if not using Ollama
   ```
4. **Boot Infrastructure (Langfuse & PostgreSQL):**
   ```bash
   docker-compose up -d
   ```
5. **Run the MCP Server:**
   ```bash
   ./scripts/run_mcp.sh
   ```

## Telemetry Trace Navigation
All executions are traced via Langfuse. 
- Open http://localhost:3000
- Login and view the generated traces to see exactly how the multi-agent graph evaluated your mathematical expressions step-by-step.
