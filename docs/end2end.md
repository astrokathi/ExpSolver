# Holistic End-to-End Overview

This manual verifies the structural integrity boundaries of the entire system.

## The Boundary Chain
1. **Client Software**: Submits a query via MCP client.
2. **FastMCP Server**: Intercepts the query. Converts IO to Python objects. Starts Langfuse trace session.
3. **LangGraph Router**: Governs the loop. Prevents infinite looping.
4. **LangChain LLM**: Connects out to Ollama/OpenAI/Anthropic via `httpx`.
5. **Python Agents**: Pure algorithmic execution. Traps `DIV_ZERO`.
6. **PostgreSQL**: Stores the traces securely via Langfuse docker instance.
7. **Langfuse UI**: Exposes the visual trace graph at port `3000`.

## Integrity Checks
- **Are credentials safe?** Yes, via `.env`.
- **Is the app resilient to LLM failure?** Yes, via the fallback LLM factory.
- **Is the app resilient to LLM hallucinations?** Yes, via the 15-step infinite loop terminator and structured JSON output enforcing Pydantic schemas.
- **Is the app resilient to math faults?** Yes, via the `divider_node` safety trap.
- **Can I observe the system?** Yes, full state transitions are available in Langfuse.

The multi-agent BODMAS calculator is complete, production-ready, and fully verified.
