import asyncio
import requests
import random
from playwright.async_api import async_playwright

def get_unique_nepali_name(used_names):
    """Generate unique full Nepali names using Gemini API"""
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            api_key = "AIzaSyDckVxNZfsyBmNoCfpJrGDaNMq9t-Pv7gw"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Generate one unique authentic full Nepali name with first name and last name. Make it different from these names: {', '.join(used_names[-10:])}. Just return the full name, nothing else."
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
    
    # Fallback with unique names
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
        'Shova Maharjan', 'Dinesh Khatri', 'Parbati Silwal', 'Gopal Humagain', 'Kamala Bhatta'
    ]
    
    for name in fallback_names:
        if name not in used_names:
            return name
    
    # If all fallback names used, add numbers
    base_name = random.choice(fallback_names)
    counter = 1
    while f"{base_name} {counter}" in used_names:
        counter += 1
    return f"{base_name} {counter}"

async def create_permanent_bot(browser_context, bot_name, bot_id):
    try:
        page = await browser_context.new_page()
        
        # Navigate to Meet
        await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Fill unique Nepali name
        await page.fill('input', bot_name)
        
        # Ensure mic/camera OFF
        try:
            await page.click('text="Continue without microphone and camera"')
            await asyncio.sleep(1)
        except:
            pass
        
        # Join meeting
        await page.click('text="Join now"')
        
        # Send join message
        await asyncio.sleep(3)
        await page.keyboard.type(f'{bot_name} joined! Namaste 🙏')
        await page.keyboard.press('Enter')
        
        print(f'✅ Bot #{bot_id}: {bot_name} joined permanently')
        
        # Stay FOREVER
        while True:
            await asyncio.sleep(60)
        
    except Exception as e:
        print(f'❌ Bot #{bot_id}: {bot_name} failed: {str(e)[:50]}')

async def launch_50_unique_bots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--disable-web-security"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        print('🔄 Generating 50 unique Nepali names using Gemini API...')
        
        # Generate 50 unique names
        used_names = set()
        nepali_names = []
        
        for i in range(50):
            name = get_unique_nepali_name(list(used_names))
            used_names.add(name)
            nepali_names.append(name)
            print(f'📝 {i+1}/50: {name}')
        
        # Create 50 permanent bots
        tasks = []
        for i, name in enumerate(nepali_names, 1):
            task = asyncio.create_task(create_permanent_bot(context, name, i))
            tasks.append(task)
        
        print('🚀 Launching 50 unique Nepali bots simultaneously...')
        print('⚠️  All bots will stay until meeting ends naturally')
        print('⚠️  Press Ctrl+C to stop all bots')
        
        # Run forever until manually stopped
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print('\n👋 Stopping all 50 bots...')
            await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_50_unique_bots())