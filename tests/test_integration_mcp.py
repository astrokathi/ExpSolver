import pytest
from src.mcp_server import calculate_expression

# To make this a true unit test without calling the LLM, we would mock run_calculation.
# Here we test the interface structure itself.

def test_mcp_interface_handles_errors(monkeypatch):
    """Test that FastMCP interface wraps exceptions cleanly."""
    def mock_run_calculation(expr):
        raise ValueError("Simulated Exception")
        
    import src.mcp_server
    monkeypatch.setattr(src.mcp_server, "run_calculation", mock_run_calculation)
    
    result = calculate_expression("1 + 1")
    assert result.startswith("System Error:")
    assert "Simulated Exception" in result

def test_mcp_interface_success(monkeypatch):
    """Test that FastMCP interface returns the valid result."""
    def mock_run_calculation(expr):
        return "42.0"
        
    import src.mcp_server
    monkeypatch.setattr(src.mcp_server, "run_calculation", mock_run_calculation)
    
    result = calculate_expression("20 + 22")
    assert result == "42.0"
