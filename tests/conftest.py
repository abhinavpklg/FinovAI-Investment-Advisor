import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def env_setup():
    """Automatically load environment variables for all tests"""
    load_dotenv() 