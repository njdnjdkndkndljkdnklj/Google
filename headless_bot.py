import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-web-security', '--use-fake-ui-for-media-stream']
        )
        
        for i in range(10):
            page = await browser.new_page()
            try:
                await page.goto('https://meet.google.com/jzn-xoee-pvr', timeout=30000)
                await page.fill('input', f'Bot-{i+1}')
                await page.click('text="Join now"')
                print(f'✅ Bot-{i+1} joined')
            except Exception as e:
                print(f'❌ Bot-{i+1} failed: {str(e)[:50]}')
            await asyncio.sleep(1)
        
        await asyncio.sleep(300)
        await browser.close()

asyncio.run(main())