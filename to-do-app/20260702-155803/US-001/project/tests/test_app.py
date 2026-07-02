import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_add_todo_item(client):
    response = client.post("/", data={"todo": "Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Task" in response.data

def test_empty_submission(client):
    response = client.post("/", data={"todo": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"" not in response.data