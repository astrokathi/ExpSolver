from src.state import BODMASGraphState
from src.agents.base import base_agent_node

def subtractor_node(state: BODMASGraphState):
    base_update = base_agent_node(state, "subtractor")
    target = state["next_target_op"]
    
    a, b = target["args"]
    res = a - b
    
    orig_expr = state["current_expression"]
    match_str = target["original_match"]
    new_expr = orig_expr.replace(match_str, str(res), 1)
    
    return {
        "agent_history": base_update["agent_history"],
        "step_result": str(res),
        "current_expression": new_expr
    }
