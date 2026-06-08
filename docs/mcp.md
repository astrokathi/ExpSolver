# FastMCP Interface Standard Documentation

The application exposes the calculation engine via the Model Context Protocol (MCP) using the `fastmcp` Python package.

## Server Configuration
- **Server Name**: `BODMAS_Calculation_Engine`
- **Transport**: Standard I/O (stdio)
- **File**: `src/mcp_server.py`

## Exposed Tools

### `calculate_expression`
Evaluates a mathematical string using the multi-agent BODMAS graph.

**Inputs:**
- `expression` (string, required): The mathematical expression to evaluate. Example: `"10 / (3 + 2)"`

**Outputs:**
- Returns a `string`.
- On success: The string representation of the final evaluated float (e.g., `"2.0"`).
- On business error: A formatted string `ERROR: [CODE] message`.
- On system error: `System Error: <exception text>`.

## Usage
Clients can bind to this server by executing the `scripts/run_mcp.sh` shell script.
