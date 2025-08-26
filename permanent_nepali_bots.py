import asyncio
import requests
import random
from playwright.async_api import async_playwright

def get_full_nepali_name():
    """Generate full Nepali names (first + last) using Gemini API"""
    try:
        api_key = "AIzaSyDckVxNZfsyBmNoCfpJrGDaNMq9t-Pv7gw"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Generate one authentic full Nepali name with first name and last name (like 'Rajesh Sharma' or 'Sita Gurung'). Just return the full name, nothing else."
                }]
            }]
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            name = result['candidates'][0]['content']['parts'][0]['text'].strip()
            return name
        else:
            # Fallback full Nepali names
            fallback_names = [
                'Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 
                'Dipesh Shrestha', 'Sunita Tamang', 'Bibek Karki', 'Mina Poudel',
                'Kiran Adhikari', 'Gita Neupane'
            ]
            return random.choice(fallback_names)
    except:
        fallback_names = [
            'Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 
            'Dipesh Shrestha', 'Sunita Tamang', 'Bibek Karki', 'Mina Poudel',
            'Kiran Adhikari', 'Gita Neupane'
        ]
        return random.choice(fallback_names)

async def create_permanent_bot(browser_context, bot_name):
    try:
        page = await browser_context.new_page()
        
        # Navigate to Meet
        await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Fill full Nepali name
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
        
        print(f'✅ {bot_name} joined and will stay permanently')
        
        # Stay FOREVER - never leave until browser closes
        while True:
            await asyncio.sleep(60)  # Check every minute but never leave
        
    except Exception as e:
        print(f'❌ {bot_name} failed: {str(e)[:50]}')

async def launch_permanent_nepali_bots():
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
        
        print('🔄 Generating full Nepali names using Gemini API...')
        
        # Generate 10 unique full Nepali names
        nepali_names = []
        for i in range(10):
            name = get_full_nepali_name()
            nepali_names.append(name)
            print(f'📝 Generated: {name}')
        
        # Create permanent bots
        tasks = []
        for name in nepali_names:
            task = asyncio.create_task(create_permanent_bot(context, name))
            tasks.append(task)
        
        print('🚀 Launching 10 permanent Nepali bots...')
        print('⚠️  Bots will NEVER leave - they stay until meeting ends naturally')
        print('⚠️  Press Ctrl+C to stop all bots')
        
        # Run forever until manually stopped
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print('\n👋 Stopping all bots...')
            await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_permanent_nepali_bots())