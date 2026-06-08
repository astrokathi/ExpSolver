from typing import TypedDict, Optional, Dict, Any, List

class BODMASGraphState(TypedDict):
    """
    Central state definition for the graph.
    Fields:
    - original_expression: The initial math expression string.
    - current_expression: The continually reduced string.
    - next_target_op: A structured dictionary payload from the planner (e.g. {"op": "add", "args": [1, 2]}).
    - step_result: The result of the math operation.
    - agent_history: Tracking loop steps to prevent infinite execution.
    - error_context: Details about business errors like DIV_ZERO.
    - final_value: The completed float evaluation result.
    """
    original_expression: str
    current_expression: str
    next_target_op: Optional[Dict[str, Any]]
    step_result: Optional[str]
    agent_history: List[str]
    error_context: Optional[Dict[str, Any]]
    final_value: Optional[float]
