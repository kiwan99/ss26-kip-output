import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Calculate Sum' in response.data

def test_calculate_sum(client):
    response = client.post('/', data={'num1': '3', 'num2': '5'})
    assert response.status_code == 200
    assert b'Sum: 8' in response.data

def test_invalid_input(client):
    response = client.post('/', data={'num1': 'a', 'num2': '5'})
    assert response.status_code == 200
    assert b'Sum:' not in response.data