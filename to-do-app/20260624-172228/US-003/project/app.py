from flask import Flask, render_template, request, redirect, url_for
from models import db, Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    active = Todo.query.filter_by(is_done=False).all()
    done = Todo.query.filter_by(is_done=True).all()
    return render_template('index.html', active=active, done=done)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    if title:
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:id>', methods=['POST'])
def mark_done(id):
    todo = Todo.query.get(id)
    if todo:
        todo.is_done = True
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)