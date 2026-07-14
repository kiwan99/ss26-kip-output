import re
import urllib.request


def test_calculator_input_form():
    """Verify root route renders form with two number inputs, four operations, and Calculate button."""
    url = "http://localhost:42627/"
    resp = urllib.request.urlopen(url)
    html = resp.read().decode("utf-8")

    # Criterion 1: exactly two number input fields (match HTML tags only, not CSS selectors)
    matches = re.findall(r'<input[^>]*type="number"', html)
    assert len(matches) == 2, f"Expected exactly 2 number inputs, found {len(matches)}"

    # Criterion 2: selection control with four operations (add, subtract, multiply, divide)
    assert "<select" in html, "Missing select element for operation"
    for op in ("add", "subtract", "multiply", "divide"):
        assert f'value="{op}"' in html, f"Missing option value '{op}'"

    # Criterion 3: Calculate button that submits form to server
    assert '<button type="submit">Calculate</button>' in html, "Missing Calculate submit button"
    assert 'method="post"' in html or "method='post'" in html, "Form missing POST method"
    assert 'action="/"' in html or "action='/'" in html, "Form action not set to /"
