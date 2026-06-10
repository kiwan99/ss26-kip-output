from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    initial_values = {
        'number1': '',
        'number2': '',
        'result': ''
    }
    
    # Get current values from form or use defaults if not POSTed
    return render_template('index.html', 
                           number1=request.form.get('number1', ''),
                           number2=request.form.get('number2', ''),
                           result=get_result(request.form.get('number1'), request.form.get('number2')))


@app.route('/add', methods=['POST'])
def add_numbers():
    num1_str = request.form.get('number1')
    num2_str = request.form.get('number2')
    
    # Calculate and display result with current form data
    return render_template('index.html', 
                           number1=num1_str or '',
                           number2=num2_str or '',
                           result=get_result(num1_str, num2_str))


def get_result(n1=None, n2=None):
    """Calculate sum of two numbers if valid."""
    try:
        # Handle empty strings as None
        val1 = float(n1) if n1 else 0.0
        val2 = float(n2) if n2 else 0.0
        
        result = val1 + val2
        
        # Format output nicely (convert to int for whole numbers)
        if result == int(result):
            return str(int(result))
        return str(round(result, 4)).rstrip('0').rstrip('.')
    except Exception:
        return 'Error'


if __name__ == '__main__':
    app.run(debug=True)
