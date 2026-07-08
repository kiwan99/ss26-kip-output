import requests
import pytest

@pytest.mark.parametrize("title", ["Test Todo", "Another Todo", "Yet Another"])
def test_add_and_get_active(title):
    add_response = requests.post("http://sandbox-app:8000/add", json={"title": title})
    assert add_response.status_code == 201
    item_id = add_response.json()["id"]
    active_list = requests.get("http://sandbox-app:8000/active").json()
    assert any(item["id"] == item_id and item["title"] == title for item in active_list)

def test_mark_done_and_check_done_list():
    add_response = requests.post("http://sandbox-app:8000/add", json={"title": "Test Done"})
    assert add_response.status_code == 201
    item_id = add_response.json()["id"]
    done_response = requests.post(f"http://sandbox-app:8000/done/{item_id}")
    assert done_response.status_code == 200
    done_list = requests.get("http://sandbox-app:8000/done_list").json()
    assert any(item["id"] == item_id for item in done_list)

def test_done_list_not_in_active():
    add_response = requests.post("http://sandbox-app:8000/add", json={"title": "Done Item"})
    assert add_response.status_code == 201
    item_id = add_response.json()["id"]
    done_response = requests.post(f"http://sandbox-app:8000/done/{item_id}")
    assert done_response.status_code == 200
    active_list = requests.get("http://sandbox-app:8000/active").json()
    assert not any(item["id"] == item_id for item in active_list)