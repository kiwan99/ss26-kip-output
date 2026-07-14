import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


def render_page(num1="", num2="", operation="add", result=None, error=None):
    add_selected = " selected" if operation == "add" else ""
    subtract_selected = " selected" if operation == "subtract" else ""
    multiply_selected = " selected" if operation == "multiply" else ""
    divide_selected = " selected" if operation == "divide" else ""

    result_html = ""
    if error:
        result_html = f"""            <div class="result-area error">
                <div class="result-label">Error</div>
                <div class="result-value">{error}</div>
            </div>"""
    elif result is not None:
        if isinstance(result, float) and result == int(result):
            result_str = str(int(result))
        else:
            result_str = f"{result:.6f}".rstrip("0").rstrip(".")
        result_html = f"""            <div class="result-area">
                <div class="result-label">Result</div>
                <div class="result-value">{result_str}</div>
            </div>"""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .calculator {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            padding: 32px;
            width: 100%;
            max-width: 480px;
        }
        h1 {
            text-align: center;
            margin-bottom: 24px;
            font-size: 1.5rem;
            color: #2c3e50;
        }
        .form-group {
            margin-bottom: 16px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            color: #555;
        }
        input[type="number"], select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #dcdfe6;
            border-radius: 6px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }
        input[type="number"]:focus, select:focus {
            outline: none;
            border-color: #409eff;
        }
        button[type="submit"] {
            width: 100%;
            padding: 12px;
            background-color: #409eff;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 8px;
        }
        button[type="submit"]:hover {
            background-color: #3a8ee6;
        }
        .result-area {
            margin-top: 20px;
            padding: 16px;
            background-color: #ecf5ff;
            border: 1px solid #d9ecff;
            border-radius: 6px;
            text-align: center;
        }
        .result-area.error {
            background-color: #fef0f0;
            border-color: #fbc4c4;
            color: #f56c6c;
        }
        .result-label {
            font-weight: 600;
            margin-bottom: 4px;
            font-size: 0.85rem;
            color: #909399;
        }
        .result-value {
            font-size: 1.25rem;
            font-weight: 700;
            color: #303133;
        }
        @media (max-width: 600px) {
            .calculator {
                padding: 24px;
            }
            h1 {
                font-size: 1.25rem;
            }
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>
        <form method="post" action="/">
            <div class="form-group">
                <label for="num1">Number 1</label>
                <input type="number" id="num1" name="num1" step="any" value="__NUM1__">
            </div>
            <div class="form-group">
                <label for="num2">Number 2</label>
                <input type="number" id="num2" name="num2" step="any" value="__NUM2__">
            </div>
            <div class="form-group">
                <label for="operation">Operation</label>
                <select id="operation" name="operation">
                    <option value="add"__ADD_SELECTED__>Add</option>
                    <option value="subtract"__SUBTRACT_SELECTED__>Subtract</option>
                    <option value="multiply"__MULTIPLY_SELECTED__>Multiply</option>
                    <option value="divide"__DIVIDE_SELECTED__>Divide</option>
                </select>
            </div>
            <button type="submit">Calculate</button>
        </form>
__RESULT_HTML__
    </div>
</body>
</html>"""

    html = html.replace("__NUM1__", str(num1))
    html = html.replace("__NUM2__", str(num2))
    html = html.replace("__ADD_SELECTED__", add_selected)
    html = html.replace("__SUBTRACT_SELECTED__", subtract_selected)
    html = html.replace("__MULTIPLY_SELECTED__", multiply_selected)
    html = html.replace("__DIVIDE_SELECTED__", divide_selected)
    html = html.replace("__RESULT_HTML__", result_html)

    return html


class CalculatorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html = render_page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body>Not Found</body></html>")

    def do_POST(self):
        if self.path == "/" or self.path == "/index.html":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            parsed = parse_qs(post_data.decode("utf-8"))

            num1_str = parsed.get("num1", [""])[0]
            num2_str = parsed.get("num2", [""])[0]
            operation = parsed.get("operation", ["add"])[0]

            result = None
            error = None

            try:
                if not num1_str or not num2_str:
                    raise ValueError("Empty input")
                num1 = float(num1_str)
                num2 = float(num2_str)
            except (ValueError, TypeError):
                error = "Please enter valid numbers for both fields."

            if not error:
                try:
                    if operation == "add":
                        result = num1 + num2
                    elif operation == "subtract":
                        result = num1 - num2
                    elif operation == "multiply":
                        result = num1 * num2
                    elif operation == "divide":
                        if num2 == 0:
                            error = "Cannot divide by zero."
                        else:
                            result = num1 / num2
                    else:
                        error = "Unknown operation selected."
                except Exception as e:
                    error = f"Calculation error: {e}"

            html = render_page(
                num1=num1_str,
                num2=num2_str,
                operation=operation,
                result=result,
                error=error,
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body>Not Found</body></html>")

    def log_message(self, format, *args):
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), CalculatorHandler)
    print(f"Calculator app running on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
