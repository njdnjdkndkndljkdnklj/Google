import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        
        for i in range(10):
            page = await browser.new_page()
            try:
                await page.goto('https://meet.google.com/jzn-xoee-pvr')
                await page.wait_for_load_state('networkidle')
                
                # Try multiple selectors for name input
                name_filled = False
                for selector in ['input[type="text"]', 'input[placeholder*="name"]', 'input']:
                    try:
                        await page.fill(selector, f'Bot-{i+1}')
                        name_filled = True
                        break
                    except:
                        continue
                
                # Try join button
                joined = False
                for text in ['Join now', 'Ask to join', 'Join']:
                    try:
                        await page.click(f'text="{text}"')
                        joined = True
                        break
                    except:
                        continue
                
                if joined:
                    print(f'✅ Bot-{i+1} joined')
                    # Send chat message
                    await asyncio.sleep(2)
                    try:
                        await page.keyboard.press('Tab')
                        await page.keyboard.type(f'Bot-{i+1} has joined the meeting!')
                        await page.keyboard.press('Enter')
                    except:
                        pass
                else:
                    print(f'❌ Bot-{i+1} failed to join')
                    
            except Exception as e:
                print(f'❌ Bot-{i+1} error: {str(e)[:30]}')
        
        await asyncio.sleep(300)
        await browser.close()

asyncio.run(main())