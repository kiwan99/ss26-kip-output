from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

active_items = []

@app.route("/", methods=["GET", "POST"])
def index():
    global active_items
    if request.method == "POST":
        item = request.form.get("todo_item")
        if item:
            active_items.append(item)
            return render_template("index.html", active_items=active_items)  # Render template instead of redirecting
    return render_template("index.html", active_items=active_items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)