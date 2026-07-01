import pytest
from ..app import app, todos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_to_do(client):
    response = client.post('/add', data={'text': 'Test Item'})
    assert response.status_code == 200
    assert response.json['success'] is True

def test_active_todos(client):
    client.post('/add', data={'text': 'Test1'})
    client.post('/add', data={'text': 'Test2'})
    response = client.get('/')
    assert b'Test1' in response.data
    assert b'Test2' in response.data