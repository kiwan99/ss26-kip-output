import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Basic Calculator' in response.data

def test_index_post_add(client):
    response = client.post('/', data={
        'num1': '2',
        'num2': '3',
        'operation': 'add'
    })
    assert response.status_code == 200
    assert b'Result: 5.0' in response.data

def test_index_post_subtract(client):
    response = client.post('/', data={
        'num1': '10',
        'num2': '5',
        'operation': 'subtract'
    })
    assert response.status_code == 200
    assert b'Result: 5.0' in response.data

def test_index_post_multiply(client):
    response = client.post('/', data={
        'num1': '4',
        'num2': '5',
        'operation': 'multiply'
    })
    assert response.status_code == 200
    assert b'Result: 20.0' in response.data

def test_index_post_divide(client):
    response = client.post('/', data={
        'num1': '10',
        'num2': '2',
        'operation': 'divide'
    })
    assert response.status_code == 200
    assert b'Result: 5.0' in response.data

def test_index_post_divide_by_zero(client):
    response = client.post('/', data={
        'num1': '10',
        'num2': '0',
        'operation': 'divide'
    })
    assert response.status_code == 200
    assert b'Error: Division by zero' in response.data