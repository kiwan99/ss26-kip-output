import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, db
from flask import jsonify
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_add_todo(client):
    response = client.post('/add', json={'title': 'Test Todo'})
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Todo added'

def test_mark_done(client):
    # Add a todo first
    client.post('/add', json={'title': 'Mark Me'})
    
    # Get the ID of the added item
    response = client.get('/active')
    data = json.loads(response.data)
    item_id = data[0]['id']

    # Mark it as done
    response = client.put(f'/done/{item_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Marked as done'

def test_get_done_list(client):
    # Add a todo and mark it as done
    client.post('/add', json={'title': 'Done Item'})
    response = client.get('/active')
    data = json.loads(response.data)
    item_id = data[0]['id']
    client.put(f'/done/{item_id}')

    # Check done list
    response = client.get('/done_list')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    assert data[0]['title'] == 'Done Item'