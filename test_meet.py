import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        
        await page.goto('https://meet.google.com/jzn-xoee-pvr')
        await page.wait_for_load_state('networkidle')
        
        # Get page content
        content = await page.content()
        print("Page loaded successfully")
        print(f"Content length: {len(content)}")
        
        # Check for key elements
        inputs = await page.query_selector_all('input')
        buttons = await page.query_selector_all('button')
        
        print(f"Found {len(inputs)} inputs and {len(buttons)} buttons")
        
        if buttons:
            for i, btn in enumerate(buttons[:5]):
                text = await btn.inner_text()
                print(f"Button {i}: '{text.strip()}'")
        
        await browser.close()

asyncio.run(test())