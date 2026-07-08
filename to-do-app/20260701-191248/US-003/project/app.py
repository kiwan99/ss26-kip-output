from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = [{'id': 1, 'text': 'Sample Todo', 'done': False}]
done_todos = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_id = int(request.form['todo_id'])
        # Find the todo in active list
        for todo in todos:
            if todo['id'] == todo_id:
                # Move to done list
                done_todos.append(todo)
                todos.remove(todo)
                break
    return render_template('index.html', todos=todos, done_todos=done_todos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)