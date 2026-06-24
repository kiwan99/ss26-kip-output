from flask import Flask, render_template, request, redirect, url_for
from models import db, Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db.init_app(app)

# Create tables within app context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    active_items = Todo.query.filter_by(done=False).order_by(Todo.id).all()
    return render_template('index.html', items=active_items)

@app.route('/done')
def done():
    completed_items = Todo.query.filter_by(done=True).order_by(Todo.completion_time).all()
    return render_template('done.html', items=completed_items)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_item = Todo(content=content)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def mark_done(id):
    item = db.session.get(id)
    if item:
        item.done = True
        item.completion_time = db.func.current_timestamp()
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)