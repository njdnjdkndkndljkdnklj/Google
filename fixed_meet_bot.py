import asyncio
from playwright.async_api import async_playwright

async def join_meet_bots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Must be False for Meet
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage", 
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        for i in range(10):
            page = await browser.new_page()
            try:
                # Navigate to Meet
                await page.goto('https://meet.google.com/jzn-xoee-pvr')
                await page.wait_for_load_state('networkidle')
                
                # Debug info
                print(f"Bot-{i+1} - URL: {page.url}")
                print(f"Bot-{i+1} - Title: {await page.title()}")
                
                # Handle consent popup
                try:
                    await page.click("button:has-text('I agree')", timeout=3000)
                except:
                    pass
                
                # Fill name
                await page.fill('input[type="text"]', f'Bot-{i+1}')
                await asyncio.sleep(1)
                
                # Join meeting
                await page.click('text="Join now"')
                print(f'✅ Bot-{i+1} joined successfully')
                
                # Send chat message
                await asyncio.sleep(3)
                await page.keyboard.type(f'Bot-{i+1} has joined!')
                await page.keyboard.press('Enter')
                
            except Exception as e:
                print(f'❌ Bot-{i+1} failed: {str(e)[:50]}')
            
            await asyncio.sleep(2)
        
        # Keep bots in meeting
        await asyncio.sleep(300)
        await browser.close()

asyncio.run(join_meet_bots())