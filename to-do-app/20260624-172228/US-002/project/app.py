from flask import Flask, render_template, request, redirect, url_for
from tasks import Tasks

app = Flask(__name__)
tasks = Tasks()

@app.route('/')
def index():
    return redirect(url_for('active'))

@app.route('/active')
def active():
    active_tasks = [task for task in tasks.get_all() if not task.done]
    return render_template('active.html', tasks=active_tasks)

@app.route('/mark_done/<int:task_id>', methods=['POST'])
def mark_done(task_id):
    tasks.mark_done(task_id)
    return redirect(url_for('active'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)