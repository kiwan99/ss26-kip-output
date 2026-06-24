import pytest
from flask import Flask
from models import db, Todo
from app import app

@pytest.fixture
def test_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_routes(test_app):
    client = test_app.test_client()

    # Test adding item
    response = client.post('/add', data={'content': 'Test Item'})
    assert response.status_code == 302

    # Test mark as done
    response = client.get('/done/1')
    assert response.status_code == 302

    # Test done list
    response = client.get('/done')
    assert response.status_code == 200
    assert b'Test Item' in response.data