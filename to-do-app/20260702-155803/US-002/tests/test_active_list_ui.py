import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.playwright
def test_active_list_has_done_buttons():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    try:
        page.goto('http://sandbox-app:8000/active')
        
        # Take screenshot of active list page
        page.screenshot(path="/tests/screenshots/active_list_initial.png")
        
        # Check for presence of 'Done' buttons
        done_buttons = page.locator("button[aria-label='Mark as done']").count()
        assert done_buttons > 0, f"No 'Done' buttons found in active list"
        
        # Take screenshot showing buttons
        page.screenshot(path="/tests/screenshots/active_list_buttons.png")
    finally:
        browser.close()
        playwright.stop()


@pytest.mark.playwright
def test_marking_item_as_done():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    try:
        page.goto('http://sandbox-app:8000/active')
        
        # Click first 'Done' button
        page.click("button[aria-label='Mark as done']:first")
        
        # Take screenshot after clicking
        page.screenshot(path="/tests/screenshots/item_marked_done.png")
        
        # Verify item was moved to done list
        page.goto('http://sandbox-app:8000/done')
        
        # Check for presence of previously active item in done list
        assert page.locator("li:has-text('Buy groceries')").count() > 0, "Item not found in done list"
        
        # Take screenshot of done list
        page.screenshot(path="/tests/screenshots/done_list_after_move.png")
    finally:
        browser.close()
        playwright.stop()