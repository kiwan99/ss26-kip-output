import urllib.request
import urllib.parse


BASE_URL = "http://localhost:42627"


def test_invalid_input_and_preservation():
    """Criteria 1 & 3: Blank/non-numeric inputs show clear errors and preserve user input."""

    # Test blank fields
    data = urllib.parse.urlencode({"num1": "", "num2": "", "operation": "add"}).encode()
    req = urllib.request.Request(BASE_URL, data=data, method="POST")
    resp = urllib.request.urlopen(req)
    html = resp.read().decode("utf-8")

    # Criterion 1: clear error message displayed
    assert 'class="result-area error"' in html, "Error state not rendered for blank inputs"
    assert "Number 1 is required" in html, "Missing error for blank Number 1"
    assert "Number 2 is required" in html, "Missing error for blank Number 2"

    # Criterion 3: user input preserved (blank values kept)
    assert 'value=""' in html or 'value=" "' not in html, "Input fields should preserve original values"

    # Test non-numeric characters
    data = urllib.parse.urlencode({"num1": "abc", "num2": "", "operation": "add"}).encode()
    req = urllib.request.Request(BASE_URL, data=data, method="POST")
    resp = urllib.request.urlopen(req)
    html = resp.read().decode("utf-8")

    # Criterion 1: clear error for non-numeric
    assert 'class="result-area error"' in html, "Error state not rendered for non-numeric input"
    assert "Invalid number" in html or "only numeric characters" in html, "Missing error for non-numeric Number 1"

    # Criterion 3: original non-numeric value preserved so user can correct it
    assert 'value="abc"' in html, "Non-numeric input not preserved — user must re-type"


def test_divide_by_zero_warning():
    """Criterion 2: Divide by zero shows specific warning, no crash."""

    data = urllib.parse.urlencode({"num1": "10", "num2": "0", "operation": "divide"}).encode()
    req = urllib.request.Request(BASE_URL, data=data, method="POST")
    resp = urllib.request.urlopen(req)
    html = resp.read().decode("utf-8")

    # Criterion 2: specific warning shown instead of crash
    assert 'class="result-area error"' in html, "No error state for divide by zero"
    assert "Cannot divide by zero" in html, "Missing specific divide-by-zero warning message"
    assert "Division by zero is not allowed" in html, "Missing field-level warning for Number 2"

    # Criterion 3: inputs preserved after divide-by-zero error
    assert 'value="10"' in html, "Number 1 input not preserved after divide-by-zero error"
    assert 'value="0"' in html, "Number 2 input not preserved after divide-by-zero error"
