import asyncio
from playwright.async_api import async_playwright
import random

async def create_working_bot(context, name):
    try:
        page = await context.new_page()
        await page.goto("https://meet.google.com/oru-azsu-cmo")
        await asyncio.sleep(3)
        
        await page.type('input', name, delay=50)
        await asyncio.sleep(1)
        
        # Try different join button approaches
        try:
            await page.click('text="Join now"', timeout=5000)
        except:
            try:
                await page.click('[aria-label*="Join"]', timeout=5000)
            except:
                buttons = await page.query_selector_all('button')
                for i, btn in enumerate(buttons):
                    text = await btn.inner_text()
                    if 'join' in text.lower():
                        await btn.click()
                        break
        
        await asyncio.sleep(2)
        await page.keyboard.type(f'{name} joined! 🙏')
        await page.keyboard.press('Enter')
        
        print(f'✅ {name} joined successfully')
        
        while True:
            await asyncio.sleep(300)
            
    except Exception as e:
        print(f'❌ {name}: {str(e)[:30]}')

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
                "--disable-features=VizDisplayCompositor"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        await context.add_init_script("""
            delete navigator.__proto__.webdriver;
            navigator.webdriver = false;
            window.chrome = {runtime: {}};
        """)
        
        print('🚀 Launching 50 stealth Nepali bots...')
        
        tasks = []
        for name in names:
            task = asyncio.create_task(create_working_bot(context, name))
            tasks.append(task)
            await asyncio.sleep(3)  # Stagger launches
        
        await asyncio.gather(*tasks)

asyncio.run(main())