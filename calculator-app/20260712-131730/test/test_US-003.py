"""Tests for US-003: Division by Zero Error Handling."""

from pathlib import Path
import sys
import re

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import app


# ---------------------------------------------------------------------------
# Unit tests (core logic + Flask test client)
# ---------------------------------------------------------------------------

def test_calculate_division_by_zero_returns_error():
    """Division by zero returns an error message, not a result."""
    result, error = app.calculate(10.0, 0.0, "divide")
    assert result is None, "Result should be None on division by zero"
    assert error is not None, "Error message must be present"
    assert "Division by zero" in error


def test_calculate_valid_division_succeeds():
    """Valid division returns a numeric result with no error."""
    result, error = app.calculate(10.0, 2.0, "divide")
    assert result == 5.0
    assert error is None


def test_route_post_division_by_zero_shows_error():
    """POST to / with divide and num2=0 renders an error message in HTML."""
    client = app.app.test_client()
    response = client.post("/", data={"num1": "10", "num2": "0", "operation": "divide"})

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    body = response.get_data(as_text=True)

    # Error message must appear in the rendered HTML
    assert "Error: Division by zero is not allowed." in body
    # Error styling class should be present
    assert 'class="result-area error"' in body


# ---------------------------------------------------------------------------
# Integration tests (live server via httpx) — at most 2
# ---------------------------------------------------------------------------

def test_integration_division_by_zero_http():
    """Live HTTP POST: division by zero returns error, not a crash."""
    import httpx

    url = "http://localhost:8000"
    try:
        response = httpx.post(url, data={"num1": "5", "num2": "0", "operation": "divide"})
    except httpx.ConnectError:
        # Server not reachable — valid finding, not a test bug
        assert False, "Application server at localhost:8000 is not reachable"

    assert response.status_code == 200
    body = response.text
    assert "Division by zero" in body


def test_minimal_no_auth_db_js_frameworks():
    """App uses only Flask + plain HTML/CSS — no auth, DB, or JS frameworks."""
    src_dir = Path(__file__).resolve().parent / "src"

    # Read all Python source files
    py_files = list(src_dir.rglob("*.py"))
    all_py_content = ""
    for f in py_files:
        all_py_content += f.read_text() + "\n"

    # Check for auth-related imports/patterns
    assert "auth" not in all_py_content.lower(), "No authentication should be present"
    assert "login" not in all_py_content.lower(), "No login functionality expected"
    assert "password" not in all_py_content.lower(), "No password handling expected"

    # Check for database imports/patterns
    assert "sqlite" not in all_py_content.lower(), "No SQLite usage allowed"
    assert "sqlalchemy" not in all_py_content, "No SQLAlchemy allowed"
    assert "pymongo" not in all_py_content.lower(), "No MongoDB allowed"

    # Read HTML template files
    html_files = list(src_dir.rglob("*.html"))
    all_html_content = ""
    for f in html_files:
        all_html_content += f.read_text() + "\n"

    # Check for JS frameworks (React, Vue, Angular)
    assert "react" not in all_html_content.lower(), "No React framework allowed"
    assert "vue" not in all_html_content.lower(), "No Vue framework allowed"
    assert "angular" not in all_html_content.lower(), "No Angular framework allowed"

    # Verify no external JS libraries loaded via script tags (allow inline CSS)
    script_tags = re.findall(r'<script[^>]*src=["\'][^"\']+["\']', all_html_content, re.IGNORECASE)
    assert len(script_tags) == 0, "No external JavaScript libraries should be loaded"
