# Developer Documentation & Code Layout

## Modifying LLM Prompts
If you need to change how the system parses BODMAS rules, modify the `ChatPromptTemplate` inside `src/agents/planner.py`.
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a mathematical expression parser..."),
    ("user", "Expression: {expression}")
])
```

## Adding New Operations (e.g. Exponents)
1. Add a new agent file `src/agents/exponent.py`.
2. Update `OperationToken` inside `src/agents/planner.py` to allow `"exponent"` in the `op` field description.
3. Import the new node into `src/graph.py`.
4. Add the node to the `workflow`: `workflow.add_node("exponent", exponent_node)`.
5. Add the routing logic in `route_from_planner`: `elif op == "exponent": return "exponent"`.
6. Add the return edge: `workflow.add_conditional_edges("exponent", route_from_math, ...)`.

## Running the Test Suite
The system uses pytest. Telemetry is explicitly disabled during testing to avoid polluting your Langfuse dashboard with test runs.
```bash
./scripts/test_all.sh
```
