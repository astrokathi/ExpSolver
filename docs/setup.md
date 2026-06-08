# Environment Setup Walkthrough

This document explains how to bootstrap the BODMAS calculation engine from scratch.

## 1. Environment Variables (`.env`)
Copy the provided `.env.example` to `.env`:
```bash
cp .env.example .env
```

The system relies on LLMs. The fallback chain is:
1. `OLLAMA_BASE_URL`: The system attempts to ping this first. Default is `http://localhost:11434`.
2. `OPENAI_API_KEY`: If Ollama is down, it uses GPT-4o.
3. `ANTHROPIC_API_KEY`: If OpenAI is missing, it uses Claude 3.5 Sonnet.

If you wish to use Langfuse tracking, ensure these are populated:
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_HOST=http://localhost:3000`

## 2. Docker & Database Migrations
The system requires PostgreSQL to run Langfuse. Ollama is explicitly excluded from Docker and must be run on the host machine.
```bash
docker-compose up -d
```
Docker Compose will automatically spin up PostgreSQL, wait for it to be healthy, and start Langfuse. Langfuse will automatically run its schema migrations on boot.

## 3. Telemetry Endpoint Binding
Once Langfuse boots:
1. Navigate to `http://localhost:3000`.
2. Create an account and a new project.
3. Generate new API keys in the project settings.
4. Paste the `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` into your `.env` file.

The `src/config.py` uses `get_langfuse_handler()` to automatically bind these keys into a `CallbackHandler` which is injected into the LangGraph compile and invoke sequences.
