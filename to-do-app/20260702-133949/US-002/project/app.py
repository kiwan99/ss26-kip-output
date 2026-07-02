from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
tasks = [
    {'id': 1, 'description': 'Task 1', 'done': False},
    {'id': 2, 'description': 'Task 2', 'done': True},
    {'id': 3, 'description': 'Task 3', 'done': False},
]

@app.route('/')
def index():
    active_tasks = [task for task in tasks if not task['done']]
    return render_template('index.html', tasks=active_tasks)

@app.route('/done/<int:task_id>', methods=['POST'])
def mark_done(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)