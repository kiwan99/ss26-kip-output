import requests

def test_add_task():
    response = requests.post('http://localhost:8000', data={'task': 'Test Task'})
    assert response.status_code == 200
    assert 'Test Task' in response.text