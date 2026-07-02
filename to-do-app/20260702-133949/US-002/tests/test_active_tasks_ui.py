import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser_instance():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    context = browser.new_context()
    yield context
    context.close()
    browser.close()
    playwright.stop()

def test_active_tasks_list(browser_instance):
    page = browser_instance.new_page()
    page.goto("http://sandbox-app:8000")
    
    # Take screenshot of initial active tasks list
    page.screenshot(path="/tests/screenshots/active_tasks_initial.png")

    # Verify active tasks are displayed
    task1 = page.locator("li:has-text('Task 1')")
    task3 = page.locator("li:has-text('Task 3')")
    task2 = page.locator("li:has-text('Task 2')")

    assert task1.is_visible()
    assert task3.is_visible()
    assert not task2.is_visible()

    # Verify Done buttons exist for active tasks
    done_button_task1 = task1.locator("input[value='Done']")
    done_button_task3 = task3.locator("input[value='Done']")

    assert done_button_task1.is_visible()
    assert done_button_task3.is_visible()

    # Click Done button for Task 3 and verify it disappears
    done_button_task3.click()
    page.wait_for_load_state("networkidle")
    page.screenshot(path="/tests/screenshots/task3_marked_done.png")

    task3_after = page.locator("li:has-text('Task 3')")
    assert not task3_after.is_visible()

    # Verify Task 1 still exists
    assert task1.is_visible()