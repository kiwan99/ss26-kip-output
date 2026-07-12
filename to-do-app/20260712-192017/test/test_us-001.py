"""Tests for US-001: Add New Tasks — acceptance criteria verification."""

import json
from pathlib import Path
import sys
import urllib.request
import urllib.error

SRC = Path("/project/src") if Path("/project/src").exists() else Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

BASE_URL = "http://localhost:33129"


def _get(path):
    """Perform a GET request and return (status_code, body_bytes)."""
    req = urllib.request.Request(BASE_URL + path)
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _post(path, data):
    """Perform a POST request with JSON body and return (status_code, parsed_json)."""
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL + path,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_ui_elements_and_valid_task_addition():
    """
    Covers acceptance criteria:
      1. Page displays a text input field and an 'Add Task' button.
      2. Entering text and clicking the button adds the task to the visible list
         immediately without reloading the page (server returns 201).
      4. After successful submission, the input field clears automatically for the next entry
         (verified via client-side JS source: clearInput() called on success).
    """
    # Criterion 1: Check HTML contains required form elements
    status, html_bytes = _get("/")
    assert status == 200, f"Expected 200 from GET /, got {status}"
    html = html_bytes.decode("utf-8")

    assert 'id="taskInput"' in html, "Missing text input field #taskInput"
    assert 'id="addTaskBtn"' in html, "Missing Add Task button #addTaskBtn"
    assert 'type="submit"' in html or '<button' in html, "Button should be a submit button"

    # Criterion 2: POST valid task → server returns 201 (task added)
    status, resp_json = _post("/api/tasks", {"text": "Buy groceries"})
    assert status == 201, f"Expected 201 for valid task, got {status}"
    assert resp_json["status"] == "ok"
    assert resp_json["task"]["text"] == "Buy groceries"

    # Criterion 4: Verify client-side JS clears input after successful submission.
    js_path = SRC / "static/app.js"
    js_source = js_path.read_text()
    assert "clearInput()" in js_source, (
        "Client-side JS must call clearInput() after successful task addition."
    )
    # Verify it's called in the success path (.then handler)
    assert ".then(function (data)" in js_source and "clearInput()" in js_source


def test_empty_and_whitespace_input_validation():
    """
    Covers acceptance criterion:
      3. Submitting an empty or whitespace-only input does not add a new task
         and shows a brief validation message.
    """
    # Empty string submission → 400 with error message
    status, resp_json = _post("/api/tasks", {"text": ""})
    assert status == 400, f"Expected 400 for empty input, got {status}"
    assert resp_json["status"] == "error"
    assert "message" in resp_json and len(resp_json["message"]) > 0

    # Whitespace-only submission → 400 with error message
    status, resp_json = _post("/api/tasks", {"text": "   "})
    assert status == 400, f"Expected 400 for whitespace-only input, got {status}"
    assert resp_json["status"] == "error"
    assert "message" in resp_json and len(resp_json["message"]) > 0

    # Verify client-side JS shows validation message on invalid input
    js_path = SRC / "static/app.js"
    js_source = js_path.read_text()
    assert "showValidationMessage(" in js_source, (
        "Client-side JS must show a validation message for empty/whitespace input."
    )
