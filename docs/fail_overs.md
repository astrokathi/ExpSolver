# Fail-over and Governance Strategy

This system is built with robust safety nets to handle both deterministic code failures and LLM provider outages.

## 1. LLM Provider Fallback Factory
Located in `src/config.py`, the `get_llm()` factory method provides layered redundancy:
- **Tier 1 (Local Ollama)**: The system attempts an HTTP ping to `$OLLAMA_BASE_URL`. If a 200 OK is received, it instantiates `ChatOllama`. This ensures zero-cost, localized, secure processing by default.
- **Tier 2 (OpenAI)**: If Ollama times out or refuses connection, the factory falls back to `OPENAI_API_KEY`.
- **Tier 3 (Anthropic)**: If OpenAI keys are missing or invalid, it falls back to `ANTHROPIC_API_KEY`.
- **Catastrophic Failure**: If all tiers fail, it raises an exception which is caught and surfaced via FastMCP.

## 2. Infinite Loop Trapping
LLMs can sometimes fail to parse an expression, repeating the exact same output tokens in a loop.
- The `router_node` checks `len(state.get("agent_history", []))`.
- If the count exceeds 15, the router sets `error_context = {"code": "INFINITE_LOOP_DETECTED"}`.
- This forces the routing edge `route_from_router` to instantly map to `END`.

## 3. Mathematical Safety Nets
- The `divider_node` actively traps division by zero. Before execution, it inspects `args[1]`.
- If the denominator is `0` or `0.0`, it sets `error_context = {"code": "DIV_ZERO"}` instead of throwing a raw Python `ZeroDivisionError`.
- This ensures the state graph exits cleanly and passes a formatted business error back to the user interface.
