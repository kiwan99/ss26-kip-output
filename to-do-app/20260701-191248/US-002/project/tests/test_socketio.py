import pytest
from ..app import app, socketio

@pytest.fixture
def socketio_client():
    app.config['TESTING'] = True
    client = socketio.test_client(app)
    return client

def test_socketio_emit(socketio_client):
    socketio_client.emit('item_added', {'text': 'Test'})
    # This test might require additional setup to verify event emission