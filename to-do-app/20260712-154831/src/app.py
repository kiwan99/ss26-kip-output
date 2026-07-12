"""
To-Do App - Flask entrypoint.

Run with: python src/app.py
Starts the app on host 0.0.0.0 and port 8000.
"""

from flask import Flask, render_template, request, jsonify

from task_manager import TaskManager

app = Flask(__name__)

# Shared task manager instance (in-memory storage)
task_manager = TaskManager()


@app.route("/")
def index():
    """Serve the main to-do page."""
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as JSON."""
    return jsonify(task_manager.get_tasks())


@app.route("/api/tasks", methods=["POST"])
def add_task():
    """Add a new task from JSON body {text: '...'}. Returns created task or error."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    task = task_manager.add_task(data["text"])
    if task is None:
        return jsonify({"error": "Task text cannot be empty"}), 400

    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    if task_manager.delete_task(task_id):
        return jsonify({"success": True})
    return jsonify({"error": "Task not found"}), 404


@app.route("/api/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_complete(task_id):
    """Toggle the completed status of a task."""
    if task_manager.toggle_complete(task_id):
        task = task_manager.get_task(task_id)
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
