import asyncio
import random
import string
from playwright.async_api import async_playwright

def generate_name():
    names = ['Alex', 'Sam', 'Jordan', 'Casey', 'Taylor', 'Morgan', 'Riley', 'Avery']
    suffix = ''.join(random.choices(string.digits, k=2))
    return f"{random.choice(names)}-{suffix}"

async def create_bot(browser_context, bot_name):
    try:
        page = await browser_context.new_page()
        
        # Navigate to Meet
        await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Fill name in the input field
        await page.fill('input', bot_name)
        
        # Click "Continue without microphone and camera" to ensure muted
        try:
            await page.click('text="Continue without microphone and camera"')
            await asyncio.sleep(1)
        except:
            pass
        
        # Click "Join now"
        await page.click('text="Join now"')
        
        # Wait a moment then send join message
        await asyncio.sleep(3)
        await page.keyboard.type(f'{bot_name} has joined the meeting!')
        await page.keyboard.press('Enter')
        
        print(f'✅ {bot_name} joined successfully with mic/camera OFF')
        return page
        
    except Exception as e:
        print(f'❌ {bot_name} failed: {str(e)[:50]}')
        return None

async def launch_bots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--disable-web-security"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Create 10 bots simultaneously
        tasks = []
        for i in range(10):
            bot_name = generate_name()
            task = asyncio.create_task(create_bot(context, bot_name))
            tasks.append(task)
        
        print('🚀 Launching 10 bots simultaneously...')
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_bots = [r for r in results if r is not None and not isinstance(r, Exception)]
        print(f'🎉 {len(successful_bots)} bots joined successfully!')
        
        # Keep bots in meeting for 5 minutes
        print('⏰ Bots will stay in meeting for 5 minutes...')
        await asyncio.sleep(300)
        
        await browser.close()
        print('👋 All bots have left the meeting')

if __name__ == "__main__":
    asyncio.run(launch_bots())