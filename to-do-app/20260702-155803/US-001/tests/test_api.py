import requests
def test_add_via_api():
    response = requests.post("http://sandbox-app:8000", data={"todo": "Test via API"}, allow_redirects=True)
    assert "Test via API" in response.text