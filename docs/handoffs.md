# Data Handoffs Protocol

This document explains the data shapes passing between the system domains.

## 1. FastMCP to Graph Router
When the user executes the `calculate_expression` tool, FastMCP accepts a raw string.
It maps this string into the initial `BODMASGraphState`:
```python
{
    "original_expression": "10 + 2 * 3",
    "current_expression": "10 + 2 * 3",
    "agent_history": [],
    "next_target_op": None,
    "step_result": None,
    "error_context": None,
    "final_value": None
}
```

## 2. Planner to Math Agents
The Planner generates structured output enforcing the Pydantic `OperationToken` model.
This is injected into the state under `next_target_op`:
```python
{
    "op": "multiply",
    "args": [2.0, 3.0],
    "original_match": "2 * 3"
}
```

## 3. Math Agents to Router
The executed math agent takes the `next_target_op`, performs the calculation, and performs a string replacement on `current_expression`.
The new state moving back to the router looks like:
```python
{
    "step_result": "6.0",
    "current_expression": "10 + 6.0",
    "agent_history": ["planner", "multiplier"]
}
```
The router then loops this back to the Planner until `current_expression` is a solitary float.
