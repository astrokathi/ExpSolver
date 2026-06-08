import pytest
import os

@pytest.fixture(autouse=True)
def disable_telemetry_for_tests():
    """Ensure Langfuse is disabled during pytest runs."""
    os.environ["LANGFUSE_PUBLIC_KEY"] = ""
    os.environ["LANGFUSE_SECRET_KEY"] = ""
    os.environ["LANGFUSE_HOST"] = ""
