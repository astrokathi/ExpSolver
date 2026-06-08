# Architectural Agents Profile

The system employs 5 independent agents within the graph.

## 1. The Planner Agent
- **Type**: LLM-Backed (Ollama / OpenAI / Anthropic)
- **Responsibility**: Semantic parsing of strings based on BODMAS rules.
- **Output JSON Schema**:
  ```json
  {
    "op": "add|subtract|multiply|divide",
    "args": [float, float],
    "original_match": "string"
  }
  ```
- **System Prompt**: Enforces strict extraction of the *single* most immediate next mathematical step to take.

## 2. The Adder Agent
- **Type**: Deterministic Python execution.
- **Behavior**: Reads `args`, sums them, and performs a string replacement on `original_match` inside `current_expression` with the evaluated float.

## 3. The Subtractor Agent
- **Type**: Deterministic Python execution.
- **Behavior**: Reads `args[0]` and `args[1]`, subtracts them, replaces the string match.

## 4. The Multiplier Agent
- **Type**: Deterministic Python execution.
- **Behavior**: Multiplies the two arguments, replaces the string match.

## 5. The Divider Agent
- **Type**: Deterministic Python execution with Safety Trap.
- **Behavior**: Checks `args[1]`. If it is exactly `0.0`, it traps the execution, logs `{"code": "DIV_ZERO", "msg": "Cannot divide by zero"}` to `error_context`, and forces an early termination of the graph. If non-zero, it performs standard division and string replacement.
