import urllib.request
import urllib.parse


BASE_URL = "http://localhost:37077"


def _post(data: dict) -> str:
    """POST form data and return the HTML response body."""
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=body, method="POST")
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def test_validation_errors():
    """Covers AC1 (empty inputs), AC2 (non-numeric), and AC3 (division by zero)."""

    # AC1: Empty number inputs → error message about fields that must be filled in
    html_empty_num1 = _post({"num1": "", "num2": "5", "operation": "add"})
    assert "Error:" in html_empty_num1, "Empty num1 should produce an error"
    assert "Number 1" in html_empty_num1, "Error should mention Number 1"

    html_both_empty = _post({"num1": "", "num2": "", "operation": "add"})
    assert "Error:" in html_both_empty
    assert "Number 1" in html_both_empty and "Number 2" in html_both_empty

    # AC2: Non-numeric entries → validation warning
    html_non_numeric = _post({"num1": "abc", "num2": "5", "operation": "add"})
    assert "Warning:" in html_non_numeric, "Non-numeric input should produce a warning"
    assert "valid numeric values" in html_non_numeric

    # AC3: Division by zero → specific error message
    html_div_zero = _post({"num1": "10", "num2": "0", "operation": "divide"})
    assert "Error:" in html_div_zero, "Division by zero should produce an error"
    assert "Division by zero is not allowed" in html_div_zero


def test_preserves_values_after_submission():
    """Covers AC4: entered values are preserved in form fields after submission."""

    # Submit valid data — result shown, but inputs preserved
    html_valid = _post({"num1": "3", "num2=": "7", "operation": "multiply"})
    assert 'value="3"' in html_valid or 'value="3">' in html_valid, \
        "num1 value should be preserved"

    # Submit invalid data — error shown, but inputs still preserved so user can fix them
    html_non_numeric = _post({"num1": "abc", "num2": "5", "operation": "add"})
    assert 'value="abc"' in html_non_numeric, \
        "Non-numeric num1 should be preserved for re-editing"
    assert 'value="5"' in html_non_numeric or 'value="5">' in html_non_numeric, \
        "num2 value should be preserved"

    # Submit empty field — error shown, but other filled fields preserved
    html_empty = _post({"num1": "", "num2": "9", "operation": "subtract"})
    assert 'value="9"' in html_empty or 'value="9">' in html_empty, \
        "Filled num2 should be preserved after empty-field error"
