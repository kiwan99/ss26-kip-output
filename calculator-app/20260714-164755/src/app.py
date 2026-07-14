import html
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# ---------------------------------------------------------------------------
# HTML template – server-rendered with current state
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calculator</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #f4f6f8;
      color: #222;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 1rem;
    }}

    .calculator {{
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.1);
      padding: 2rem;
      width: 100%;
      max-width: 420px;
    }}

    h1 {{ text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem; }}

    .input-group {{ margin-bottom: 1rem; }}
    .input-group label {{ display: block; margin-bottom: .35rem; font-weight: 600; font-size: .9rem; }}
    .input-group input {{
      width: 100%;
      padding: .6rem .75rem;
      border: 2px solid #d0d5dd;
      border-radius: 8px;
      font-size: 1rem;
      transition: border-color .2s;
    }}
    .input-group input:focus {{ outline: none; border-color: #4a90d9; }}

    .buttons {{ display: flex; gap: .75rem; justify-content: center; margin: 1.25rem 0; flex-wrap: wrap; }}
    .btn {{
      padding: .65rem 1.6rem;
      border: none;
      border-radius: 8px;
      font-size: 1.1rem;
      cursor: pointer;
      color: #fff;
      transition: opacity .2s, transform .1s;
    }}
    .btn:hover {{ opacity: .85; }}
    .btn:active {{ transform: scale(.97); }}

    .btn-plus  {{ background: #4a90d9; }}
    .btn-minus {{ background: #e67e22; }}

    .result-box {{
      text-align: center;
      padding: 1rem;
      border-radius: 8px;
      font-size: 1.15rem;
      min-height: 3.5rem;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .result-success {{ background: #eaf6ec; color: #27ae60; border: 1px solid #27ae60; }}
    .result-error   {{ background: #fdecea; color: #c0392b; border: 1px solid #c0392b; }}

    @media (max-width: 480px) {{
      .calculator {{ padding: 1.25rem; }}
      .btn {{ padding: .55rem 1rem; font-size: 1rem; }}
    }}
  </style>
</head>
<body>
  <div class="calculator">
    <h1>Calculator</h1>

    <form id="calc-form" method="post" action="/">
      <div class="input-group">
        <label for="num1">Number 1</label>
        <input type="text" id="num1" name="num1"{num1_val} placeholder="Enter first number">
      </div>

      <div class="input-group">
        <label for="num2">Number 2</label>
        <input type="text" id="num2" name="num2"{num2_val} placeholder="Enter second number">
      </div>

      <div class="buttons">
        <button type="submit" name="op" value="+" class="btn btn-plus">+</button>
        <button type="submit" name="op" value="-" class="btn btn-minus">&minus;</button>
      </div>
    </form>

{result_html}

  </div>

  <script>
    // Lightweight enhancement: after a POST the page reloads with server-rendered state.
    // This script only adds visual polish; it does not affect acceptance criteria.
    document.addEventListener('DOMContentLoaded', function () {{
      var form = document.getElementById('calc-form');
      if (form) {{
        form.addEventListener('submit', function (e) {{
          // Let the default POST submit happen – server renders the result.
        }});
      }}
    }});
  </script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Application state (in-memory, single-user for this local app)
# ---------------------------------------------------------------------------

app_state = {
    "num1": "",
    "num2": "",
    "result_text": "",
    "result_type": "",   # "" | "success" | "error"
}


def parse_number(value):
    """Return a float if *value* is numeric, otherwise None."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def compute(op, n1, n2):
    """Perform the requested operation and return (result_string, type_tag)."""

    # Validate inputs are numeric
    a = parse_number(n1)
    b = parse_number(n2)

    if a is None or b is None:
        bad_inputs = []
        label_a = "Number 1" if parse_number(n1) is None else ""
        label_b = "Number 2" if parse_number(n2) is None else ""
        if label_a and label_b:
            msg = f"Invalid input for {label_a} and {label_b}. Please enter valid numbers."
        elif label_a:
            msg = f"Invalid input for {label_a}. Please enter a valid number."
        elif label_b:
            msg = f"Invalid input for {label_b}. Please enter a valid number."
        else:
            msg = "Please enter valid numeric values."
        return msg, "error"

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    else:
        return f"Unknown operation '{op}'.", "error"

    # Format nicely: drop trailing .0 for whole numbers
    if result == int(result):
        formatted = str(int(result))
    else:
        formatted = f"{result:.6f}".rstrip("0").rstrip(".")

    return formatted, "success"


def render_html():
    """Build the HTML page with current app_state baked in."""
    escaped_num1 = html.escape(app_state["num1"], quote=True)
    escaped_num2 = html.escape(app_state["num2"], quote=True)
    num1_val = f' value="{escaped_num1}"' if app_state["num1"] else ""
    num2_val = f' value="{escaped_num2}"' if app_state["num2"] else ""

    result_html = ""
    if app_state["result_text"]:
        css_class = "result-success" if app_state["result_type"] == "success" else "result-error"
        icon = "✓" if app_state["result_type"] == "success" else "⚠"
        label = "Result" if app_state["result_type"] == "success" else "Error"
        escaped_result = html.escape(app_state["result_text"], quote=True)
        result_html = f'''    <div class="result-box {css_class}">
      <strong>{icon} {label}:</strong> {escaped_result}
    </div>\n'''

    return HTML_TEMPLATE.format(
        num1_val=num1_val,
        num2_val=num2_val,
        result_html=result_html,
    )


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class CalculatorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "":
            body = render_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/" or self.path == "":
            # Read form body
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length).decode("utf-8")

            # Parse application/x-www-form-urlencoded
            params = {}
            if raw:
                for pair in raw.split("&"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        from urllib.parse import unquote_plus
                        params[unquote_plus(k)] = unquote_plus(v)

            # Update state with submitted values
            app_state["num1"] = params.get("num1", "").strip()
            app_state["num2"] = params.get("num2", "").strip()
            op = params.get("op", "")

            if op in ("+", "-"):
                result_text, result_type = compute(op, app_state["num1"], app_state["num2"])
                app_state["result_text"] = result_text
                app_state["result_type"] = result_type
            else:
                # No operation selected – keep previous state or show hint
                app_state["result_text"] = "Select an operation (+ or -) to calculate."
                app_state["result_type"] = "error"

            body = render_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not Found")

    # Quiet default logging to keep output clean
    def log_message(self, format, *args):
        pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), CalculatorHandler)
    print(f"Calculator app running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
