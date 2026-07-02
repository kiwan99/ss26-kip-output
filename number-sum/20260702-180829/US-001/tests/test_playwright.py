from playwright.sync_api import sync_playwright
import pytest

@pytest.mark.skip(reason="No UI implementation, only API endpoint")
def test_ui_sum():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to UI (this will fail if no UI exists)
        page.goto("http://sandbox-app:8000")
        
        # Attempt to submit form values (if UI existed)
        page.fill("input[name='a']", "5")
        page.fill("input[name='b']", "7")
        page.click("button[type='submit']")
        
        # Save screenshot (even if UI doesn't exist)
        page.screenshot(path="/tests/screenshots/ui_sum_test.png")
        
        # Validate result (this will fail if no UI exists)
        assert page.locator("#result").text_content() == "Sum: 12"
        
        browser.close()