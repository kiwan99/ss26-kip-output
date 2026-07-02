import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_form_elements_present(page):
    page.goto("http://sandbox-app:8000")
    page.screenshot(path="/tests/screenshots/initial_page.png")
    assert page.locator("input[name='task']").is_visible()
    assert page.locator("button[type='submit']").is_visible()

def test_adding_task_displays_in_list(page):
    page.goto("http://sandbox-app:8000")
    page.fill("input[name='task']", "Test Task")
    page.click("button[type='submit']")
    page.wait_for_selector("ul li", timeout=5000)
    assert page.locator("ul li").text_content() == "Test Task"
    page.screenshot(path="/tests/screenshots/task_added.png")