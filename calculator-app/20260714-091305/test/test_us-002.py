import urllib.request
import urllib.parse


def test_server_side_calculation_and_display():
    """Covers all three acceptance criteria for US-002:
    1. Form submission triggers server-side computation and re-renders with result in labeled area.
    2. Computed value correctly reflects the selected operation on the two numbers.
    3. Original input values remain visible after submission."""

    url = "http://localhost:42627/"
    data = urllib.parse.urlencode({"num1": "10", "num2": "5", "operation": "multiply"}).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")

    # Criterion 1: Result displayed in a labeled area after server-side computation
    assert '<div class="result-area">' in html, "Result area div missing"
    assert "<div class=\"result-label\">Result</div>" in html, "Result label missing"
    assert "<div class=\"result-value\">" in html, "Result value element missing"

    # Criterion 2: Computed value correctly reflects the operation (10 * 5 = 50)
    assert ">50<" in html or '>50.0<' in html, "Computed result does not match expected value for multiply"

    # Criterion 3: Original input values remain visible after submission
    assert 'value="10"' in html, "Original num1 value not preserved"
    assert 'value="5"' in html, "Original num2 value not preserved"