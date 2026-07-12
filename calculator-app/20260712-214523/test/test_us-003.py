import urllib.request
import urllib.parse


BASE = "http://localhost:41003"


def post_form(data: dict) -> str:
    """POST form data and return the HTML response body."""
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(BASE, data=encoded, method="POST")
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def test_validation_errors():
    """Criteria 1 & 2: non-numeric input shows error; empty fields show prompt."""

    # Criterion 1: non-numeric characters → error message
    html = post_form({"num1": "abc", "num2": "5", "operation": "add"})
    assert "error" in html.lower(), "Expected error section for non-numeric input"
    assert "'abc' is not a valid number" in html, "Expected specific error message for 'abc'"

    # Criterion 2: empty required field → prompt to fill in missing values
    html = post_form({"num1": "", "num2": "5", "operation": "add"})
    assert "error" in html.lower(), "Expected error section for empty field"
    assert "Please enter a value for the first number" in html, \
        "Expected prompt to fill in missing first number"


def test_division_by_zero():
    """Criterion 3: division by zero displays clear warning instead of crashing."""

    html = post_form({"num1": "10", "num2": "0", "operation": "divide"})
    assert "error" in html.lower(), "Expected error section for division by zero"
    assert "Cannot divide by zero" in html, \
        "Expected clear warning message for division by zero"
    # App should not crash — we got a valid HTML response (200 OK)
    assert "<!DOCTYPE" in html or "<html" in html, "App returned valid HTML instead of crashing"
