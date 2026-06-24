import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("todo_text", ["Buy groceries", "Walk the dog", "Finish report"])
def test_mark_todo_as_done(todo_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Take initial screenshot
        page.screenshot(path="/tests/screenshots/initial_page.png")
        
        try:
            page.goto("http://sandbox-app:8080")  # Corrected port to 8080
            
            # Wait for the input field to be present
            page.wait_for_selector("#todo-input", timeout=10000)
            
            # Test 1: Verify empty lists initially
            assert page.locator(".active-list li").count() == 0
            assert page.locator(".done-list li").count() == 0
            
            # Test 2: Add new To-Do
            page.fill("#todo-input", todo_text)
            page.click("#add-todo-btn")
            
            # Screenshot after adding
            page.screenshot(path=f"/tests/screenshots/added_{todo_text.replace(' ', '_')}.png")
            
            # Verify active list has item
            assert page.locator(".active-list li").text_content() == todo_text
            
            # Test 3: Mark as done
            page.click(".checkbox")
            
            # Screenshot after marking done
            page.screenshot(path=f"/tests/screenshots/marked_done_{todo_text.replace(' ', '_')}.png")
            
            # Verify active list is empty
            assert page.locator(".active-list li").count() == 0
            
            # Verify done list has item
            assert page.locator(".done-list li").text_content() == todo_text
            
        finally:
            browser.close()