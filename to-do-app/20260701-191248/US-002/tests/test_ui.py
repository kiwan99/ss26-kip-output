import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("test_name, item_text, expected_text", [
    ("Add item via form", "Test Form Item", "Test Form Item"),
    ("Add item via API", "Test API Item", "Test API Item")
])
def test_active_list_updates(test_name, item_text, expected_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('http://sandbox-app:8000')

        # Take initial screenshot
        page.screenshot(path="/tests/screenshots/initial_page.png")

        # Test form submission
        if test_name == "Add item via form":
            page.fill("#todo-text", item_text)
            page.click("#add-form button")
            page.wait_for_selector(f"li:has-text('{expected_text}')")
            page.screenshot(path="/tests/screenshots/form_submission.png")
        
        # Test API addition
        if test_name == "Add item via API":
            page.evaluate(f"""fetch('/add', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                body: 'text={item_text}'
            }})""")
            page.wait_for_selector(f"li:has-text('{expected_text}')")
            page.screenshot(path="/tests/screenshots/api_submission.png")

        # Verify item appears in list
        assert page.locator(f"li:has-text('{expected_text}')").count() > 0

        browser.close()