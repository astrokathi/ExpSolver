from src.state import BODMASGraphState

def base_agent_node(state: BODMASGraphState, agent_name: str) -> dict:
    """
    Base utility to log agent history.
    Each specific node will call this to append to history.
    """
    history = state.get("agent_history", [])
    history.append(agent_name)
    return {"agent_history": history}
