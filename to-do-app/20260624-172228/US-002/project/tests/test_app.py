import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, tasks
from tasks import Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_task(client):
    tasks.add('Test task')
    response = client.get('/active')
    assert response.status_code == 200
    assert b'Test task' in response.data

def test_mark_done(client):
    tasks.add('Test task')
    task = tasks.get_all()[0]
    task_id = task.id
    response = client.post(f'/mark_done/{task_id}')
    assert response.status_code == 302
    task = tasks.get_all()[0]
    assert task.done is True