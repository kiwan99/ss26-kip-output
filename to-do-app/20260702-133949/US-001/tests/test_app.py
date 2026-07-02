import requests

def test_add_task_api():
    response = requests.post("http://sandbox-app:8000", data={"task": "Test Task"})
    assert response.status_code == 200
    assert "Test Task" in response.text