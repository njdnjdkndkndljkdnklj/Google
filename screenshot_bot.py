import asyncio
from playwright.async_api import async_playwright

async def screenshot_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        
        try:
            await page.goto('https://meet.google.com/jzn-xoee-pvr')
            await asyncio.sleep(5)
            
            # Take screenshot
            await page.screenshot(path='bot_page.png', full_page=True)
            print('📸 Screenshot saved as bot_page.png')
            
            # Get page info
            title = await page.title()
            url = page.url
            print(f'Title: {title}')
            print(f'URL: {url}')
            
        except Exception as e:
            print(f'Error: {e}')
        finally:
            await browser.close()

asyncio.run(screenshot_bot())