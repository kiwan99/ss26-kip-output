from flask import Flask, render_template, request, redirect, url_for
from models import db, ToDo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    active_todos = ToDo.query.filter_by(completed=False).all()
    done_todos = ToDo.query.filter_by(completed=True).all()
    return render_template('index.html', active_todos=active_todos, done_todos=done_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    text = request.form['text']
    new_todo = ToDo(text=text)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def mark_done(id):
    todo = ToDo.query.get(id)
    if todo:
        todo.completed = True
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)