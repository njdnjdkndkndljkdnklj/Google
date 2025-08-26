import asyncio
import random
import string
from playwright.async_api import async_playwright

def generate_human_name():
    """Generate realistic human-like names"""
    names = ['Alex', 'Sam', 'Jordan', 'Casey', 'Taylor', 'Morgan', 'Riley', 'Avery', 'Quinn', 'Blake']
    suffix = ''.join(random.choices(string.digits, k=2))
    return f"{random.choice(names)}-{suffix}"

async def create_human_bot(browser, meet_url, bot_name):
    try:
        page = await browser.new_page()
        
        # Navigate to Meet
        await page.goto(meet_url)
        await page.wait_for_load_state('networkidle')
        
        # Handle consent popup
        try:
            await page.click("button:has-text('I agree')", timeout=2000)
        except:
            pass
        
        # Human-like pause (reading the page)
        await asyncio.sleep(random.uniform(1, 3))
        
        # Fill name
        await page.fill('input[type="text"]', bot_name)
        
        # Turn OFF mic and camera (human behavior)
        await page.keyboard.press("Control+d")  # mute mic
        await page.keyboard.press("Control+e")  # turn off camera
        
        # Small pause before joining
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Join meeting
        await page.click('text="Join now"')
        
        # Wait a bit then send join message
        await asyncio.sleep(random.uniform(2, 4))
        await page.keyboard.type(f'{bot_name} has joined!')
        await page.keyboard.press('Enter')
        
        print(f'✅ {bot_name} joined with mic/camera OFF')
        
        # Stay for random duration (5-10 minutes)
        stay_time = random.randint(300, 600)
        await asyncio.sleep(stay_time)
        
        await page.close()
        print(f'👋 {bot_name} left after {stay_time//60} minutes')
        
    except Exception as e:
        print(f'❌ {bot_name} failed: {str(e)[:40]}')

async def join_simultaneous_bots(meet_url, num_bots):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream", 
                "--mute-audio",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        # Create all bot tasks simultaneously
        tasks = []
        for i in range(num_bots):
            bot_name = generate_human_name()
            task = asyncio.create_task(create_human_bot(browser, meet_url, bot_name))
            tasks.append(task)
        
        print(f'🚀 Launching {num_bots} bots simultaneously...')
        
        # All bots join at the same time
        await asyncio.gather(*tasks, return_exceptions=True)
        
        await browser.close()
        print('🎉 All bots completed!')

# Run the enhanced bot system
if __name__ == "__main__":
    meet_url = "https://meet.google.com/jzn-xoee-pvr"
    num_bots = 10
    
    asyncio.run(join_simultaneous_bots(meet_url, num_bots))