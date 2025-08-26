import asyncio
from playwright.async_api import async_playwright

async def create_bot(browser, bot_id):
    try:
        page = await browser.new_page()
        await page.goto('https://meet.google.com/jzn-xoee-pvr')
        await page.wait_for_load_state('networkidle')
        
        # Handle consent
        try:
            await page.click("button:has-text('I agree')", timeout=2000)
        except:
            pass
        
        # Fill name and join
        await page.fill('input[type="text"]', f'Bot-{bot_id}')
        await page.click('text="Join now"')
        
        # Send message
        await asyncio.sleep(2)
        await page.keyboard.type(f'Bot-{bot_id} joined the meeting!')
        await page.keyboard.press('Enter')
        
        print(f'✅ Bot-{bot_id} joined and sent message')
        return page
        
    except Exception as e:
        print(f'❌ Bot-{bot_id} failed: {str(e)[:40]}')
        return None

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream"
            ]
        )
        
        # Create all bots
        pages = []
        for i in range(1, 11):
            page = await create_bot(browser, i)
            if page:
                pages.append(page)
            await asyncio.sleep(3)
        
        print(f"🎉 {len(pages)} bots successfully joined!")
        
        # Keep alive
        await asyncio.sleep(600)
        await browser.close()

asyncio.run(main())