import os
from typing import Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
import httpx

load_dotenv()

def get_llm() -> Any:
    """
    LLM Factory following fallback rules:
    1. Local Ollama (default check)
    2. OpenAI API
    3. Anthropic API
    """
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Simple check if Ollama is accessible
    try:
        response = httpx.get(ollama_url, timeout=2.0)
        if response.status_code == 200:
            print("[LLM FACTORY] Using Local Ollama.")
            return ChatOllama(base_url=ollama_url, model="gemma4:e4b", temperature=0, format="json")
    except httpx.RequestError:
        print("[LLM FACTORY] Local Ollama not reachable.")
        pass

    # Fallback 1: OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        print("[LLM FACTORY] Using OpenAI.")
        return ChatOpenAI(api_key=openai_key, model="gpt-4o", temperature=0)
        
    # Fallback 2: Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        print("[LLM FACTORY] Using Anthropic.")
        return ChatAnthropic(api_key=anthropic_key, model="claude-3-5-sonnet-20240620", temperature=0)

    # If all fail, throw an error
    raise ValueError("No reachable LLM providers configured. Check your .env file or ensure Ollama is running.")

def get_langfuse_handler() -> Any:
    """
    Initializes and returns the Langfuse callback handler if keys are present.
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    
    if public_key and secret_key:
        try:
            from langfuse.langchain import CallbackHandler
            return CallbackHandler()
        except ImportError:
            print("WARNING: Langfuse not installed. Returning None.")
    return None
