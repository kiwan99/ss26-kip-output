import pytest
from flask import Flask
from project.app import app, active_items

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_todo_item(client):
    # Submit the form with "Test Item"
    response = client.post("/", data={"todo_item": "Test Item"})
    assert response.status_code == 200

    # Check that the active_items list contains "Test Item"
    assert "Test Item" in active_items

    # Check that the response HTML does not have the input field with "Test Item"
    html = response.get_data(as_text=True)
    assert "value=\"Test Item\"" not in html