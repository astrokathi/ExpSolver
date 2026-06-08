# Execution Mock Lifecycle Log

The following represents a mock chronological trace action sequence.

**User Request**: `calculate_expression("10 - (2 * 3)")`

1. **FastMCP Invocation**: Server receives string. Initializes LangGraph.
2. **Router Node**: Sees `"10 - (2 * 3)"`. Not a simple number. Routes to `planner`.
3. **Planner Node**: 
   - LLM analyzes expression.
   - Determines BODMAS bracket precedence: `2 * 3`.
   - Generates output: `{"op": "multiply", "args": [2, 3], "original_match": "2 * 3"}`.
4. **Multiplier Node**:
   - Executes `2 * 3 = 6.0`.
   - Replaces string. State `current_expression` is now `"10 - (6.0)"`.
5. **Router Node**: Sees `"10 - (6.0)"`. Not a simple number. Routes to `planner`.
6. **Planner Node**:
   - Strips brackets to `"10 - 6.0"`.
   - Determines next operation.
   - Generates output: `{"op": "subtract", "args": [10, 6.0], "original_match": "10 - 6.0"}`.
7. **Subtractor Node**:
   - Executes `10 - 6.0 = 4.0`.
   - Replaces string. State `current_expression` is now `"4.0"`.
8. **Router Node**: Sees `"4.0"`. This is a solitary float.
   - Sets `final_value = 4.0`.
   - Routes to `END`.
9. **FastMCP Return**: Server responds with `"4.0"`.
