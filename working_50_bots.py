import asyncio
from playwright.async_api import async_playwright

async def create_bot(context, name):
    try:
        page = await context.new_page()
        await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Fill name
        await page.fill('input', name)
        
        # Click join button by position (button 3 from our earlier discovery)
        buttons = await page.query_selector_all('button')
        if len(buttons) >= 4:
            await buttons[3].click()  # "Join now" was button 3
        
        await asyncio.sleep(2)
        await page.keyboard.type(f'{name} joined! 🙏')
        await page.keyboard.press('Enter')
        
        print(f'✅ {name} joined successfully')
        
        # Stay forever
        while True:
            await asyncio.sleep(300)
            
    except Exception as e:
        print(f'❌ {name}: {str(e)[:40]}')

async def main():
    names = [
        'Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 'Dipesh Shrestha',
        'Sunita Tamang', 'Bibek Karki', 'Mina Poudel', 'Kiran Adhikari', 'Gita Neupane',
        'Ramesh Bhandari', 'Laxmi Ghimire', 'Suresh Pandey', 'Radha Koirala', 'Naresh Joshi',
        'Sarita Basnet', 'Mahesh Regmi', 'Purnima Dahal', 'Ganesh Khadka', 'Sabita Oli',
        'Umesh Gautam', 'Bishnu Aryal', 'Shanti Bhattarai', 'Ramhari Subedi', 'Devi Chaudhary',
        'Surya Magar', 'Indira Limbu', 'Hari Sherpa', 'Kamana Thakuri', 'Rajan Yadav',
        'Nirmala Chhetri', 'Deepak Rijal', 'Sangita Kc', 'Mohan Sapkota', 'Geeta Mainali',
        'Ashok Pokhrel', 'Sundar Acharya', 'Rama Devkota', 'Tek Bahadur', 'Sushila Dhakal',
        'Binod Kafle', 'Saraswoti Upreti', 'Tilak Bhusal', 'Durga Lamichhane', 'Ravi Pandey',
        'Shova Maharjan', 'Dinesh Khatri', 'Parbati Silwal', 'Gopal Humagain', 'Kamala Bhatta'
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=VizDisplayCompositor",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--disable-web-security"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        print('🚀 Launching 50 Nepali bots...')
        
        tasks = []
        for name in names:
            task = asyncio.create_task(create_bot(context, name))
            tasks.append(task)
            await asyncio.sleep(1)  # 1 second between each bot
        
        print('⚠️ All 50 bots launched! Press Ctrl+C to stop')
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            await browser.close()

asyncio.run(main())