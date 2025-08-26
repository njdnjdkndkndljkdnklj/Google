import asyncio
import requests
import random
from playwright.async_api import async_playwright

def get_unique_nepali_name(used_names):
    """Generate unique full Nepali names using Gemini API"""
    try:
        api_key = "AIzaSyDckVxNZfsyBmNoCfpJrGDaNMq9t-Pv7gw"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Generate one unique authentic full Nepali name with first name and last name. Just return the full name, nothing else."
                }]
            }]
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            name = result['candidates'][0]['content']['parts'][0]['text'].strip()
            if name not in used_names:
                return name
    except:
        pass
    
    # Extended fallback names
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
    
    # Add numbers if all names used
    base_name = random.choice(fallback_names)
    counter = 1
    while f"{base_name} {counter}" in used_names:
        counter += 1
    return f"{base_name} {counter}"

async def create_reliable_bot(browser, bot_name, bot_id, max_retries=3):
    """Create bot with retry mechanism to ensure 100% success"""
    for attempt in range(max_retries):
        try:
            page = await browser.new_page()
            
            # Navigate with longer timeout
            await page.goto("https://meet.google.com/jzn-xoee-pvr", 
                          wait_until="domcontentloaded", timeout=60000)
            
            # Wait for page to fully load
            await asyncio.sleep(5)
            
            # Fill name with retry
            name_filled = False
            for selector in ['input[type="text"]', 'input']:
                try:
                    await page.fill(selector, bot_name, timeout=10000)
                    name_filled = True
                    break
                except:
                    continue
            
            if not name_filled:
                raise Exception("Could not fill name")
            
            # Ensure mic/camera OFF
            try:
                await page.click('text="Continue without microphone and camera"', timeout=5000)
                await asyncio.sleep(1)
            except:
                pass
            
            # Join with retry
            joined = False
            for join_text in ['Join now', 'Ask to join']:
                try:
                    await page.click(f'text="{join_text}"', timeout=10000)
                    joined = True
                    break
                except:
                    continue
            
            if not joined:
                raise Exception("Could not click join")
            
            # Send message
            await asyncio.sleep(3)
            await page.keyboard.type(f'{bot_name} joined! 🙏')
            await page.keyboard.press('Enter')
            
            print(f'✅ Bot #{bot_id}: {bot_name} joined successfully (attempt {attempt+1})')
            
            # Stay forever
            while True:
                await asyncio.sleep(300)
            
        except Exception as e:
            print(f'⚠️  Bot #{bot_id}: {bot_name} attempt {attempt+1} failed: {str(e)[:40]}')
            try:
                await page.close()
            except:
                pass
            
            if attempt < max_retries - 1:
                await asyncio.sleep(5)  # Wait before retry
            else:
                print(f'❌ Bot #{bot_id}: {bot_name} FAILED after {max_retries} attempts')

async def launch_all_50_bots():
    async with async_playwright() as p:
        # Use multiple browser instances for better reliability
        browsers = []
        for i in range(5):  # 5 browsers, 10 bots each
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--use-fake-device-for-media-stream",
                    "--use-fake-ui-for-media-stream",
                    "--disable-web-security",
                    "--disable-dev-shm-usage"
                ]
            )
            browsers.append(browser)
        
        print('🔄 Generating 50 unique Nepali names...')
        
        # Generate 50 unique names
        used_names = set()
        nepali_names = []
        
        for i in range(50):
            name = get_unique_nepali_name(list(used_names))
            used_names.add(name)
            nepali_names.append(name)
            print(f'📝 {i+1}/50: {name}')
        
        print('🚀 Launching all 50 bots with retry mechanism...')
        
        # Distribute bots across browsers
        all_tasks = []
        for i, name in enumerate(nepali_names):
            browser_index = i % 5  # Distribute across 5 browsers
            browser = browsers[browser_index]
            task = asyncio.create_task(create_reliable_bot(browser, name, i+1))
            all_tasks.append(task)
            
            # Small delay between launches
            await asyncio.sleep(2)
        
        print('⚠️  All 50 bots launched with retry! They will stay until meeting ends')
        print('⚠️  Press Ctrl+C to stop all bots')
        
        try:
            await asyncio.gather(*all_tasks)
        except KeyboardInterrupt:
            print('\n👋 Stopping all bots...')
            for browser in browsers:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_all_50_bots())