#!/usr/bin/env python3
import os
from src.graph import run_calculation
from src.config import get_langfuse_handler

print("Testing Langfuse Tracing Initialization...")

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-7426292a-2605-4bc9-bb22-4c9afd9461e6"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-8be29e03-d46b-44d8-a60a-d78019684eff"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

try:
    print("\nExecuting calculation: 10 + 2")
    res = run_calculation("10 + 2")
    print(f"Result: {res}")
except Exception as e:
    print(f"Calculation failed (this is expected if no LLM is running): {e}")

print("\nFlushing Langfuse events...")
from langfuse import Langfuse
Langfuse().flush()
print("Tracing flushed successfully. Check http://localhost:3000")
