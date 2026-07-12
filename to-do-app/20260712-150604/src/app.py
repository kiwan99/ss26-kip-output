"""To-Do App — Flask backend for US-001 Add New Task."""

import uuid
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory task storage. Each task: {"id": str, "text": str, "completed": bool}
tasks = []


def add_task(text):
    """Create a new task from the given text.

    Returns:
        dict with keys id, text, completed on success.
        None if text is empty or whitespace-only.
    """
    stripped = text.strip() if isinstance(text, str) else ""
    if not stripped:
        return None
    task = {
        "id": str(uuid.uuid4()),
        "text": stripped,
        "completed": False,
    }
    tasks.append(task)
    return task


def get_tasks():
    """Return a copy of the current task list."""
    return list(tasks)


# ── Routes ──────────────────────────────────────────────

@app.route("/")
def index():
    """Render the main page with the current task list."""
    return render_template("index.html", tasks=get_tasks())


@app.route("/add_task", methods=["POST"])
def handle_add_task():
    """Accept JSON body {"text": "..."} and add a new task.

    Returns:
        201 + task dict on success.
        400 + error message if text is empty/missing.
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    result = add_task(text)
    if result is None:
        return jsonify({"error": "Task text cannot be empty."}), 400

    return jsonify(result), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
