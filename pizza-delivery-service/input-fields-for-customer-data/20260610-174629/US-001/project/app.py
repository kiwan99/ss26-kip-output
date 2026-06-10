from flask import Flask, render_template, request, redirect, url_for, flash


@app.route('/')
def index():
    """Home page with ordering link."""
    return render_template('index.html', title='Pizza Delivery Service')


@app.route('/checkout', methods=['GET'])
def checkout_form():
    """Checkout form for customer contact information."""
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
