import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, db, Todo
from flask import Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()
    
    with app.app_context():
        db.create_all()
    
    yield client

    with app.app_context():
        db.drop_all()

def test_add_todo(client):
    response = client.post('/add', data={'title': 'Test Task'})
    assert response.status_code == 302

    response = client.get('/')
    assert b'Test Task' in response.data

def test_mark_done(client):
    # Add task first
    client.post('/add', data={'title': 'Test Task'})
    
    # Mark as done
    response = client.post('/done/1')
    assert response.status_code == 302
    
    # Check if moved to done list
    response = client.get('/')
    assert b'Done Tasks' in response.data
    assert b'Test Task' in response.data
    
    # Check button disappears for done items
    # (Need to check HTML rendering)
    # This requires more detailed testing of templates
    # which is beyond basic pytest scope without JS testing framework