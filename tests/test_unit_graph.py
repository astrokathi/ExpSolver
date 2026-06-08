import pytest
from src.graph import router_node, route_from_router, route_from_planner, route_from_math

def test_router_node_infinite_loop():
    state = {
        "current_expression": "1 + 1",
        "agent_history": ["dummy"] * 16
    }
    result = router_node(state)
    assert "error_context" in result
    assert result["error_context"]["code"] == "INFINITE_LOOP_DETECTED"

def test_router_node_final_value():
    state = {"current_expression": "42.0"}
    result = router_node(state)
    assert "final_value" in result
    assert result["final_value"] == 42.0
    
    state_neg = {"current_expression": "-3.14"}
    result = router_node(state_neg)
    assert result["final_value"] == -3.14

def test_router_node_continue():
    state = {"current_expression": "10 + 2"}
    result = router_node(state)
    assert "current_expression" in result
    assert result["current_expression"] == "10 + 2"
    assert "final_value" not in result

def test_route_from_router():
    assert route_from_router({"error_context": {}}) == "END"
    assert route_from_router({"final_value": 42}) == "END"
    assert route_from_router({"current_expression": "1+1"}) == "planner"

def test_route_from_planner():
    assert route_from_planner({"next_target_op": {"op": "add"}}) == "adder"
    assert route_from_planner({"next_target_op": {"op": "subtract"}}) == "subtractor"
    assert route_from_planner({"next_target_op": {"op": "multiply"}}) == "multiplier"
    assert route_from_planner({"next_target_op": {"op": "divide"}}) == "divider"
    assert route_from_planner({"next_target_op": None}) == "END"
    assert route_from_planner({"next_target_op": {"op": "garbage"}}) == "END"

def test_route_from_math():
    assert route_from_math({"error_context": {}}) == "END"
    assert route_from_math({"step_result": "5"}) == "router"
