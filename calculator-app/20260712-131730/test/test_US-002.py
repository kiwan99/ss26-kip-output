"""Tests for US-002: Server-Side Calculation and Result Display.

Acceptance Criteria Covered:
1. Submitting the form computes the result server-side.
2. The page re-renders with a labeled result area showing the computed value.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import app as calculator_app


# ---------------------------------------------------------------------------
# Unit Tests (using Flask test_client — no running server required)
# ---------------------------------------------------------------------------

def _client():
    """Return a fresh test client."""
    return calculator_app.app.test_client()


class TestServerSideCalculation:
    """AC1: Submitting the form computes the result server-side."""

    def test_post_addition_computes_correctly(self):
        """POST with add operation returns correct sum in response."""
        client = _client()
        resp = client.post("/", data={"num1": "3", "num2": "4", "operation": "add"})
        body = resp.get_data(as_text=True)

        assert resp.status_code == 200
        # Result value must appear in rendered HTML (server-side computation)
        assert "7.0" in body, f"Expected '7.0' in response body.\nGot: {body}"

    def test_post_subtraction_computes_correctly(self):
        """POST with subtract operation returns correct difference."""
        client = _client()
        resp = client.post("/", data={"num1": "10", "num2": "3", "operation": "subtract"})
        body = resp.get_data(as_text=True)

        assert resp.status_code == 200
        assert "7.0" in body, f"Expected '7.0' in response.\nGot: {body}"

    def test_post_multiplication_computes_correctly(self):
        """POST with multiply operation returns correct product."""
        client = _client()
        resp = client.post("/", data={"num1": "5", "num2": "6", "operation": "multiply"})
        body = resp.get_data(as_text=True)

        assert resp.status_code == 200
        assert "30.0" in body, f"Expected '30.0' in response.\nGot: {body}"

    def test_post_division_computes_correctly(self):
        """POST with divide operation returns correct quotient."""
        client = _client()
        resp = client.post("/", data={"num1": "15", "num2": "3", "operation": "divide"})
        body = resp.get_data(as_text=True)

        assert resp.status_code == 200
        assert "5.0" in body, f"Expected '5.0' in response.\nGot: {body}"


class TestResultAreaDisplay:
    """AC2: The page re-renders with a labeled result area showing the computed value."""

    def test_result_area_shows_label_and_value(self):
        """Successful POST renders <strong>Result:</strong> label with computed value."""
        client = _client()
        resp = client.post("/", data={"num1": "2", "num2": "3", "operation": "add"})
        body = resp.get_data(as_text=True)

        assert resp.status_code == 200
        # Labeled result area must be present in re-rendered page
        assert "<strong>Result:</strong>" in body, (
            f"Expected '<strong>Result:</strong>' label in response.\nGot: {body}"
        )
        assert "5.0" in body, f"Expected computed value '5.0' in result area.\nGot: {body}"

    def test_error_area_shows_label_on_division_by_zero(self):
        """Division by zero renders <strong>Error:</strong> label with error message."""
        client = _client()
        resp = client.post("/", data={"num1": "10", "num2": "0", "operation": "divide"})
        body = resp.get_data(as_text=True)

        assert resp.status_code == 200
        # Error result area must be present in re-rendered page
        assert "<strong>Error:</strong>" in body, (
            f"Expected '<strong>Error:</strong>' label in response.\nGot: {body}"
        )
        assert "Division by zero" in body, (
            f"Expected 'Division by zero' error message in result area.\nGot: {body}"
        )


# ---------------------------------------------------------------------------
# Integration Tests (live server at http://localhost:8000)
# ---------------------------------------------------------------------------

try:
    import httpx
except ImportError:
    import requests as httpx  # fallback if httpx unavailable

BASE_URL = "http://localhost:8000"


class TestIntegrationServerSideCalculation:
    """AC1 integration: live server computes result on POST."""

    def test_live_post_addition(self):
        """Live POST to / with add returns correct computed result."""
        resp = httpx.post(
            f"{BASE_URL}/",
            data={"num1": "7", "num2": "8", "operation": "add"},
            timeout=5,
        )
        assert resp.status_code == 200
        body = resp.text
        assert "15.0" in body, f"Expected '15.0' in live response.\nGot: {body}"


class TestIntegrationResultDisplay:
    """AC2 integration: live server re-renders page with labeled result area."""

    def test_live_post_shows_result_area(self):
        """Live POST renders page containing Result label and computed value."""
        resp = httpx.post(
            f"{BASE_URL}/",
            data={"num1": "9", "num2": "1", "operation": "subtract"},
            timeout=5,
        )
        assert resp.status_code == 200
        body = resp.text

        # Must contain the labeled result area from template
        assert "<strong>Result:</strong>" in body, (
            f"Expected '<strong>Result:</strong>' label in live response.\nGot: {body}"
        )
        assert "8.0" in body, f"Expected computed value '8.0' in result area.\nGot: {body}"
