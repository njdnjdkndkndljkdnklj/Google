import asyncio
from playwright.async_api import async_playwright

async def create_fast_bot(browser, name):
    try:
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        await context.add_init_script("""
            delete navigator.__proto__.webdriver;
            navigator.webdriver = false;
            window.chrome = {runtime: {}};
        """)
        
        page = await context.new_page()
        await page.goto("https://meet.google.com/oru-azsu-cmo")
        await asyncio.sleep(1)
        
        await page.fill('input', name)
        
        # Fast join - try multiple selectors simultaneously
        try:
            await page.click('text="Join now"', timeout=3000)
        except:
            buttons = await page.query_selector_all('button')
            for btn in buttons:
                try:
                    text = await btn.inner_text()
                    if 'join' in text.lower():
                        await btn.click()
                        break
                except:
                    continue
        
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
        
        print('🚀 Launching ALL 50 bots FAST...')
        
        # Launch all bots simultaneously with minimal delay
        tasks = []
        for name in names:
            task = asyncio.create_task(create_fast_bot(browser, name))
            tasks.append(task)
            await asyncio.sleep(0.1)  # Minimal delay
        
        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())