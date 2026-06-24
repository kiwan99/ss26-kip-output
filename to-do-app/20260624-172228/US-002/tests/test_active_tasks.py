import pytest
from playwright.sync_api import sync_playwright

def test_active_tasks():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Add a task and check it's displayed
        page.goto("http://sandbox-app:8000/active")
        page.request.post("http://sandbox-app:8000/add_task", json={"task": "Task 1"})
        page.goto("http://sandbox-app:8000/active")
        task_element = page.locator("ul li").first
        assert task_element.text_content() == "Task 1"
        task_element.screenshot(path="/tests/screenshots/task_displayed.png")
        
        # Check for Done button
        done_button = page.locator("button").first
        assert done_button.text_content() == "Done"
        done_button.screenshot(path="/tests/screenshots/done_button.png")
        
        # Add another task and check order
        page.request.post("http://sandbox-app:8000/add_task", json={"task": "Task 2"})
        page.goto("http://sandbox-app:8000/active")
        tasks = page.locator("ul li").all()
        assert len(tasks) == 2
        assert tasks[0].text_content() == "Task 1"
        assert tasks[1].text_content() == "Task 2"
        page.screenshot(path="/tests/screenshots/tasks_order.png")
        
        # Mark Task 1 as done and check it's not in Active list
        page.request.post("http://sandbox-app:8000/mark_done", json={"task": "Task 1"})
        page.goto("http://sandbox-app:8000/active")
        active_tasks = page.locator("ul li").all()
        assert len(active_tasks) == 1
        assert active_tasks[0].text_content() == "Task 2"
        page.screenshot(path="/tests/screenshots/task_marked_done.png")
        
        browser.close()