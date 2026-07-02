import pytest
from playwright.sync_api import Playwright, sync_playwright

@pytest.mark.playwright
def test_form_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://sandbox-app:8000")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="/tests/screenshots/test_form_elements.png")
        assert page.locator("input[name='todo']").is_visible()
        assert page.locator("input[type='submit']").is_visible()
        browser.close()

@pytest.mark.playwright
def test_add_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://sandbox-app:8000")
        page.wait_for_load_state("networkidle")
        page.fill("input[name='todo']", "Test Task")
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="/tests/screenshots/test_add_task.png")
        assert "Test Task" in page.text_content("ul")
        browser.close()