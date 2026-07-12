import urllib.request
import urllib.parse


BASE = "http://localhost:41003"


def test_submit_form_renders_result_with_inputs():
    """Verify server-side computation, re-rendering, labeled result area, and preserved inputs."""
    # POST form data: 10 + 5 = 15
    data = urllib.parse.urlencode({"num1": "10", "num2": "5", "operation": "add"}).encode()
    req = urllib.request.Request(BASE, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")

    # Criterion 1 & 2: Server-side computation triggers re-render with calculated value
    assert "15" in html, "Computed result not present in rendered page"

    # Criterion 3: Clearly labeled result area shows numeric output
    assert 'class="result-area"' in html, "Result area div missing"
    assert 'class="result-label"' in html, "Result label missing"
    assert ">Result<" in html, "Result label text not found"
    assert 'class="result-value"' in html, "Result value element missing"

    # Criterion 4: Original input values and chosen operation remain visible
    assert 'value="10"' in html, "First number input not preserved"
    assert 'value="5"' in html, "Second number input not preserved"
    assert '<option value="add" selected>' in html, "Chosen operation not shown as selected"
