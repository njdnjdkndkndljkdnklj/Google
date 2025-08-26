import asyncio
from playwright.async_api import async_playwright

async def join_visible():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-web-security', '--use-fake-ui-for-media-stream']
        )
        
        for i in range(10):
            page = await browser.new_page()
            try:
                await page.goto('https://meet.google.com/jzn-xoee-pvr')
                await page.wait_for_selector('input, button', timeout=15000)
                
                # Fill name
                await page.fill('input', f'Bot-{i+1}')
                await asyncio.sleep(1)
                
                # Join
                await page.click('text="Join now"')
                print(f'✅ Bot-{i+1} joined')
                
                # Send message
                await asyncio.sleep(3)
                try:
                    await page.keyboard.press('Tab')
                    await page.keyboard.press('Tab') 
                    await page.keyboard.press('Enter')
                    await page.type('text', f'Bot-{i+1} has joined!')
                    await page.keyboard.press('Enter')
                except:
                    pass
                    
            except Exception as e:
                print(f'❌ Bot-{i+1}: {str(e)[:30]}')
            
            await asyncio.sleep(2)
        
        await asyncio.sleep(300)
        await browser.close()

asyncio.run(join_visible())