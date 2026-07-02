import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Task 1' in response.data
    assert b'Task 3' in response.data
    assert b'Task 2' not in response.data

def test_mark_done(client):
    assert tasks[2]['done'] is False
    response = client.post('/done/3')
    assert response.status_code == 302
    assert tasks[2]['done'] is True