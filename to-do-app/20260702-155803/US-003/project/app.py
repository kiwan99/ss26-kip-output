from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
]

@app.route("/")
def index():
    active_tasks = [task for task in tasks if not task["completed"]]
    done_tasks = [task for task in tasks if task["completed"]]
    return render_template("index.html", active_tasks=active_tasks, done_tasks=done_tasks)

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)