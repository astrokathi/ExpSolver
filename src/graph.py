import re
from langgraph.graph import StateGraph, END
from src.state import BODMASGraphState
from src.agents.planner import planner_node
from src.agents.adder import adder_node
from src.agents.subtractor import subtractor_node
from src.agents.multiplier import multiplier_node
from src.agents.divider import divider_node
from src.config import get_langfuse_handler

def router_node(state: BODMASGraphState):
    """
    The main routing logic.
    Decides if the expression is fully reduced or needs processing.
    """
    current_expr = state["current_expression"].strip()
    
    # Check if infinite loop
    if len(state.get("agent_history", [])) > 15:
        return {"error_context": {"code": "INFINITE_LOOP_DETECTED", "msg": "Graph execution exceeded 15 steps."}}
    
    # Check if it's already a single number (float or int, optionally negative)
    if re.match(r"^-?\d+(\.\d+)?$", current_expr):
        return {"final_value": float(current_expr)}
        
    return {"current_expression": current_expr}

def route_from_router(state: BODMASGraphState) -> str:
    """
    Routing edge from router.
    If error -> END
    If final_value -> END
    Else -> planner
    """
    if state.get("error_context") is not None:
        return "END"
    if state.get("final_value") is not None:
        return "END"
    return "planner"

def route_from_planner(state: BODMASGraphState) -> str:
    """
    Routing edge from planner to specific math node.
    """
    target = state.get("next_target_op")
    if not target:
        return "END"
        
    op = target.get("op")
    if op == "add":
        return "adder"
    elif op == "subtract":
        return "subtractor"
    elif op == "multiply":
        return "multiplier"
    elif op == "divide":
        return "divider"
    else:
        # Fallback if the planner creates garbage
        return "END"

def route_from_math(state: BODMASGraphState) -> str:
    """
    After a math operation, we go back to the router,
    UNLESS there was a critical math error (like DIV_ZERO).
    """
    if state.get("error_context") is not None:
        return "END"
    return "router"

def create_bodmas_graph():
    """
    Constructs the supervisor/router LangGraph loop.
    """
    workflow = StateGraph(BODMASGraphState)

    workflow.add_node("router", router_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("adder", adder_node)
    workflow.add_node("subtractor", subtractor_node)
    workflow.add_node("multiplier", multiplier_node)
    workflow.add_node("divider", divider_node)

    # Initial entrypoint
    workflow.set_entry_point("router")

    # Routing from router -> END or planner
    workflow.add_conditional_edges("router", route_from_router, {
        "END": END,
        "planner": "planner"
    })

    # Routing from planner -> math agents
    workflow.add_conditional_edges("planner", route_from_planner, {
        "adder": "adder",
        "subtractor": "subtractor",
        "multiplier": "multiplier",
        "divider": "divider",
        "END": END
    })

    # Routing from math agents -> router
    workflow.add_conditional_edges("adder", route_from_math, {"router": "router", "END": END})
    workflow.add_conditional_edges("subtractor", route_from_math, {"router": "router", "END": END})
    workflow.add_conditional_edges("multiplier", route_from_math, {"router": "router", "END": END})
    workflow.add_conditional_edges("divider", route_from_math, {"router": "router", "END": END})

    app = workflow.compile()
    return app

def run_calculation(expression: str) -> str:
    """
    Helper function to run the compiled graph with tracing.
    """
    app = create_bodmas_graph()
    initial_state = {
        "original_expression": expression,
        "current_expression": expression,
        "agent_history": [],
        "next_target_op": None,
        "step_result": None,
        "error_context": None,
        "final_value": None
    }
    
    callbacks = []
    langfuse_handler = get_langfuse_handler()
    if langfuse_handler:
        callbacks.append(langfuse_handler)
        
    config = {"callbacks": callbacks} if callbacks else {}
    
    final_state = app.invoke(initial_state, config=config)
    
    if final_state.get("error_context"):
        err = final_state["error_context"]
        return f"ERROR: [{err.get('code')}] {err.get('msg')}"
        
    if final_state.get("final_value") is not None:
        return str(final_state["final_value"])
        
    return "ERROR: Computation failed to reach a final value."
