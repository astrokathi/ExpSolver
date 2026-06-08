import json
import re
from src.state import BODMASGraphState
from src.agents.base import base_agent_node
from src.config import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class OperationToken(BaseModel):
    is_valid: bool = Field(description="True if the expression is valid and complete. False if it is incomplete (e.g., '10 +', unbalanced parens).")
    error_message: str | None = Field(default=None, description="If is_valid is False, provide the error reason.")
    op: str | None = Field(default=None, description="The mathematical operation to perform: 'add', 'subtract', 'multiply', or 'divide'")
    args: list[float] | None = Field(default=None, description="The two numerical arguments for the operation")
    original_match: str | None = Field(default=None, description="The exact substring matched from the expression, e.g. '3 + 2'")

def planner_node(state: BODMASGraphState):
    """
    Analyzes the current expression and determines the next atomic operation
    based on BODMAS precedence.
    """
    base_update = base_agent_node(state, "planner")
    current_expr = state["current_expression"].strip()
    current_expr = current_expr.replace("÷", "/").replace("×", "*")

    # Strip redundant parentheses around single numbers
    prev_expr = ""
    while prev_expr != current_expr:
        prev_expr = current_expr
        current_expr = re.sub(r'\(\s*(-?\d+\.?\d*)\s*\)', r'\1', current_expr)

    # If it's just parentheses wrapping the whole expression, strip them
    while current_expr.startswith("(") and current_expr.endswith(")") and current_expr.count("(") == 1:
        current_expr = current_expr[1:-1].strip()

    # Regex logic to find the next BODMAS operation
    match = re.search(r'\(\s*(-?\d+\.?\d*)\s*([\+\-\*\/])\s*(-?\d+\.?\d*)\s*\)', current_expr)
    if not match:
        match = re.search(r'(-?\d+\.?\d*)\s*([\*\/])\s*(-?\d+\.?\d*)', current_expr)
        if not match:
            match = re.search(r'(-?\d+\.?\d*)\s*([\+\-])\s*(-?\d+\.?\d*)', current_expr)
            
    if match:
        num1, op_char, num2 = match.groups()
        op_map = {'+': 'add', '-': 'subtract', '*': 'multiply', '/': 'divide'}
        return {
            "agent_history": base_update["agent_history"],
            "next_target_op": {
                "op": op_map[op_char],
                "args": [float(num1), float(num2)],
                "original_match": match.group(0)
            },
            "current_expression": current_expr
        }
        
    llm = get_llm()
    structured_llm = llm.with_structured_output(OperationToken)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a mathematical expression parser strictly following BODMAS precedence rules (Brackets, Orders, Divide/Multiply, Add/Subtract).
        
        First, check if the expression is mathematically valid and complete. If it is incomplete (e.g. '10 +', '15 /', unbalanced brackets), set is_valid=False and provide an error_message.
        
        If it is valid, find the MOST IMMEDIATE NEXT step to evaluate in the following expression.
        You must find the innermost brackets first! Inside those brackets, follow Division/Multiplication before Addition/Subtraction.
        Extract exactly ONE atomic operation (two numbers and one operator).
        
        Return the operation type ('add', 'subtract', 'multiply', 'divide'), the two numerical arguments, and the exact string match.
        
        Examples:
        - In '10 / (3 + 2)', the innermost brackets contain '3 + 2', so return: op='add', args=[3, 2], original_match='3 + 2'
        - In '48 / (2 * (10 - 4))', the innermost brackets contain '10 - 4', so return: op='subtract', args=[10, 4], original_match='10 - 4'
        - In '48 / (2 * 6)', the innermost brackets contain '2 * 6', so return: op='multiply', args=[2, 6], original_match='2 * 6'
        - In '48 / 12 + 5', division comes first, so return: op='divide', args=[48, 12], original_match='48 / 12'
        - In '3 + 1', return: op='add', args=[3, 1], original_match='3 + 1'
        
        You MUST respond ONLY with a raw JSON object matching the required schema. Do not include markdown formatting or conversational text.
        """),
        ("user", "Expression: {expression}")
    ])
    
    chain = prompt | structured_llm
    
    try:
        result = chain.invoke({"expression": current_expr})
        
        if not result.is_valid:
            return {"error_context": {"code": "INCOMPLETE_EXPRESSION", "msg": result.error_message or "Expression is incomplete or invalid."}}
            
        target_op = {
            "op": result.op,
            "args": result.args,
            "original_match": result.original_match
        }
        
        return {
            "agent_history": base_update["agent_history"],
            "next_target_op": target_op,
            "current_expression": current_expr # Update in case we stripped parens
        }
    except Exception as e:
        return {"error_context": {"code": "PLANNER_ERROR", "msg": f"Failed to parse expression: {str(e)}"}}
