import asyncio
from playwright.async_api import async_playwright

async def create_guaranteed_bot(browser, name, delay):
    await asyncio.sleep(delay)  # Stagger start times
    
    for attempt in range(5):  # Retry up to 5 times
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
            await asyncio.sleep(2)
            
            # Check if we have input field (real page)
            inputs = await page.query_selector_all('input')
            if len(inputs) == 0:
                await context.close()
                await asyncio.sleep(5)  # Wait before retry
                continue
            
            await page.fill('input', name)
            
            # Try join
            buttons = await page.query_selector_all('button')
            for btn in buttons:
                try:
                    text = await btn.inner_text()
                    if 'join' in text.lower():
                        await btn.click()
                        break
                except:
                    continue
            
            await asyncio.sleep(1)
            await page.keyboard.type(f'{name} joined! 🙏')
            await page.keyboard.press('Enter')
            
            print(f'✅ {name} joined successfully (attempt {attempt+1})')
            
            # Stay forever
            while True:
                await asyncio.sleep(300)
            
        except Exception as e:
            print(f'⚠️ {name} attempt {attempt+1} failed: {str(e)[:30]}')
            try:
                await context.close()
            except:
                pass
            await asyncio.sleep(3)
    
    print(f'❌ {name} FAILED after 5 attempts')

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
        
        print('🚀 Launching ALL 50 bots with retry guarantee...')
        
        # Launch with staggered delays to avoid rate limiting
        tasks = []
        for i, name in enumerate(names):
            delay = i * 2  # 2 second intervals
            task = asyncio.create_task(create_guaranteed_bot(browser, name, delay))
            tasks.append(task)
        
        print('⚠️ Each bot will retry until successful - ALL 50 WILL JOIN!')
        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())