from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sum_result = None
    if request.method == 'POST':
        try:
            num1 = int(request.form['num1'])
            num2 = int(request.form['num2'])
            sum_result = num1 + num2
        except (KeyError, ValueError):
            pass  # Handle invalid input silently
    return render_template('index.html', sum=sum_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)