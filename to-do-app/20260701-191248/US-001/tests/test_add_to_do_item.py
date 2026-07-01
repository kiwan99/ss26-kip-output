from playwright.sync_api import sync_playwright

def test_add_to_do_item():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Take screenshot of initial page
        page.screenshot(path="/tests/screenshots/initial_page.png")
        
        # Navigate to app
        page.goto("http://sandbox-app:8000")
        
        # Fill form and submit
        page.fill("input[name=todo_item]", "Test Item")
        page.click("button[type=submit]")
        
        # Take screenshot after submission
        page.screenshot(path="/tests/screenshots/after_submission.png")
        
        # Verify item appears in active list
        item_locator = page.locator("ul > li").first
        assert item_locator.text_content() == "Test Item"
        
        # Verify input field is cleared
        input_field = page.locator("input[name=todo_item]")
        assert input_field.input_value() == ""
        
        browser.close()