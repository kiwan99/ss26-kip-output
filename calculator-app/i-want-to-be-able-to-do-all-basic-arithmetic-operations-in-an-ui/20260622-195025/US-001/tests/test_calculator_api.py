import pytest
import requests

@pytest.mark.api
def test_addition_api():
    response = requests.post('http://sandbox-app:8000', data={'num1': '5', 'num2': '3', 'operation': 'add'})
    assert response.status_code == 200
    assert response.text == 'Result: 8.0'

@pytest.mark.api
def test_subtraction_api():
    response = requests.post('http://sandbox-app:8000', data={'num1': '10', 'num2': '2', 'operation': 'subtract'})
    assert response.status_code == 200
    assert response.text == 'Result: 8.0'

@pytest.mark.api
def test_multiplication_api():
    response = requests.post('http://sandbox-app:8000', data={'num1': '4', 'num2': '5', 'operation': 'multiply'})
    assert response.status_code == 200
    assert response.text == 'Result: 20.0'

@pytest.mark.api
def test_division_api():
    response = requests.post('http://sandbox-app:8000', data={'num1': '10', 'num2': '2', 'operation': 'divide'})
    assert response.status_code == 200
    assert response.text == 'Result: 5.0'

@pytest.mark.api
def test_division_by_zero_api():
    response = requests.post('http://sandbox-app:8000', data={'num1': '10', 'num2': '0', 'operation': 'divide'})
    assert response.status_code == 200
    assert response.text == 'Error: Division by zero'