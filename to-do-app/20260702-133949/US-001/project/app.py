from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
tasks = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form["task"]
        tasks.append(task)
        return redirect(url_for("index"))
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)