import os
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def render_html(num1="", num2="", operation="add", result=None, error=None):
    """Render the calculator page with current state embedded in HTML."""
    # Build result section
    if result is not None:
        result_display = str(result)
    elif error:
        result_display = error
    else:
        result_display = ""

    result_section = ""
    if result is not None or error:
        css_class = "error" if error else "success"
        label = "Error" if error else "Result"
        result_section = f"""
        <div class="result-area {css_class}">
            <label>{html.escape(label)}:</label>
            <span id="result-value">{html.escape(result_display)}</span>
        </div>
    """

    # Build operation options with selected state
    ops = ["add", "subtract", "multiply", "divide"]
    op_options = ""
    for op in ops:
        selected = 'selected' if op == html.escape(operation) else ''
        label_map = {
            "add": "Add (+)",
            "subtract": "Subtract (-)",
            "multiply": "Multiply (×)",
            "divide": "Divide (÷)"
        }
        op_options += f'<option value="{html.escape(op)}" {selected}>{label_map[op]}</option>\n'

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator App</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }}
        .calculator {{
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            padding: 32px;
            width: 100%;
            max-width: 480px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 24px;
            color: #2c3e50;
            font-size: 1.8rem;
        }}
        .form-group {{
            margin-bottom: 16px;
        }}
        label {{
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            color: #555;
            font-size: 0.95rem;
        }}
        input[type="number"], select {{
            width: 100%;
            padding: 12px 14px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }}
        input[type="number"]:focus, select:focus {{
            outline: none;
            border-color: #3498db;
        }}
        .btn-calculate {{
            width: 100%;
            padding: 14px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 8px;
        }}
        .btn-calculate:hover {{
            background-color: #2980b9;
        }}
        .result-area {{
            margin-top: 24px;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
        }}
        .result-area.success {{
            background-color: #d5f4e6;
            border: 2px solid #27ae60;
            color: #1e7c43;
        }}
        .result-area.error {{
            background-color: #fde8e8;
            border: 2px solid #e74c3c;
            color: #c0392b;
        }}
        .result-area label {{
            font-size: 1rem;
            margin-bottom: 4px;
        }}
        .result-area span {{
            display: block;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 4px;
        }}
        @media (max-width: 600px) {{
            .calculator {{
                padding: 20px;
            }}
            h1 {{
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>
        <form method="post" action="/">
            <div class="form-group">
                <label for="num1">Number 1:</label>
                <input type="number" id="num1" name="num1" step="any" value="{html.escape(num1)}">
            </div>
            <div class="form-group">
                <label for="num2">Number 2:</label>
                <input type="number" id="num2" name="num2" step="any" value="{html.escape(num2)}">
            </div>
            <div class="form-group">
                <label for="operation">Operation:</label>
                <select id="operation" name="operation">
                    {op_options}                </select>
            </div>
            <button type="submit" class="btn-calculate">Calculate</button>
        </form>
{result_section}    </div>
</body>
</html>"""
    return page_html


def calculate(num1, num2, operation):
    """Perform the calculation based on the selected operation."""
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return None, "Error: Division by zero is not allowed."
        return num1 / num2
    else:
        return None, "Error: Invalid operation selected."


class CalculatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the calculator app."""

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            page_html = render_html(num1="", num2="", operation="add", result=None, error=None)
            self.wfile.write(page_html.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(body)

            # Extract form values
            num1_str = params.get("num1", [""])[0]
            num2_str = params.get("num2", [""])[0]
            operation = params.get("operation", ["add"])[0]

            result = None
            error = None

            # Validate inputs are not empty
            if not num1_str or not num2_str:
                error = "Error: Both number fields must be filled in."
            else:
                try:
                    num1 = float(num1_str)
                    num2 = float(num2_str)
                except (ValueError, TypeError):
                    error = "Error: Please enter valid numbers."

                if not error:
                    calc_result = calculate(num1, num2, operation)
                    if isinstance(calc_result, tuple):
                        result, error = calc_result
                    else:
                        result = calc_result

            html = render_html(
                num1=num1_str,
                num2=num2_str,
                operation=operation,
                result=result,
                error=error
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    def log_message(self, format, *args):
        """Suppress default request logging for cleaner output."""
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), CalculatorHandler)
    print(f"Calculator app running on http://0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()


if __name__ == "__main__":
    main()
