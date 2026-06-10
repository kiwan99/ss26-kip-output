#!/usr/bin/env python3
"""Number Adder Flask Application - User Story US-001."""

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    """Main route renders the number adder page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
