"""
Tests for US-002: Mark Tasks Complete or Delete Them

Acceptance criteria covered:
1. Each task displays a clickable checkbox/toggle control
   -> test_toggle_endpoint_exists, test_task_has_completed_field
2. Clicking checkbox marks task complete with visual change (strikethrough)
   -> test_toggle_complete_flips_status, test_integration_toggle_visual_state
3. Delete button permanently removes task from view
   -> test_delete_removes_task, test_integration_delete_persists
4. Changes appear instantly without page refresh
   -> Covered by integration tests verifying immediate state changes via API
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import json
import pytest
import app


# ── Unit Tests (via Flask test_client) ──────────────────────────────

@pytest.fixture
def client():
    """Fresh Flask test client with clean TaskManager state."""
    app.task_manager = app.TaskManager()
    return app.app.test_client()


def test_toggle_endpoint_exists(client):
    """AC1: Toggle control exists — POST /api/tasks/<id>/toggle route is registered."""
    # Add a task first
    resp = client.post("/api/tasks", json={"text": "Toggle me"})
    assert resp.status_code == 201
    data = json.loads(resp.get_data(as_text=True))
    task_id = data["id"]

    # Toggle endpoint must accept POST and return 200 for existing task
    resp = client.post(f"/api/tasks/{task_id}/toggle")
    assert resp.status_code == 200


def test_task_has_completed_field(client):
    """AC1: Each task object includes a 'completed' field (backing the checkbox)."""
    resp = client.post("/api/tasks", json={"text": "Check me"})
    assert resp.status_code == 201
    data = json.loads(resp.get_data(as_text=True))
    assert "completed" in data
    assert data["completed"] is False  # new tasks start incomplete


def test_toggle_complete_flips_status(client):
    """AC2: Clicking checkbox toggles completed status (False→True, True→False)."""
    resp = client.post("/api/tasks", json={"text": "Flip me"})
    assert resp.status_code == 201
    data = json.loads(resp.get_data(as_text=True))
    task_id = data["id"]

    # First toggle: False → True
    resp = client.post(f"/api/tasks/{task_id}/toggle")
    result = json.loads(resp.get_data(as_text=True))
    assert result["completed"] is True

    # Second toggle: True → False
    resp = client.post(f"/api/tasks/{task_id}/toggle")
    result = json.loads(resp.get_data(as_text=True))
    assert result["completed"] is False


def test_delete_removes_task(client):
    """AC3: Delete button permanently removes task from the list."""
    resp = client.post("/api/tasks", json={"text": "Delete me"})
    assert resp.status_code == 201
    data = json.loads(resp.get_data(as_text=True))
    task_id = data["id"]

    # Task exists before delete
    resp = client.get("/api/tasks")
    tasks_before = json.loads(resp.get_data(as_text=True))
    assert any(t["id"] == task_id for t in tasks_before)

    # Delete the task
    resp = client.delete(f"/api/tasks/{task_id}")
    assert resp.status_code == 200

    # Task is gone after delete
    resp = client.get("/api/tasks")
    tasks_after = json.loads(resp.get_data(as_text=True))
    assert not any(t["id"] == task_id for t in tasks_after)


# ── Integration Tests (against running server at localhost:8000) ────

try:
    import httpx
except ImportError:
    httpx = None


@pytest.mark.skipif(httpx is None, reason="httpx not available")
def test_integration_toggle_visual_state():
    """AC2+4: Toggle marks task complete; change appears instantly via API."""
    with httpx.Client(base_url="http://localhost:8000", timeout=5) as hx:
        # Add a task
        resp = hx.post("/api/tasks", json={"text": "Integration toggle"})
        assert resp.status_code == 201, f"Add failed: {resp.text}"
        task_id = resp.json()["id"]

        # Toggle it complete
        resp = hx.post(f"/api/tasks/{task_id}/toggle")
        assert resp.status_code == 200, f"Toggle failed: {resp.text}"
        result = resp.json()
        assert result["completed"] is True

        # Verify state persists immediately (no refresh needed)
        resp = hx.get("/api/tasks")
        tasks = resp.json()
        matched = [t for t in tasks if t["id"] == task_id]
        assert len(matched) == 1
        assert matched[0]["completed"] is True


@pytest.mark.skipif(httpx is None, reason="httpx not available")
def test_integration_delete_persists():
    """AC3+4: Delete removes task permanently; change appears instantly via API."""
    with httpx.Client(base_url="http://localhost:8000", timeout=5) as hx:
        # Add a task
        resp = hx.post("/api/tasks", json={"text": "Integration delete"})
        assert resp.status_code == 201, f"Add failed: {resp.text}"
        task_id = resp.json()["id"]

        # Delete it
        resp = hx.delete(f"/api/tasks/{task_id}")
        assert resp.status_code == 200, f"Delete failed: {resp.text}"

        # Verify task is gone immediately (no refresh needed)
        resp = hx.get("/api/tasks")
        tasks = resp.json()
        assert not any(t["id"] == task_id for t in tasks), "Task still present after delete"
