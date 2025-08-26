import asyncio
from playwright.async_api import async_playwright
import random

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=VizDisplayCompositor",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Anti-detection script
        await context.add_init_script("""
            delete navigator.__proto__.webdriver;
            navigator.webdriver = false;
            window.chrome = {runtime: {}};
        """)
        
        page = await context.new_page()
        await page.goto("https://meet.google.com/oru-azsu-cmo")
        await asyncio.sleep(5)
        
        # Check if we get the real interface
        inputs = await page.query_selector_all('input')
        buttons = await page.query_selector_all('button')
        
        print(f"Stealth test - Inputs: {len(inputs)}, Buttons: {len(buttons)}")
        
        if len(inputs) > 0:
            print("✅ STEALTH BYPASS SUCCESSFUL!")
            await page.type('input', 'Stealth Bot', delay=100)
            await asyncio.sleep(2)
            if len(buttons) >= 4:
                await buttons[3].click()
            print("✅ Bot joined with stealth!")
        else:
            print("❌ Still blocked")
        
        await asyncio.sleep(30)
        await browser.close()

asyncio.run(main())