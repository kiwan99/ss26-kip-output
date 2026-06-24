import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, db
from models import ToDo
import os

test_db_uri = 'sqlite:///:memory:'

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_todo(client):
    client.post('/add', data={'text': 'Test Todo'})
    with app.app_context():
        todo = ToDo.query.filter_by(text='Test Todo').first()
        assert todo is not None
        assert todo.completed is False

def test_mark_done(client):
    # Add a todo first
    client.post('/add', data={'text': 'Mark Me'})
    
    # Mark it done
    todo = ToDo.query.filter_by(text='Mark Me').first()
    assert todo is not None
    todo.completed = True
    db.session.commit()
    
    # Check it appears in done list
    response = client.get('/')
    assert b'Mark Me' in response.data
    assert b'completed' in response.data