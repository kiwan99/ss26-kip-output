import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sum', methods=['GET'])
def sum_numbers():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = a + b
    return jsonify({'sum': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)