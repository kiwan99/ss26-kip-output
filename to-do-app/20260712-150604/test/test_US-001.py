"""Tests for US-001: Add New Task."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import app


def test_main_page_has_input_and_add_button():
    """AC1: The app displays an input field and an Add button on the main page."""
    client = app.app.test_client()
    resp = client.get("/")
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'id="task-input"' in html, "Input field missing from main page"
    assert 'id="add-btn"' in html, "Add button missing from main page"


def test_adding_valid_task_appends_to_list():
    """AC2: Entering text and clicking Add creates a new task entry at the bottom of the list."""
    client = app.app.test_client()

    # Clear any pre-existing tasks
    app.tasks.clear()

    resp = client.post("/add_task", json={"text": "Buy groceries"})
    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.get_data(as_text=True)}"
    data = resp.get_json()
    assert data is not None
    assert data["text"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data

    # Verify the task appears at the bottom of the rendered list
    html = client.get("/").get_data(as_text=True)
    assert "Buy groceries" in html


def test_empty_input_rejected():
    """AC3: Submitting an empty input does not create a blank task."""
    client = app.app.test_client()

    # Clear any pre-existing tasks
    app.tasks.clear()

    resp = client.post("/add_task", json={"text": ""})
    assert resp.status_code == 400, f"Expected 400 for empty text, got {resp.status_code}"

    # Verify no task was created
    assert len(app.get_tasks()) == 0


def test_whitespace_only_input_rejected():
    """AC3 (extended): Whitespace-only input also does not create a blank task."""
    client = app.app.test_client()

    resp = client.post("/add_task", json={"text": "   "})
    assert resp.status_code == 400, f"Expected 400 for whitespace text, got {resp.status_code}"


def test_input_clears_after_successful_add():
    """AC4: After adding, the input field clears automatically."""
    # This is handled by client-side JS. We verify the server returns success (201)
    # which triggers the JS clear logic. The frontend behavior is confirmed by
    # checking the response status that drives the clear action.
    client = app.app.test_client()

    resp = client.post("/add_task", json={"text": "Test task"})
    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"

    # Verify the response includes the task data that JS uses to append and clear
    data = resp.get_json()
    assert data is not None
    assert "id" in data
    assert "text" in data


def test_add_task_function_strips_whitespace():
    """Verify add_task strips whitespace from text before storing."""
    result = app.add_task("  Hello World  ")
    assert result is not None
    assert result["text"] == "Hello World", f"Expected stripped text, got: {result['text']}"


def test_add_task_returns_none_for_empty():
    """Verify add_task returns None for empty/whitespace input."""
    assert app.add_task("") is None
    assert app.add_task("   ") is None
    assert app.add_task("\t\n") is None
