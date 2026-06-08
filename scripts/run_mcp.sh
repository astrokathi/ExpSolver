#!/usr/bin/env bash
set -e

echo "[MCP RUNNER] Checking environment setup..."

if [ ! -f .env ]; then
  echo "[MCP RUNNER] WARNING: .env file not found. Falling back to .env.example structure."
fi

# Check if Docker is running and Langfuse is accessible
if curl -s http://localhost:3000 > /dev/null; then
  echo "[MCP RUNNER] Langfuse appears to be running on port 3000."
else
  echo "[MCP RUNNER] WARNING: Langfuse might not be running. Run 'docker-compose up -d' if you want tracing."
fi

# Determine if Ollama is running
OLLAMA_URL=${OLLAMA_BASE_URL:-"http://localhost:11434"}
if curl -s "$OLLAMA_URL" > /dev/null; then
  echo "[MCP RUNNER] Local Ollama instance detected at $OLLAMA_URL."
else
  echo "[MCP RUNNER] Local Ollama NOT detected. The system will fall back to OpenAI/Anthropic if keys are provided."
fi

echo "[MCP RUNNER] Starting FastMCP server..."
# Using FastMCP dev mode or standard module execution
python -m src.mcp_server
