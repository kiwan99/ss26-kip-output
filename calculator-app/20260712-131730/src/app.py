"""Calculator App — Flask-based single-page calculator."""

from flask import Flask, render_template, request

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Core calculation logic (separate from routes for easy unit testing)
# ---------------------------------------------------------------------------

def calculate(num1: float, num2: float, operation: str):
    """Perform a basic arithmetic operation.

    Args:
        num1: First operand.
        num2: Second operand.
        operation: One of 'add', 'subtract', 'multiply', 'divide'.

    Returns:
        A tuple (result, error) where exactly one is non-None.
        - On success: (computed_value, None)
        - On failure: (None, error_message)
    """
    if operation == "add":
        return num1 + num2, None
    elif operation == "subtract":
        return num1 - num2, None
    elif operation == "multiply":
        return num1 * num2, None
    elif operation == "divide":
        if num2 == 0:
            return None, "Error: Division by zero is not allowed."
        return num1 / num2, None
    else:
        return None, f"Error: Unknown operation '{operation}'."


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    num1 = None
    num2 = None
    operation = None

    if request.method == "POST":
        # Parse form fields
        raw_num1 = request.form.get("num1", "").strip()
        raw_num2 = request.form.get("num2", "").strip()
        operation = request.form.get("operation", "").strip()

        try:
            num1 = float(raw_num1) if raw_num1 else None
            num2 = float(raw_num2) if raw_num2 else None
        except (ValueError, TypeError):
            error = "Error: Please enter valid numbers."
            num1 = raw_num1 or None
            num2 = raw_num2 or None

        # Compute result only when both numbers are valid and operation is set
        if num1 is not None and num2 is not None and operation:
            result, error = calculate(num1, num2, operation)

    return render_template(
        "index.html",
        result=result,
        error=error,
        num1=num1,
        num2=num2,
        operation=operation,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
