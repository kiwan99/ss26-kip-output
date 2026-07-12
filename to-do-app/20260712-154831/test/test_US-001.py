"""
Tests for US-001: View and Add New Tasks

Acceptance criteria coverage:
  AC1 - Page loads with text input box and Add button visible at the top.
        → test_page_contains_input_and_add_button
  AC2 - Typing text + clicking Add or pressing Enter creates a new task in list.
        → test_post_valid_task_returns_201, test_get_tasks_shows_added_task
  AC3 - Input field clears automatically after successfully adding a task.
        → test_successful_add_clears_input (verifies backend returns success status)
  AC4 - Submitting empty input does not create a blank task.
        → test_post_empty_text_returns_400, test_post_whitespace_only_returns_400

Integration tests:
  test_integration_page_loads
  test_integration_add_and_list_tasks
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import json
import pytest
import app


# ---------------------------------------------------------------------------
# Unit tests (Flask test_client — no running server required)
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Flask test client for unit testing routes."""
    app.app.config["TESTING"] = True
    with app.app.test_client() as c:
        yield c


class TestPageStructure:
    """AC1: The page loads with a text input box and an Add button visible at the top."""

    def test_page_contains_input_and_add_button(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        # Verify the input field exists with correct id
        assert 'id="task-input"' in html
        # Verify the Add button exists with correct id
        assert 'id="add-btn"' in html


class TestAddTask:
    """AC2 & AC3: Adding a task creates it; success response enables frontend clearing."""

    def test_post_valid_task_returns_201(self, client):
        resp = client.post(
            "/api/tasks",
            data=json.dumps({"text": "Buy groceries"}),
            content_type="application/json",
        )
        assert resp.status_code == 201
        body = json.loads(resp.get_data(as_text=True))
        assert body["text"] == "Buy groceries"
        assert body["completed"] is False

    def test_get_tasks_shows_added_task(self, client):
        # Add a task first
        client.post(
            "/api/tasks",
            data=json.dumps({"text": "Walk the dog"}),
            content_type="application/json",
        )
        # Verify it appears in GET response
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        tasks = json.loads(resp.get_data(as_text=True))
        assert len(tasks) >= 1
        texts = [t["text"] for t in tasks]
        assert "Walk the dog" in texts

    def test_successful_add_clears_input(self, client):
        """AC3: Backend returns 201 on success — frontend JS clears input on this signal.

        The actual DOM clearing is handled by script.js (taskInput.value = ""),
        which cannot be tested without browser automation. This test verifies
        the backend contract that enables the frontend behavior: a successful
        POST returns status 201, which triggers the clear in addTask().
        """
        resp = client.post(
            "/api/tasks",
            data=json.dumps({"text": "Test task"}),
            content_type="application/json",
        )
        # 201 Created signals success → frontend clears input
        assert resp.status_code == 201


class TestEmptyInput:
    """AC4: Submitting an empty input does not create a blank task."""

    def test_post_empty_text_returns_400(self, client):
        resp = client.post(
            "/api/tasks",
            data=json.dumps({"text": ""}),
            content_type="application/json",
        )
        assert resp.status_code == 400
        body = json.loads(resp.get_data(as_text=True))
        assert "error" in body

    def test_post_whitespace_only_returns_400(self, client):
        resp = client.post(
            "/api/tasks",
            data=json.dumps({"text": "   "}),
            content_type="application/json",
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Integration tests (httpx against running server at localhost:8000)
# ---------------------------------------------------------------------------

import httpx

BASE_URL = "http://localhost:8000"


class TestIntegration:
    """End-to-end HTTP tests against the running application."""

    def test_integration_page_loads(self):
        resp = httpx.get(BASE_URL + "/")
        assert resp.status_code == 200
        html = resp.text
        assert 'id="task-input"' in html
        assert 'id="add-btn"' in html
        assert 'id="task-list"' in html

    def test_integration_add_and_list_tasks(self):
        # Add a task via POST
        add_resp = httpx.post(
            BASE_URL + "/api/tasks",
            json={"text": "Integration test task"},
        )
        assert add_resp.status_code == 201
        created = add_resp.json()
        assert created["text"] == "Integration test task"

        # Verify it appears in GET /api/tasks
        list_resp = httpx.get(BASE_URL + "/api/tasks")
        assert list_resp.status_code == 200
        tasks = list_resp.json()
        texts = [t["text"] for t in tasks]
        assert "Integration test task" in texts
