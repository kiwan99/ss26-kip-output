from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for To-Do items
todos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_todo():
    data = request.json
    todo = data.get('text')
    if todo:
        todos.append(todo)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)