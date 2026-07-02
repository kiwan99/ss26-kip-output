import requests
import pytest

@pytest.mark.parametrize("params,expected_sum", [
    ("a=5&b=7", 12),
    ("a=-3&b=5", 2),
    ("a=0&b=0", 0),
    ("a=100&b=200", 300),
    ("a=123456789&b=987654321", 1111111110),
    ("a=1&a=2", 3),  # Duplicate parameter (only first is used)
])
def test_api_sum(params, expected_sum):
    url = "http://sandbox-app:8000/sum?" + params
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200
        assert response.json()["sum"] == expected_sum
    except Exception as e:
        pytest.fail(f"Request failed: {str(e)}")