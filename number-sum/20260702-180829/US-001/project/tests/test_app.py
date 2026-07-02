import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask, jsonify
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sum_numbers(client):
    response = client.get('/sum?a=5&b=7')
    assert response.status_code == 200
    assert response.json == {'sum': 12}