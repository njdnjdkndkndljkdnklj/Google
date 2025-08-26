import asyncio
import random
import string
from playwright.async_api import async_playwright

def generate_human_name():
    names = ['Alex', 'Sam', 'Jordan', 'Casey', 'Taylor', 'Morgan', 'Riley', 'Avery', 'Quinn', 'Blake']
    suffix = ''.join(random.choices(string.digits, k=2))
    return f"{random.choice(names)}-{suffix}"

async def create_bot(browser, meet_url, bot_name):
    try:
        page = await browser.new_page()
        await page.goto(meet_url)
        await page.wait_for_load_state('networkidle')
        
        # Handle consent
        try:
            await page.click("button:has-text('I agree')", timeout=2000)
        except:
            pass
        
        # Fill name
        await page.fill('input[type="text"]', bot_name)
        
        # Join meeting
        await page.click('text="Join now"')
        
        # Send message
        await asyncio.sleep(2)
        await page.keyboard.type(f'{bot_name} joined!')
        await page.keyboard.press('Enter')
        
        print(f'✅ {bot_name} joined successfully')
        return page
        
    except Exception as e:
        print(f'❌ {bot_name} failed: {str(e)[:40]}')
        return None

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--mute-audio"
            ]
        )
        
        meet_url = "https://meet.google.com/jzn-xoee-pvr"
        
        # Create all bots simultaneously
        tasks = []
        for i in range(10):
            bot_name = generate_human_name()
            task = asyncio.create_task(create_bot(browser, meet_url, bot_name))
            tasks.append(task)
        
        print('🚀 Launching 10 bots simultaneously...')
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_bots = [r for r in results if r is not None and not isinstance(r, Exception)]
        print(f'🎉 {len(successful_bots)} bots joined successfully!')
        
        # Keep alive
        await asyncio.sleep(300)
        await browser.close()

asyncio.run(main())