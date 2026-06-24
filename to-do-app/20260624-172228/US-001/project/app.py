from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

active_tasks = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        if task:
            active_tasks.append(task)
            return redirect(url_for('index'))
    return render_template('index.html', tasks=active_tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)