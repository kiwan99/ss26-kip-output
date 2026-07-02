import pytest
from flask import Flask
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, active_items, done_items

@pytest.fixture(autouse=True)
def reset_app_state():
    global active_items, done_items
    active_items = ["Buy groceries", "Walk the dog", "Finish report"]
    done_items = []
    yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_active_items_initial_state():
    assert active_items == ["Buy groceries", "Walk the dog", "Finish report"]
    assert done_items == []

def test_mark_item_as_done(client):
    # Mark first item as done
    response = client.get('/mark_done/0')
    assert response.status_code == 302

    # Check if item was moved
    assert active_items == ["Walk the dog", "Finish report"]
    assert done_items == ["Buy groceries"]

def test_active_page_rendering(client):
    response = client.get('/active')
    assert response.status_code == 200
    assert b"Buy groceries" in response.data
    assert b"Walk the dog" in response.data
    assert b"Finish report" in response.data

def test_done_page_rendering(client):
    # First, add an item to done
    client.get('/mark_done/0')
    response = client.get('/done')
    assert response.status_code == 200
    assert b"Buy groceries" in response.data
    assert b"Walk the dog" not in response.data