# LangGraph Structural Specification

This graph utilizes a centralized Hub-and-Spoke (Supervisor) routing topology.

## Nodes
1. `router`: The central supervisor.
2. `planner`: The LLM logic hub.
3. `adder`: Worker node.
4. `subtractor`: Worker node.
5. `multiplier`: Worker node.
6. `divider`: Worker node.

## Routing Edges

**From Router:**
- If `error_context` exists -> `END`
- If `current_expression` is a standalone number -> Set `final_value`, route to `END`
- Else -> `planner`

**From Planner:**
- Reads `next_target_op["op"]`.
- Routes to `adder`, `subtractor`, `multiplier`, or `divider` based on the value.
- If missing or malformed -> `END`.

**From Math Agents:**
- Execute calculation.
- If `error_context` is raised (e.g. `DIV_ZERO`) -> `END`
- Else -> Route back to `router` for the next cycle.
