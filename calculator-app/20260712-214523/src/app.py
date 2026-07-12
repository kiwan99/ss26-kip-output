import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


def calculate(num1, num2, operation):
    """Perform basic arithmetic based on the selected operation."""
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return None
        return num1 / num2
    else:
        return None


def validate_inputs(num1_str, num2_str):
    """Validate form inputs and return a list of error messages."""
    errors = []

    # Check for empty fields (Criterion 2)
    if not num1_str or num1_str.strip() == "":
        errors.append("Please enter a value for the first number.")
    if not num2_str or num2_str.strip() == "":
        errors.append("Please enter a value for the second number.")

    # Check for non-numeric characters (Criterion 1)
    if num1_str and num1_str.strip():
        try:
            float(num1_str)
        except ValueError:
            errors.append(f"'{num1_str}' is not a valid number.")

    if num2_str and num2_str.strip():
        try:
            float(num2_str)
        except ValueError:
            errors.append(f"'{num2_str}' is not a valid number.")

    return errors


def escape_html(text):
    """Escape special HTML characters."""
    s = str(text)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s


def format_number(value):
    """Format a number for display, removing unnecessary .0 suffix."""
    if value is None:
        return ""
    f = float(value)
    if f == int(f):
        return str(int(f))
    return str(f)


def render_page(num1=None, num2=None, operation="add", result=None, error=None):
    """Generate the calculator HTML page."""

    num1_val = escape_html(format_number(num1)) if num1 is not None else ""
    num2_val = escape_html(format_number(num2)) if num2 is not None else ""

    # Build operation options with selected state
    ops = ["add", "subtract", "multiply", "divide"]
    op_labels = {"add": "Add", "subtract": "Subtract", "multiply": "Multiply", "divide": "Divide"}
    options_html = ""
    for op in ops:
        sel = ' selected' if operation == op else ''
        options_html += f'<option value="{escape_html(op)}"{sel}>{op_labels[op]}</option>\n'

    # Build result section (only show if no error)
    result_html = ""
    if error is None and result is not None:
        result_display = escape_html(format_number(result))
        result_html = f'''<div class="result-area">
            <div class="result-label">Result</div>
            <div class="result-value">{result_display}</div>
        </div>'''

    # Build error section
    error_html = ""
    if error is not None:
        escaped_error = escape_html(error)
        error_lines = escaped_error.split("\n")
        messages_html = ""
        for line in error_lines:
            stripped = line.strip()
            if stripped:
                messages_html += f'<div class="error-message">{stripped}</div>\n'
        error_html = f'''<div class="error-area">
            <div class="error-label">Error</div>
{messages_html}        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .calculator {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 1.5rem;
            color: #2c3e50;
        }}

        .form-group {{
            margin-bottom: 1rem;
        }}

        label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #555;
        }}

        input[type="number"], select {{
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }}

        input[type="number"]:focus, select:focus {{
            outline: none;
            border-color: #3498db;
        }}

        button[type="submit"] {{
            width: 100%;
            padding: 0.75rem;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }}

        button[type="submit"]:hover {{
            background-color: #2980b9;
        }}

        .result-area {{
            margin-top: 1.5rem;
            padding: 1rem;
            background-color: #e8f6f3;
            border-radius: 4px;
            text-align: center;
        }}

        .result-label {{
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }}

        .result-value {{
            font-size: 1.5rem;
            color: #27ae60;
            font-weight: bold;
        }}

        .error-area {{
            margin-top: 1.5rem;
            padding: 1rem;
            background-color: #fdedec;
            border: 1px solid #e74c3c;
            border-radius: 4px;
            text-align: center;
        }}

        .error-label {{
            font-weight: 600;
            color: #c0392b;
            margin-bottom: 0.5rem;
        }}

        .error-message {{
            font-size: 1rem;
            color: #e74c3c;
            font-weight: bold;
        }}

        @media (max-width: 480px) {{
            .calculator {{
                margin: 1rem;
                padding: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>

        <form method="POST" action="/">
            <div class="form-group">
                <label for="num1">First Number</label>
                <input type="number" id="num1" name="num1" step="any" value="{num1_val}">
            </div>

            <div class="form-group">
                <label for="operation">Operation</label>
                <select id="operation" name="operation">
{options_html}                </select>
            </div>

            <div class="form-group">
                <label for="num2">Second Number</label>
                <input type="number" id="num2" name="num2" step="any" value="{num2_val}">
            </div>

            <button type="submit" name="calculate">Calculate</button>
        </form>

{result_html}{error_html}    </div>
</body>
</html>'''
    return html


class CalculatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the calculator app."""

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = render_page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    def do_POST(self):
        if self.path == "/" or self.path == "/index.html":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")

            # Parse form data (application/x-www-form-urlencoded)
            from urllib.parse import parse_qs
            params = {}
            if post_data:
                parsed = parse_qs(post_data)
                for key, values in parsed.items():
                    params[key] = values[0] if values else ""

            num1_str = params.get("num1", "")
            num2_str = params.get("num2", "")
            operation = params.get("operation", "add")

            # Validate inputs before attempting calculation (Criteria 1 & 2)
            validation_errors = validate_inputs(num1_str, num2_str)

            if validation_errors:
                # Input validation failed — show errors, skip calculation
                error_message = "\n".join(validation_errors)
                body = render_page(num1=None, num2=None, operation=operation, result=None, error=error_message)
            else:
                # Inputs are valid — convert to float and calculate
                num1 = float(num1_str) if num1_str.strip() else None
                num2 = float(num2_str) if num2_str.strip() else None

                result = None
                error = None

                if num1 is not None and num2 is not None:
                    result = calculate(num1, num2, operation)

                    # Check for division by zero (Criterion 3)
                    if operation == "divide" and result is None:
                        error = "Cannot divide by zero."
                        result = None

                body = render_page(num1=num1, num2=num2, operation=operation, result=result, error=error)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    def log_message(self, format, *args):
        """Suppress default request logging to keep output clean."""
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), CalculatorHandler)
    print(f"Calculator app running on http://0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
