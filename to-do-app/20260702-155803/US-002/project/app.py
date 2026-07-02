from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data storage
active_items = ["Buy groceries", "Walk the dog", "Finish report"]
done_items = []

@app.route("/active")
def active():
    return render_template('active.html', items=active_items, done_items=done_items)

@app.route("/done")
def done():
    return render_template('done.html', done_items=done_items)

@app.route("/mark_done/<int:item_index>")
def mark_done(item_index):
    global active_items, done_items
    if 0 <= item_index < len(active_items):
        done_items.append(active_items.pop(item_index))
    return redirect(url_for('active'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)