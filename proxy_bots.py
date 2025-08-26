import asyncio
from playwright.async_api import async_playwright
import random

# Free proxy list (you can add more)
PROXIES = [
    None,  # No proxy
    {"server": "http://proxy1.example.com:8080"},
    {"server": "http://proxy2.example.com:8080"},
]

async def create_bot_with_proxy(p, name, proxy=None):
    try:
        browser = await p.chromium.launch(
            headless=True,
            proxy=proxy,
            args=["--no-sandbox", "--use-fake-device-for-media-stream"]
        )
        
        page = await browser.new_page()
        await page.goto("https://meet.google.com/jzn-xoee-pvr")
        await asyncio.sleep(3)
        
        await page.fill('input', name)
        buttons = await page.query_selector_all('button')
        if len(buttons) >= 4:
            await buttons[3].click()
        
        await asyncio.sleep(2)
        await page.keyboard.type(f'{name} joined!')
        await page.keyboard.press('Enter')
        
        print(f'✅ {name} joined')
        
        while True:
            await asyncio.sleep(300)
            
    except Exception as e:
        print(f'❌ {name}: {str(e)[:30]}')

async def main():
    names = [
        'Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 'Dipesh Shrestha',
        'Sunita Tamang', 'Bibek Karki', 'Mina Poudel', 'Kiran Adhikari', 'Gita Neupane'
    ]
    
    async with async_playwright() as p:
        tasks = []
        for i, name in enumerate(names):
            proxy = random.choice(PROXIES)
            task = asyncio.create_task(create_bot_with_proxy(p, name, proxy))
            tasks.append(task)
            await asyncio.sleep(5)
        
        await asyncio.gather(*tasks)

# Simple solution without proxies - just slower launch
async def simple_solution():
    names = ['Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa']
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        
        for name in names:
            try:
                page = await browser.new_page()
                await page.goto("https://meet.google.com/jzn-xoee-pvr")
                await asyncio.sleep(5)
                
                await page.fill('input', name)
                buttons = await page.query_selector_all('button')
                await buttons[3].click()
                
                print(f'✅ {name} joined')
                await asyncio.sleep(30)  # Wait 30 seconds between bots
                
            except Exception as e:
                print(f'❌ {name}: {str(e)[:30]}')

# Run the simple solution
asyncio.run(simple_solution())