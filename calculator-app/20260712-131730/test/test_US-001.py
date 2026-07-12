"""Tests for US-001: Core Calculator UI and Form Submission."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import app


# ---------------------------------------------------------------------------
# Unit tests via Flask test_client (no running server required)
# ---------------------------------------------------------------------------

def _client():
    """Return a fresh Flask test client."""
    return app.app.test_client()


def test_root_page_loads_html():
    """AC1: The page loads at the root route / with a plain HTML UI."""
    client = _client()
    resp = client.get("/")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    body = resp.get_data(as_text=True)
    assert "<!DOCTYPE html>" in body or "<html" in body, "Response is not HTML"


def test_two_number_inputs_present():
    """AC2: Two number inputs are present on the page."""
    client = _client()
    resp = client.get("/")
    body = resp.get_data(as_text=True)

    # Check for num1 input
    assert 'name="num1"' in body, "Missing num1 input field"
    assert 'type="number"' in body, "Missing number type on inputs"

    # Check for num2 input
    assert 'name="num2"' in body, "Missing num2 input field"


def test_operation_picker_has_four_options():
    """AC3: A way to pick one of the four basic operations is available."""
    client = _client()
    resp = client.get("/")
    body = resp.get_data(as_text=True)

    assert 'name="operation"' in body, "Missing operation select field"
    for op in ("add", "subtract", "multiply", "divide"):
        assert f'value="{op}"' in body, f"Missing option value '{op}'"


def test_calculate_button_submits_form():
    """AC4: A Calculate button submits the form."""
    client = _client()

    # Verify the button exists on GET
    resp_get = client.get("/")
    body = resp_get.get_data(as_text=True)
    assert 'type="submit"' in body, "Missing submit button"
    assert ">Calculate<" in body or ">Calculate</button>" in body, \
        "Button text is not 'Calculate'"

    # Verify POST submission works (form action="/", method=POST)
    resp_post = client.post("/", data={
        "num1": "3",
        "num2": "4",
        "operation": "add"
    })
    assert resp_post.status_code == 200, f"POST returned {resp_post.status_code}"

    # Result should be displayed after successful calculation
    body_post = resp_post.get_data(as_text=True)
    assert "7.0" in body_post or "Result:" in body_post, \
        "Calculation result not shown after form submission"


# ---------------------------------------------------------------------------
# Integration test (requires running server at http://localhost:8000)
# ---------------------------------------------------------------------------

def test_root_reachable_via_http():
    """Integration: Verify the app is reachable and serves HTML at /."""
    import httpx
    resp = httpx.get("http://localhost:8000/", timeout=5)
    assert resp.status_code == 200, f"Server returned {resp.status_code}"
    body = resp.text
    assert "<!DOCTYPE html>" in body or "<html" in body, "Response is not HTML"
