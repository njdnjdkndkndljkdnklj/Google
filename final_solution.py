import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=VizDisplayCompositor",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--allow-running-insecure-content",
                "--disable-web-security",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Launch just 1 bot first to test
        page = await context.new_page()
        await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        inputs = await page.query_selector_all('input')
        buttons = await page.query_selector_all('button')
        print(f"Found {len(inputs)} inputs and {len(buttons)} buttons")
        
        if len(inputs) > 0:
            await page.fill('input', 'Test Bot')
            await page.click('text="Join now"')
            print("✅ Bot joined successfully!")
            await asyncio.sleep(300)
        else:
            print("❌ Still getting error page")
        
        await browser.close()

asyncio.run(main())