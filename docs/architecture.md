# System Architecture

This document breaks down the Multi-Agent BODMAS Calculation Engine across its three primary operational domains: Ingress, Orchestration, and Execution.

## 1. Ingress Domain (FastMCP)
The application exposes a single tool, `calculate_expression(expression: str)`, via FastMCP.
- **Protocol**: FastMCP runs over stdio by default for CLI interoperability.
- **Responsibility**: It acts as the bridge for external Large Language Models to offload mathematical processing. FastMCP initializes the internal graph execution and returns the resolved string or error context back to the client.

## 2. Orchestration Domain (LangGraph Router)
At the heart of the system is the `BODMASGraphState` running in a LangGraph `StateGraph`.
- **Router Node**: Acts as the supervisor. It analyzes the `current_expression`. If the string consists purely of a number, it terminates the graph and yields the `final_value`. Otherwise, it routes the state to the Planner.
- **Infinite Loop Protection**: The Router monitors `agent_history`. If it exceeds 15 steps without resolving, it throws an `INFINITE_LOOP_DETECTED` error.

## 3. Execution Domain (Planner & Math Agents)
This layer contains 5 distinct sub-agents:
- **Planner (LLM-backed)**: Reads the string, parses BODMAS rules, and generates a structured JSON output (the `next_target_op`) indicating exactly which sub-expression to evaluate next.
- **Adder, Subtractor, Multiplier, Divider (Pure Python)**: These 4 agents are mathematically deterministic. They do not use LLMs. They execute the mathematical operation defined in `next_target_op` and string-replace the result back into the `current_expression`.

## 4. Telemetry Domain (Langfuse)
Throughout the Execution and Orchestration domains, the Langfuse `CallbackHandler` traces every state transition, LLM generation, and graph edge routing, sending data asynchronously to the locally hosted Langfuse PostgreSQL instance.
