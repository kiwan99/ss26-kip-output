import pytest
from flask import Flask
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app import app, todos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

test_data = [{'text': 'Sample Task 1'}, {'text': 'Sample Task 2'}]

def test_add_todo(client):
    # Test adding a single todo
    response = client.post('/add', json=test_data[0])
    assert response.json['success']
    assert test_data[0]['text'] in todos

    # Test adding another todo
    response = client.post('/add', json=test_data[1])
    assert response.json['success']
    assert all(t in todos for t in [test_data[0]['text'], test_data[1]['text']])

    # Test empty input
    response = client.post('/add', json={})
    assert response.json['success']
    assert len(todos) == 2