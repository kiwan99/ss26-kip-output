from flask import Flask, request


app = Flask(__name__)
app.secret_key = 'pizza-delivery-secret'  # For sessions during checkout


@app.route('/')
def index():
    return '<h1>Pizza Delivery Service - Checkout Feature (US-001)</h1><p>Contact info for delivery communication.</p>'


@app.route('/checkout')
def checkout_page():
    """Checkout page with mandatory first name and phone number entry"""
