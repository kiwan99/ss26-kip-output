from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

todos = []

@app.route('/')
def index():
    active_todos = [t for t in todos if not t['done']]
    return render_template('index.html', active_todos=active_todos)

@app.route('/add', methods=['POST'])
def add_to_do():
    text = request.form['text']
    todos.append({'text': text, 'done': False})
    socketio.emit('item_added', {'text': text})
    return jsonify(success=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)