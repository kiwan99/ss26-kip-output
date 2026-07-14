#!/usr/bin/env python3
"""
To-Do App — US-001: Add New Tasks

A simple single-page To-Do web app using only Python standard library.
Serves HTML/CSS/JS and manages tasks via HTTP endpoints.
"""

import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# In-memory task storage (list of dicts: {id, text, created_at})
tasks = []
next_id = 1


class TodoHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the To-Do App."""

    def log_message(self, format, *args):
        """Suppress default logging to keep output clean."""
        pass

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.serve_index()
        elif path == "/api/tasks":
            self.handle_get_tasks()
        elif path.startswith("/static/"):
            self.serve_static(path)
        else:
            self.send_error(404, "Not Found")

    # ------------------------------------------------------------------ POST
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/tasks":
            self.handle_add_task()
        else:
            self.send_error(404, "Not Found")

    # --------------------------------------------------------------- Helpers
    def serve_index(self):
        """Serve the main HTML page with server-rendered task list."""
        global tasks, next_id

        html = render_html(tasks)
        body = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_static(self, path):
        """Serve static files (CSS, JS) from the /project/src directory."""
        src_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(src_dir, path.lstrip("/"))

        # Resolve to absolute real path and verify it stays within src_dir
        real_path = os.path.realpath(file_path)
        if not real_path.startswith(src_dir):
            self.send_error(403, "Forbidden")
            return

        if not os.path.isfile(real_path):
            self.send_error(404, "Not Found")
            return

        # Determine MIME type
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".css": "text/css",
            ".js": "application/javascript",
            ".html": "text/html",
        }
        content_type = mime_map.get(ext, "application/octet-stream")

        with open(file_path, "rb") as f:
            body = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_add_task(self):
        """Handle POST /api/tasks to add a new task."""
        global tasks, next_id

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw = self.rfile.read(content_length)
            try:
                data = json.loads(raw.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_json_error(400, "Invalid JSON body.")
                return
        else:
            # No body — treat as empty text
            data = {"text": ""}

        text = data.get("text", "")

        # Validation: reject empty or whitespace-only input
        if not text or not text.strip():
            self.send_json_error(400, "Task text cannot be empty.")
            return

        task_text = text.strip()

        # Add task to in-memory store with creation timestamp
        new_task = {"id": next_id, "text": task_text, "created_at": time.time()}
        tasks.append(new_task)
        next_id += 1

        # Return success with the new task data
        self.send_json_response(201, {
            "status": "ok",
            "task": new_task,
        })

    def send_json_response(self, status_code, data):
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json_error(self, status_code, message):
        """Send a JSON error response."""
        self.send_json_response(status_code, {
            "status": "error",
            "message": message,
        })

    def handle_get_tasks(self):
        """Handle GET /api/tasks — return all tasks sorted by creation time."""
        global tasks
        sorted_tasks = sorted(tasks, key=lambda t: t.get("created_at", 0))
        self.send_json_response(200, {
            "status": "ok",
            "tasks": sorted_tasks,
        })


def render_html(tasks_list):
    """Generate the full HTML page with server-rendered task list."""

    # Sort tasks chronologically by creation time
    sorted_tasks = sorted(tasks_list, key=lambda t: t.get("created_at", 0))

    # Build server-rendered task list items
    task_items = ""
    if sorted_tasks:
        for t in sorted_tasks:
            escaped_text = escape_html(t["text"])
            created_at = t.get("created_at", 0)
            task_items += (
                f'<li class="task-item" data-task-id="{t["id"]}" '
                f'data-created-at="{created_at}">'
                f'{escaped_text}</li>\n'
            )
    else:
        task_items = '<p class="no-tasks">No tasks yet</p>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>To-Do App</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="app-container">
    <h1>To-Do List</h1>

    <!-- Add Task Form -->
    <form id="addTaskForm" autocomplete="off">
      <input type="text" id="taskInput" placeholder="Enter a new task..." aria-label="New task text">
      <button type="submit" id="addTaskBtn">Add Task</button>
    </form>

    <!-- Validation Message -->
    <p id="validationMsg" class="validation-error" role="alert"></p>

    <!-- Task List -->
    <ul id="taskList">
{task_items}    </ul>
  </div>

  <script src="/static/app.js"></script>
</body>
</html>"""
    return html


def escape_html(text):
    """Escape HTML special characters in task text."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
    )


def main():
    """Start the HTTP server."""
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))

    server = HTTPServer((host, port), TodoHandler)
    print(f"To-Do App running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    main()
