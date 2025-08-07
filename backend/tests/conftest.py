import os
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def ensure_data_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/storage", exist_ok=True)
