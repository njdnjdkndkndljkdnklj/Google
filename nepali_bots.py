import asyncio
import requests
import random
from playwright.async_api import async_playwright

def get_nepali_name():
    """Generate perfect Nepali names using Gemini API"""
    try:
        api_key = "AIzaSyDckVxNZfsyBmNoCfpJrGDaNMq9t-Pv7gw"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Generate one authentic Nepali name (first name only). Just return the name, nothing else."
                }]
            }]
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            name = result['candidates'][0]['content']['parts'][0]['text'].strip()
            return name
        else:
            # Fallback names if API fails
            fallback_names = ['Aarav', 'Anish', 'Bibek', 'Dipesh', 'Kiran', 'Manish', 'Nischal', 'Prakash', 'Rajesh', 'Suman']
            return random.choice(fallback_names)
    except:
        fallback_names = ['Aarav', 'Anish', 'Bibek', 'Dipesh', 'Kiran', 'Manish', 'Nischal', 'Prakash', 'Rajesh', 'Suman']
        return random.choice(fallback_names)

async def create_nepali_bot(browser_context, bot_name):
    try:
        page = await browser_context.new_page()
        
        # Navigate to Meet
        await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Fill Nepali name
        await page.fill('input', bot_name)
        
        # Ensure mic/camera OFF
        try:
            await page.click('text="Continue without microphone and camera"')
            await asyncio.sleep(1)
        except:
            pass
        
        # Join meeting
        await page.click('text="Join now"')
        
        # Send join message in Nepali style
        await asyncio.sleep(3)
        await page.keyboard.type(f'{bot_name} joined! Namaste 🙏')
        await page.keyboard.press('Enter')
        
        print(f'✅ {bot_name} joined successfully')
        
        # Stay until meeting ends (check every 30 seconds)
        while True:
            try:
                # Check if still in meeting by looking for meeting UI elements
                meeting_active = await page.query_selector('[aria-label*="Leave call"], [data-tooltip*="Leave"], button:has-text("Leave")')
                if not meeting_active:
                    print(f'📞 {bot_name} - Meeting ended, leaving...')
                    break
                await asyncio.sleep(30)
            except:
                print(f'❌ {bot_name} - Connection lost')
                break
        
        await page.close()
        return True
        
    except Exception as e:
        print(f'❌ {bot_name} failed: {str(e)[:50]}')
        return False

async def launch_nepali_bots():
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
        
        print('🔄 Generating Nepali names using Gemini API...')
        
        # Generate 10 unique Nepali names
        nepali_names = []
        for i in range(10):
            name = get_nepali_name()
            nepali_names.append(name)
            print(f'📝 Generated: {name}')
        
        # Create bots with Nepali names
        tasks = []
        for name in nepali_names:
            task = asyncio.create_task(create_nepali_bot(context, name))
            tasks.append(task)
        
        print('🚀 Launching 10 Nepali bots simultaneously...')
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_count = sum(1 for r in results if r is True)
        print(f'🎉 {successful_count} Nepali bots joined successfully!')
        print('⏰ Bots will stay until meeting ends...')
        
        # Wait for all bots to finish (when meeting ends)
        await asyncio.sleep(10)  # Small delay before closing browser
        await browser.close()
        print('👋 All Nepali bots have left - Meeting ended!')

if __name__ == "__main__":
    asyncio.run(launch_nepali_bots())