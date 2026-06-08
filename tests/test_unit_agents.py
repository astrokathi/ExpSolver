import pytest
from src.agents.adder import adder_node
from src.agents.subtractor import subtractor_node
from src.agents.multiplier import multiplier_node
from src.agents.divider import divider_node
from src.agents.planner import planner_node

def test_adder_agent():
    state = {
        "current_expression": "10 / (3 + 2)",
        "next_target_op": {"op": "add", "args": [3.0, 2.0], "original_match": "3 + 2"},
        "agent_history": []
    }
    result = adder_node(state)
    assert result["step_result"] == "5.0"
    assert result["current_expression"] == "10 / (5.0)"
    assert "adder" in result["agent_history"]

def test_subtractor_agent():
    state = {
        "current_expression": "10 - 2",
        "next_target_op": {"op": "subtract", "args": [10.0, 2.0], "original_match": "10 - 2"},
        "agent_history": []
    }
    result = subtractor_node(state)
    assert result["step_result"] == "8.0"
    assert result["current_expression"] == "8.0"
    assert "subtractor" in result["agent_history"]

def test_multiplier_agent():
    state = {
        "current_expression": "4 * 5",
        "next_target_op": {"op": "multiply", "args": [4.0, 5.0], "original_match": "4 * 5"},
        "agent_history": []
    }
    result = multiplier_node(state)
    assert result["step_result"] == "20.0"
    assert result["current_expression"] == "20.0"

def test_divider_agent():
    state = {
        "current_expression": "10 / 2",
        "next_target_op": {"op": "divide", "args": [10, 2], "original_match": "10 / 2"},
        "agent_history": []
    }
    result = divider_node(state)
    assert result["step_result"] == "5.0"
    assert result["current_expression"] == "5.0"

def test_divider_agent_zero():
    state = {
        "current_expression": "10 / 0",
        "next_target_op": {"op": "divide", "args": [10, 0], "original_match": "10 / 0"},
        "agent_history": []
    }
    result = divider_node(state)
    assert "error_context" in result
    assert result["error_context"]["code"] == "DIV_ZERO"
    
# Not testing planner directly since it requires LLM access, 
# but one could mock the LLM factory for a pure unit test.
