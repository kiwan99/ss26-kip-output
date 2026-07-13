import urllib.request


def test_ui_elements_at_root():
    """Verify the root route serves a page with two number inputs, an operation picker (add/subtract/multiply/divide), and a Calculate button."""
    url = "http://localhost:37077/"

    # Criterion 1: Page loads at root route /
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    assert resp.status == 200, f"Expected 200, got {resp.status}"
    content_type = resp.headers.get("Content-Type", "")
    assert "text/html" in content_type, f"Expected text/html, got {content_type}"

    html = resp.read().decode("utf-8")

    # Criterion 2: Two number input fields (match <input type="number"...> not CSS rules)
    num_inputs = [line for line in html.split("\n") if '<input type="number"' in line]
    assert len(num_inputs) == 2, f"Expected 2 number inputs, found {len(num_inputs)}"

    # Criterion 3: Operation picker with add, subtract, multiply, divide
    assert "<select" in html, "Missing <select> element for operation picker"
    for op in ("add", "subtract", "multiply", "divide"):
        assert f'value="{op}"' in html, f"Missing option value={op} in select"

    # Criterion 4: Calculate button present
    assert 'type="submit"' in html and "Calculate" in html, (
        "Missing submit button labeled 'Calculate'"
    )
