from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    """Home page with number input form"""
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_numbers():
    """Calculate the sum of two numbers"""
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('num1', 0))
            num2 = float(request.form.get('num2', 0))
            result = round(num1 + num2, 2)
            
            return jsonify({
                'success': True,
                'result': result,
                'display_result': f"{int(num1)}+{int(num2)}={int(result)}" if result == int(result) else f"{num1}+{num2}={result}"
            })
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Please enter valid numbers'
            }), 400
    
    # GET request - show form with empty values
    return render_template('index.html', num1=0.0, num2=0.0)


@app.route('/api/add/<num1>/<num2>')
def api_add(num1=float(num1), num2=float(num2)):
    """API endpoint for adding two numbers"""
    result = round((float(num1)) + (float(num2)), 2)
    
    return jsonify({
        'result': result,
        'formula': f"{num1} + {num2}"
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
