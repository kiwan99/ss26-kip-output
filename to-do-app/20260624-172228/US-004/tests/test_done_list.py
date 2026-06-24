import asyncio
from playwright.async_api import async_playwright
import pytest

@pytest.mark.asyncio
async def test_done_list():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Test 1: Add item and check it appears in Done list
        await page.goto('http://sandbox-app:8000', wait_until='networkidle')
        await page.wait_for_selector('form[action="/add"] input[name="content"]')
        await page.fill('form[action="/add"] input[name="content"]', 'Test Item 1')
        await page.click('form[action="/add"] button[type="submit"]')
        await page.click(f"a[href='/done/1']")
        await page.goto('http://sandbox-app:8000/done')
        assert await page.text_content('li') == 'Test Item 1 (Completed at: )'
        await page.screenshot(path="/tests/screenshots/test_done_list_1.png")

        # Test 2: Visual distinction between active and done items
        await page.goto('http://sandbox-app:8000')
        assert await page.text_content('li') == ''
        assert await page.text_content('li.done') is None
        await page.screenshot(path="/tests/screenshots/test_done_list_2.png")

        # Test 3: Completion order preservation
        await page.goto('http://sandbox-app:8000')
        await page.wait_for_selector('form[action="/add"] input[name="content"]')
        await page.fill('form[action="/add"] input[name="content"]', 'Test Item 2')
        await page.click('form[action="/add"] button[type="submit"]')
        await page.click(f"a[href='/done/2']")
        await page.goto('http://sandbox-app:8000/done')
        items = await page.text_content('ul')
        assert 'Test Item 1' in items
        assert 'Test Item 2' in items
        assert items.find('Test Item 1') < items.find('Test Item 2')
        await page.screenshot(path="/tests/screenshots/test_done_list_3.png")

        await browser.close()