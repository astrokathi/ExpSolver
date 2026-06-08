# State Management Schema

The graph's central state is managed via a TypedDict `BODMASGraphState`. It tracks the entire reduction process from start to finish.

## Schema Definition
```python
class BODMASGraphState(TypedDict):
    original_expression: str
    current_expression: str
    next_target_op: Optional[Dict[str, Any]]
    step_result: Optional[str]
    agent_history: List[str]
    error_context: Optional[Dict[str, Any]]
    final_value: Optional[float]
```

## Flow Transitions
1. **Init**: User submits `10+2`. `original_expression` and `current_expression` become `"10+2"`.
2. **Planner**: Identifies addition. Sets `next_target_op` to `{"op": "add", "args": [10, 2], "original_match": "10+2"}`. Appends `"planner"` to `agent_history`.
3. **Adder**: Executes math. Sets `step_result` to `"12.0"`. Updates `current_expression` to `"12.0"`. Appends `"adder"` to `agent_history`.
4. **Router**: Sees `current_expression` is a float. Sets `final_value` to `12.0`. Ends execution.

At any point, if an error occurs, `error_context` is populated, triggering an immediate routing to the `END` node.
