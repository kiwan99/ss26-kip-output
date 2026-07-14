import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# ---------------------------------------------------------------------------
# Static assets embedded as strings to avoid external dependencies
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         "Helvetica Neue", Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f0f2f5;
        }

        .calculator {
            width: 100%;
            max-width: 360px;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
            padding: 20px;
        }

        .display {
            width: 100%;
            background-color: #1a1a2e;
            color: #ffffff;
            font-size: 2rem;
            text-align: right;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
            min-height: 64px;
            overflow-x: auto;
            white-space: nowrap;
        }

        .buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }

        .btn {
            font-size: 1.4rem;
            padding: 18px 0;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background-color: #e9ecef;
            color: #212529;
            transition: background-color 0.15s ease, transform 0.1s ease;
            user-select: none;
        }

        .btn:hover {
            background-color: #dee2e6;
        }

        .btn:active {
            transform: scale(0.96);
            background-color: #ced4da;
        }

        @media (max-width: 480px) {
            body {
                align-items: flex-start;
                padding-top: 20px;
            }

            .calculator {
                max-width: 100%;
                border-radius: 0;
                box-shadow: none;
                padding: 16px;
            }

            .display {
                font-size: 1.6rem;
                padding: 12px 16px;
            }

            .btn {
                font-size: 1.2rem;
                padding: 14px 0;
            }
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div id="display" class="display">0</div>
        <div class="buttons">
            <button class="btn num-btn" data-value="7">7</button>
            <button class="btn num-btn" data-value="8">8</button>
            <button class="btn num-btn" data-value="9">9</button>
            <button class="btn num-btn" data-value="4">4</button>
            <button class="btn num-btn" data-value="5">5</button>
            <button class="btn num-btn" data-value="6">6</button>
            <button class="btn num-btn" data-value="1">1</button>
            <button class="btn num-btn" data-value="2">2</button>
            <button class="btn num-btn" data-value="3">3</button>
            <button class="btn num-btn" data-value="0">0</button>
        </div>
    </div>

    <script>
        (function () {
            var display = document.getElementById('display');
            var buttons = document.querySelectorAll('.num-btn');

            for (var i = 0; i < buttons.length; i++) {
                buttons[i].addEventListener('click', function () {
                    var digit = this.getAttribute('data-value');
                    if (display.textContent === '0') {
                        display.textContent = digit;
                    } else {
                        display.textContent += digit;
                    }
                });
            }
        })();
    </script>
</body>
</html>
"""


class CalculatorHandler(BaseHTTPRequestHandler):
    """HTTP handler serving the calculator web app."""

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Server-render initial state: display shows "0"
            body = HTML_TEMPLATE
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(body.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            body = b'Not Found\n'
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, format, *args):
        """Suppress default request logging for cleaner output."""
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(('0.0.0.0', port), CalculatorHandler)
    print(f"Calculator app running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
