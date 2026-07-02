import pytest
from flask import Flask
from app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Active Tasks' in response.data
    assert b'Done Tasks' in response.data
    assert b'Task 1' in response.data
    assert b'Task 2' in response.data

def test_complete_task(client):
    response = client.get('/complete/1')
    assert response.status_code == 302
    assert tasks[0]["completed"] is True