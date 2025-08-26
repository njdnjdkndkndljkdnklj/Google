import asyncio
import requests
import random
from playwright.async_api import async_playwright

def get_unique_nepali_name(used_names):
    """Generate unique full Nepali names"""
    fallback_names = [
        'Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 'Dipesh Shrestha',
        'Sunita Tamang', 'Bibek Karki', 'Mina Poudel', 'Kiran Adhikari', 'Gita Neupane',
        'Ramesh Bhandari', 'Laxmi Ghimire', 'Suresh Pandey', 'Radha Koirala', 'Naresh Joshi',
        'Sarita Basnet', 'Mahesh Regmi', 'Purnima Dahal', 'Ganesh Khadka', 'Sabita Oli',
        'Umesh Gautam', 'Bishnu Aryal', 'Shanti Bhattarai', 'Ramhari Subedi', 'Devi Chaudhary',
        'Surya Magar', 'Indira Limbu', 'Hari Sherpa', 'Kamana Thakuri', 'Rajan Yadav',
        'Nirmala Chhetri', 'Deepak Rijal', 'Sangita Kc', 'Mohan Sapkota', 'Geeta Mainali',
        'Ashok Pokhrel', 'Sundar Acharya', 'Rama Devkota', 'Tek Bahadur', 'Sushila Dhakal',
        'Binod Kafle', 'Saraswoti Upreti', 'Tilak Bhusal', 'Durga Lamichhane', 'Ravi Pandey',
        'Shova Maharjan', 'Dinesh Khatri', 'Parbati Silwal', 'Gopal Humagain', 'Kamala Bhatta',
        'Krishna Bahadur', 'Sushma Karki', 'Arjun Thapa', 'Bimala Rai', 'Santosh Gurung'
    ]
    
    for name in fallback_names:
        if name not in used_names:
            return name
    
    # Add numbers if needed
    base_name = random.choice(fallback_names)
    counter = 1
    while f"{base_name} {counter}" in used_names:
        counter += 1
    return f"{base_name} {counter}"

async def create_guaranteed_bot(browser, bot_name, bot_id):
    """Create bot that WILL join - keeps trying until success"""
    attempt = 0
    while True:
        attempt += 1
        try:
            page = await browser.new_page()
            
            # Use the working browser flags we discovered
            await page.goto("https://meet.google.com/jzn-xoee-pvr", 
                          wait_until="domcontentloaded", timeout=60000)
            
            # Wait for page to load
            await asyncio.sleep(8)
            
            # Check if we have the right page (with input field)
            inputs = await page.query_selector_all('input')
            buttons = await page.query_selector_all('button')
            
            print(f'🔍 Bot #{bot_id} attempt {attempt}: Found {len(inputs)} inputs, {len(buttons)} buttons')
            
            if len(inputs) == 0:
                # We're on error page, close and retry
                await page.close()
                print(f'⚠️  Bot #{bot_id}: Error page detected, retrying in 10 seconds...')
                await asyncio.sleep(10)
                continue
            
            # We have input field! Fill name
            await page.fill('input', bot_name)
            
            # Handle mic/camera
            try:
                await page.click('text="Continue without microphone and camera"')
                await asyncio.sleep(1)
            except:
                pass
            
            # Join meeting
            await page.click('text="Join now"')
            
            # Send message
            await asyncio.sleep(3)
            await page.keyboard.type(f'{bot_name} joined! 🙏')
            await page.keyboard.press('Enter')
            
            print(f'✅ Bot #{bot_id}: {bot_name} SUCCESSFULLY joined (attempt {attempt})')
            
            # Stay forever
            while True:
                await asyncio.sleep(300)
            
        except Exception as e:
            print(f'⚠️  Bot #{bot_id}: Attempt {attempt} failed: {str(e)[:40]}')
            try:
                await page.close()
            except:
                pass
            
            # Wait longer between retries to avoid rate limiting
            wait_time = min(30, attempt * 5)
            print(f'⏳ Bot #{bot_id}: Waiting {wait_time}s before retry...')
            await asyncio.sleep(wait_time)

async def launch_guaranteed_50():
    async with async_playwright() as p:
        # Use the exact browser config that worked before
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=VizDisplayCompositor",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--allow-running-insecure-content",
                "--disable-web-security",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection"
            ]
        )
        
        print('📝 Generating 50 unique Nepali names...')
        
        # Generate names
        used_names = set()
        nepali_names = []
        
        for i in range(50):
            name = get_unique_nepali_name(list(used_names))
            used_names.add(name)
            nepali_names.append(name)
            print(f'{i+1}/50: {name}')
        
        print('🚀 Launching 50 GUARANTEED bots (they will keep retrying until success)...')
        print('⚠️  Each bot will retry until it joins - this may take time but ALL will join!')
        
        # Launch all bots with very slow stagger
        tasks = []
        for i, name in enumerate(nepali_names):
            task = asyncio.create_task(create_guaranteed_bot(browser, name, i+1))
            tasks.append(task)
            
            # Slow stagger to avoid overwhelming
            await asyncio.sleep(5)
        
        print('⚠️  All bots launched! They will retry until ALL 50 join successfully')
        print('⚠️  Press Ctrl+C to stop')
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print('\n👋 Stopping all bots...')
            await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_guaranteed_50())