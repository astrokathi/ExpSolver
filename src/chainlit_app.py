import chainlit as cl
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome to the BODMAS Calculation Engine! I am connected to the MCP Server. Please enter a mathematical expression (e.g., '15 + 3').").send()

@cl.on_message
async def on_message(message: cl.Message):
    # Send a thinking message
    msg = cl.Message(content="Calculating via MCP Server...")
    await msg.send()
    
    try:
        import sys
        import os
        
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        
        # Define the MCP Server parameters
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["src/mcp_server.py"],
            env=env
        )
        
        # Connect to the MCP Server via stdio
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the MCP session
                await session.initialize()
                
                # Execute the calculation tool
                response = await session.call_tool("calculate_expression", {"expression": message.content})
                
                # Extract the result from the MCP response
                if response.content and len(response.content) > 0:
                    result = response.content[0].text
                    msg.content = f"Result: {result}"
                else:
                    msg.content = "No result returned from MCP Server."
                
                await msg.update()
                
    except Exception as e:
        msg.content = f"An MCP error occurred: {str(e)}"
        await msg.update()
