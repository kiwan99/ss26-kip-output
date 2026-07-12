#!/usr/bin/env python3
"""Quick smoke test for the To-Do App."""
import urllib.request
import json

BASE = "http://localhost:8000"

# Test 1: GET / returns HTML with input, button, task list
resp = urllib.request.urlopen(BASE + "/")
html = resp.read().decode("utf-8")
assert "<input" in html, "Missing input field"
assert "Add Task" in html, "Missing Add Task button"
assert 'id="taskList"' in html, "Missing task list container"
print("[PASS] GET / — HTML contains input, button, and task list")

# Test 2: POST empty text returns error
req = urllib.request.Request(
    BASE + "/api/tasks",
    data=json.dumps({"text": ""}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
try:
    resp = urllib.request.urlopen(req)
    print("[FAIL] POST empty text should return error")
except urllib.error.HTTPError as e:
    body = json.loads(e.read().decode("utf-8"))
    assert e.code == 400, f"Expected 400, got {e.code}"
    assert "error" in body.get("status", ""), "Missing error status"
    print(f"[PASS] POST empty text returns 400: {body['message']}")

# Test 3: POST whitespace-only text returns error
req = urllib.request.Request(
    BASE + "/api/tasks",
    data=json.dumps({"text": "   "}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
try:
    resp = urllib.request.urlopen(req)
    print("[FAIL] POST whitespace text should return error")
except urllib.error.HTTPError as e:
    body = json.loads(e.read().decode("utf-8"))
    assert e.code == 400, f"Expected 400, got {e.code}"
    print(f"[PASS] POST whitespace text returns 400: {body['message']}")

# Test 4: POST valid task succeeds and adds to list
req = urllib.request.Request(
    BASE + "/api/tasks",
    data=json.dumps({"text": "Buy groceries"}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
resp = urllib.request.urlopen(req)
assert resp.status == 201, f"Expected 201, got {resp.status}"
body = json.loads(resp.read().decode("utf-8"))
assert body["status"] == "ok", "Missing ok status"
assert body["task"]["text"] == "Buy groceries", "Task text mismatch"
print(f"[PASS] POST valid task returns 201: {body['task']}")

# Test 5: GET / now shows the added task server-rendered
resp = urllib.request.urlopen(BASE + "/")
html = resp.read().decode("utf-8")
assert "Buy groceries" in html, "Added task not visible in HTML"
print("[PASS] GET / — Added task 'Buy groceries' appears in rendered HTML")

# Test 6: Add second task and verify both appear
req = urllib.request.Request(
    BASE + "/api/tasks",
    data=json.dumps({"text": "Walk the dog"}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
resp = urllib.request.urlopen(req)
body = json.loads(resp.read().decode("utf-8"))
print(f"[PASS] POST second task: {body['task']}")

resp = urllib.request.urlopen(BASE + "/")
html = resp.read().decode("utf-8")
assert "Buy groceries" in html, "First task missing after adding second"
assert "Walk the dog" in html, "Second task not visible in HTML"
print("[PASS] GET / — Both tasks appear server-rendered")

# Test 7: Static files load correctly
resp = urllib.request.urlopen(BASE + "/static/style.css")
css = resp.read().decode("utf-8")
assert len(css) > 10, "CSS file too short"
print(f"[PASS] GET /static/style.css — {len(css)} bytes")

resp = urllib.request.urlopen(BASE + "/static/app.js")
js = resp.read().decode("utf-8")
assert "addTask" in js, "Missing addTask function in JS"
assert "validateInput" in js, "Missing validateInput function in JS"
print(f"[PASS] GET /static/app.js — {len(js)} bytes, contains key functions")

print("\n=== ALL SMOKE TESTS PASSED ===")
