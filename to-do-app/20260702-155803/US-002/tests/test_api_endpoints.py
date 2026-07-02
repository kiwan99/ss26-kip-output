import pytest
import requests


@pytest.mark.api
def test_api_initial_active_items():
    response = requests.get('http://sandbox-app:8000/api/items')
    assert response.status_code == 200
    data = response.json()
    assert len(data['active']) == 3
    assert 'Buy groceries' in data['active']
    assert 'Walk the dog' in data['active']
    assert 'Finish report' in data['active']
    
    # Check for encoding issues
    assert all(isinstance(item, str) for item in data['active'])


@pytest.mark.api
def test_api_mark_item_done():
    # Mark first item as done
    response = requests.post('http://sandbox-app:8000/api/items/0/mark_done')
    assert response.status_code == 200
    
    # Verify item was moved
    response = requests.get('http://sandbox-app:8000/api/items')
    assert response.status_code == 200
    data = response.json()
    assert 'Buy groceries' in data['done']
    assert 'Buy groceries' not in data['active']
    
    # Verify other items remain in active list
    assert 'Walk the dog' in data['active']
    assert 'Finish report' in data['active']