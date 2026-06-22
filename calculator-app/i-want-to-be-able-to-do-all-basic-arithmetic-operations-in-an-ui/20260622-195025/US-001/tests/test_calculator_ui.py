import pytest
from playwright.sync_api import Page

@pytest.mark.ui
def test_ui_elements(page: Page):
    page.goto('http://sandbox-app:8000')
    page.screenshot(path="/tests/screenshots/ui_elements_before.png")
    
    # Check operation dropdown options
    options = page.query_selector_all("select[name='operation'] option")
    assert len(options) == 4, "Missing operation options"
    operations = [option.text_content() for option in options]
    assert 'Add' in operations
    assert 'Subtract' in operations
    assert 'Multiply' in operations
    assert 'Divide' in operations
    
    # Check input fields
    num1 = page.query_selector("input[name='num1']")
    assert num1 is not None, "Missing num1 input"
    num2 = page.query_selector("input[name='num2']")
    assert num2 is not None, "Missing num2 input"
    
    # Check calculate button
    button = page.query_selector("button[type='submit']")
    assert button is not None, "Missing calculate button"
    page.screenshot(path="/tests/screenshots/ui_elements_after.png")

@pytest.mark.ui
def test_addition(page: Page):
    page.goto('http://sandbox-app:8000')
    page.fill("input[name='num1']", "5")
    page.select_option("select[name='operation']", "add")
    page.fill("input[name='num2']", "3")
    page.click("button[type='submit']")
    
    result = page.query_selector("body > h1 + div")
    assert result is not None, "Result not found"
    assert result.text_content() == "Result: 8.0", "Incorrect addition result"
    page.screenshot(path="/tests/screenshots/addition_result.png")

@pytest.mark.ui
def test_division_by_zero(page: Page):
    page.goto('http://sandbox-app:8000')
    page.fill("input[name='num1']", "10")
    page.select_option("select[name='operation']", "divide")
    page.fill("input[name='num2']", "0")
    page.click("button[type='submit']")
    
    error = page.query_selector("body > h1 + div")
    assert error is not None, "Error message not found"
    assert error.text_content() == "Error: Division by zero", "Incorrect error message"
    page.screenshot(path="/tests/screenshots/division_error.png")