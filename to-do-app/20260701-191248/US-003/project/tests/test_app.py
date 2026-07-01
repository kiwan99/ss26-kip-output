import pytest
from ..app import app, todos, done_todos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_mark_done(client):
    # Add a test todo
    todos.append({'id': 2, 'text': 'Test Todo', 'done': False})
    # Submit the form to mark done
    response = client.post('/', data={'todo_id': 2})
    # Check that the todo is now in done_todos
    assert len(done_todos) == 1
    assert done_todos[0]['id'] == 2
    assert len(todos) == 1