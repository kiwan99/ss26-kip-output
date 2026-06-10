"""
Number Adder QA Test Suite - User Story US-001: Core Calculation Feature (Browser UI Tests)

Acceptance Criteria to Verify via Playwright Browser:
  AC_001_The application displays exactly two input fields for entering numeric values.
  AC_002_A clear action button labeled 'Add' is placed next to or below the inputs. 
  AC_003_Upon clicking Add with valid numbers in both fields, a Result area immediately appears displaying the sum of the two entered values.

Screenshot Strategy (per requirement): Take screenshots at:
  - After page loads  
  - After each user interaction (fill forms, click buttons)
  - After verifying result displays or fails
    
"""

from playwright.sync_api import sync_playwright, expect, TimeoutError as PlayTimeout
import time


# Connection retry configuration for potentially slow-starting servers 
RETRY_MAX = 3
WAIT_SEC_BETWEEN_RETRIES = (60-15) 

def load_page_with_retries(url="http://sandbox-app/"):
    """Connect to application with retries."""
    browser, page_obj = None, None
    
    for attempt in range(1, RETRY_MAX + 1): 
        if browser is not None: 
            context_new = browser.new_context(ignore_https_errors=True)
            page_obj_retrying = context_new.new_page()
