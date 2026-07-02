import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_task(client):
    response = client.post("/", data={"task": "Test Task"}, follow_redirects=True)
    assert b"Test Task" in response.data