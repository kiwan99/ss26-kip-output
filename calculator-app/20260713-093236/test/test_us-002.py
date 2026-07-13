import urllib.request
import urllib.parse


BASE_URL = "http://localhost:37077"


def test_server_side_calculation_and_display():
    """Cover all acceptance criteria for US-002 in one HTTP smoke test.

    Criteria covered:
    - Submitting the form triggers server-side computation.
    - The page re-renders after submission displaying the entered inputs and selected operation.
    - A clearly labeled Result area shows the computed value.
    - The calculation correctly handles addition, subtraction, multiplication, and division.
    """
    cases = [
        ("10", "5", "add", 15),
        ("10", "3", "subtract", 7),
        ("4", "6", "multiply", 24),
        ("9", "3", "divide", 3.0),
    ]

    for num1, num2, operation, expected in cases:
        data = urllib.parse.urlencode({"num1": num1, "num2": num2, "operation": operation}).encode()
        req = urllib.request.Request(BASE_URL + "/", data=data, method="POST")
        with urllib.request.urlopen(req) as resp:
            html_bytes = resp.read().decode("utf-8")

        # Criterion 1: Server-side computation triggered (200 response from POST)
        assert resp.status == 200, f"Expected 200 for {operation}, got {resp.status}"

        # Criterion 2: Page re-renders with entered inputs and selected operation
        assert f'value="{num1}"' in html_bytes, f"Input num1={num1} not reflected in page ({operation})"
        assert f'value="{num2}"' in html_bytes, f"Input num2={num2} not reflected in page ({operation})"
        assert f'<option value="{operation}" selected>' in html_bytes, (
            f"Operation '{operation}' not shown as selected ({operation})"
        )

        # Criterion 3: Clearly labeled Result area shows computed value
        assert '<div class="result-area success">' in html_bytes, (
            f"Result area missing for {operation}"
        )
        assert "<label>Result:</label>" in html_bytes, (
            f"Result label missing for {operation}"
        )
        expected_str = str(expected) if not isinstance(expected, float) else str(expected)
        # Handle integer results that may render as "15.0" or "15"
        assert expected_str in html_bytes or f"{expected:.1f}" in html_bytes, (
            f"Expected result '{expected}' not found in page for {operation}. Got: {html_bytes[html_bytes.find('result-value'):html_bytes.find('result-value')+30]}"
        )

        # Criterion 4: Calculation is correct (value matches expected)
        assert f'id="result-value">{expected_str}</span>' in html_bytes or \
               f'id="result-value">{expected:.1f}</span>' in html_bytes, (
            f"Computed value mismatch for {operation}: expected {expected}"
        )
