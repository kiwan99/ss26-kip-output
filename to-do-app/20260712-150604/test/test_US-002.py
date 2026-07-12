"""Tests for US-002: View and Mark Tasks as Complete."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import json
import pytest
from app import app, tasks


@pytest.fixture
def client():
    """Flask test client with clean task state per test."""
    tasks.clear()
    return app.test_client()


# ── AC1: All added tasks are displayed in a list on the main page. ──

def test_add_task_displays_in_list(client):
    """Adding a task via /add_task makes it appear in the task list on /.

    Covers AC1 (displayed in list) and AC2 (text content visible).
    """
    # Add two tasks
    r1 = client.post("/add_task", json={"text": "Buy groceries"})
    assert r1.status_code == 201, f"Add task failed: {r1.get_data(as_text=True)}"

    r2 = client.post("/add_task", json={"text": "Walk the dog"})
    assert r2.status_code == 201, f"Add task failed: {r2.get_data(as_text=True)}"

    # GET main page and verify both tasks appear in the list
    resp = client.get("/")
    html = resp.get_data(as_text=True)

    assert "<ul id=\"task-list\">" in html, "Task list element missing from page."
    assert "Buy groceries" in html, "First task text not displayed."
    assert "Walk the dog" in html, "Second task text not displayed."


# ── AC3: Clicking checkbox marks complete with visual indicator. ──

def test_toggle_marks_complete_with_visual_indicator(client):
    """Toggling a task sets completed=True and page shows strikethrough/dimmed style."""
    # Add a task
    r = client.post("/add_task", json={"text": "Read a book"})
    assert r.status_code == 201
    task_data = json.loads(r.get_data(as_text=True))
    task_id = task_data["id"]

    # Toggle it complete via API
    toggle_resp = client.post("/toggle_task", json={"id": task_id})
    assert toggle_resp.status_code == 200, f"Toggle failed: {toggle_resp.get_data(as_text=True)}"
    updated = json.loads(toggle_resp.get_data(as_text=True))
    assert updated["completed"] is True

    # Verify the main page renders with visual indicator (completed class + checked box)
    resp = client.get("/")
    html = resp.get_data(as_text=True)

    # The template adds 'completed' class to span when task.completed is True
    assert "task-text completed" in html, "Visual indicator (completed class) missing."
    assert "checked" in html, "Checkbox not marked as checked for completed task."


# ── AC4: Clicking again removes completion state. ──

def test_toggle_again_removes_completion(client):
    """Toggling a completed task back restores original appearance."""
    # Add and complete a task
    r = client.post("/add_task", json={"text": "Call mom"})
    assert r.status_code == 201
    task_data = json.loads(r.get_data(as_text=True))
    task_id = task_data["id"]

    # First toggle: mark complete
    t1 = client.post("/toggle_task", json={"id": task_id})
    d1 = json.loads(t1.get_data(as_text=True))
    assert d1["completed"] is True

    # Second toggle: remove completion
    t2 = client.post("/toggle_task", json={"id": task_id})
    assert t2.status_code == 200
    d2 = json.loads(t2.get_data(as_text=True))
    assert d2["completed"] is False, "Task should be incomplete after second toggle."

    # Verify page renders without visual indicator
    resp = client.get("/")
    html = resp.get_data(as_text=True)

    # The task text span should NOT have the 'completed' class
    # Check that for this specific task, there's no "task-text completed" near its text
    assert "Call mom" in html, "Task disappeared from list."
    lines = html.split("\n")
    found_task_line = False
    for line in lines:
        if "Call mom" in line:
            found_task_line = True
            assert "task-text completed" not in line, \
                "Completion indicator still present after un-toggling."
            break
    assert found_task_line, "Task text line not found in HTML."


# ── Integration test (uses Flask test client, no live server needed) ──

def test_integration_add_view_toggle(client):
    """End-to-end: add task, view it on page, toggle complete, verify visual change."""
    # Step 1: Add a task
    r = client.post("/add_task", json={"text": "Integration test"})
    assert r.status_code == 201
    task_data = json.loads(r.get_data(as_text=True))
    task_id = task_data["id"]

    # Step 2: View main page — task should be in list, not completed
    resp = client.get("/")
    html_before = resp.get_data(as_text=True)
    assert "Integration test" in html_before
    for line in html_before.split("\n"):
        if "Integration test" in line:
            assert "task-text completed" not in line

    # Step 3: Toggle complete
    t = client.post("/toggle_task", json={"id": task_id})
    d = json.loads(t.get_data(as_text=True))
    assert d["completed"] is True

    # Step 4: View main page again — visual indicator should appear
    resp2 = client.get("/")
    html_after = resp2.get_data(as_text=True)
    for line in html_after.split("\n"):
        if "Integration test" in line:
            assert "task-text completed" in line, \
                "Visual indicator (strikethrough/dimmed) not applied after toggle."
            break

    # Step 5: Toggle back to incomplete
    t2 = client.post("/toggle_task", json={"id": task_id})
    d2 = json.loads(t2.get_data(as_text=True))
    assert d2["completed"] is False

    # Step 6: Verify visual indicator removed
    resp3 = client.get("/")
    html_final = resp3.get_data(as_text=True)
    for line in html_final.split("\n"):
        if "Integration test" in line:
            assert "task-text completed" not in line, \
                "Completion indicator persists after un-toggling."
            break


# ── Edge case: toggle non-existent task returns 404 ──

def test_toggle_nonexistent_task_returns_404(client):
    """Toggling a task ID that doesn't exist returns 404."""
    resp = client.post("/toggle_task", json={"id": "nonexistent-id"})
    assert resp.status_code == 404
