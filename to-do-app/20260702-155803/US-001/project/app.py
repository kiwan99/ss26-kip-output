from flask import Flask, request, render_template_string

app = Flask(__name__)

todo_list = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_todo = request.form.get("todo")
        if new_todo and new_todo.strip() != "":
            todo_list.append(new_todo)
    return render_template_string("""
    <html>
    <body>
        <h1>To-Do App</h1>
        <form method=\"POST\">
            <input type=\"text\" name=\"todo\" required>
            <input type=\"submit\" value=\"Add\">
        </form>
        <h2>Active Tasks:</h2>
        <ul>
            {% for item in todo_list %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """, todo_list=todo_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)