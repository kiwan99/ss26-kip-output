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


def toggle_task(task_id):
    """Toggle the completed state of a task by its ID.

    Returns:
        dict with updated task data on success.
        None if no task with that ID exists.
    """
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return {
                "id": task["id"],
                "text": task["text"],
                "completed": task["completed"],
            }
    return None


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


@app.route("/toggle_task", methods=["POST"])
def handle_toggle_task():
    """Accept JSON body {"id": "<task-uuid>"} and toggle task completion.

    Returns:
        200 + updated task dict on success.
        404 + error message if task not found.
    """
    data = request.get_json(silent=True) or {}
    task_id = data.get("id", "")

    result = toggle_task(task_id)
    if result is None:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
