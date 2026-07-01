from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<ToDoItem {self.title}>'

@app.route('/add', methods=['POST'])
def add_todo():
    data = request.json
    new_item = ToDoItem(title=data['title'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Todo added'}), 201

@app.route('/done/<int:item_id>', methods=['PUT'])
def mark_done(item_id):
    item = ToDoItem.query.get_or_404(item_id)
    item.done = True
    db.session.commit()
    return jsonify({'message': 'Marked as done'}), 200

@app.route('/active', methods=['GET'])
def get_active():
    active_items = ToDoItem.query.filter_by(done=False).all()
    return jsonify([{'id': i.id, 'title': i.title, 'date': i.date} for i in active_items])

@app.route('/done_list', methods=['GET'])
def get_done():
    done_items = ToDoItem.query.filter_by(done=True).all()
    return jsonify([{'id': i.id, 'title': i.title, 'date': i.date} for i in done_items])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000)