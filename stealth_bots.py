import asyncio
from playwright.async_api import async_playwright
import random

async def create_stealth_bot(context, name):
    try:
        page = await context.new_page()
        
        # Human-like navigation
        await page.goto("https://meet.google.com/oru-azsu-cmo")
        await asyncio.sleep(random.uniform(2, 5))
        
        # Human-like typing
        await page.type('input', name, delay=random.randint(50, 150))
        await asyncio.sleep(random.uniform(1, 3))
        
        # Human-like mouse movement and click
        buttons = await page.query_selector_all('button')
        if len(buttons) >= 4:
            box = await buttons[3].bounding_box()
            if box:
                await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=random.randint(10, 30))
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        
        await asyncio.sleep(random.uniform(2, 4))
        await page.type('textarea, input[placeholder*="message"]', f'{name} joined! 🙏', delay=random.randint(30, 100))
        await page.keyboard.press('Enter')
        
        print(f'✅ {name} joined with stealth')
        
        while True:
            await asyncio.sleep(300)
            
    except Exception as e:
        print(f'❌ {name}: {str(e)[:30]}')

async def main():
    names = ['Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 'Dipesh Shrestha']
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Visible browser
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--start-maximized",
                "--disable-web-security",
                "--user-data-dir=/tmp/chrome-user-data"
            ]
        )
        
        # Stealth context with realistic fingerprint
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        # Remove webdriver traces
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """)
        
        tasks = []
        for name in names:
            task = asyncio.create_task(create_stealth_bot(context, name))
            tasks.append(task)
            await asyncio.sleep(random.uniform(10, 20))  # Stagger launches
        
        await asyncio.gather(*tasks)

asyncio.run(main())