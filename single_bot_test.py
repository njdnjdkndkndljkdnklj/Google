import asyncio
from playwright.async_api import async_playwright

async def test_single_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--use-fake-device-for-media-stream",
                "--use-fake-ui-for-media-stream",
                "--mute-audio"
            ]
        )
        
        page = await browser.new_page()
        
        try:
            print("🔄 Navigating to Meet...")
            await page.goto("https://meet.google.com/jzn-xoee-pvr")
            await page.wait_for_load_state('networkidle')
            
            print(f"📍 Current URL: {page.url}")
            print(f"📄 Page title: {await page.title()}")
            
            # Check what elements are available
            inputs = await page.query_selector_all('input')
            buttons = await page.query_selector_all('button')
            print(f"🔍 Found {len(inputs)} inputs and {len(buttons)} buttons")
            
            # Try to find and fill name field
            name_filled = False
            for selector in ['input[type="text"]', 'input[placeholder*="name"]', 'input']:
                try:
                    await page.fill(selector, 'TestBot')
                    print(f"✅ Name filled using: {selector}")
                    name_filled = True
                    break
                except:
                    continue
            
            if not name_filled:
                print("❌ Could not find name input field")
                # Show available buttons for debugging
                for i, btn in enumerate(buttons[:5]):
                    text = await btn.inner_text()
                    print(f"  Button {i}: '{text.strip()}'")
                return
            
            # Try to join
            joined = False
            for text in ['Join now', 'Ask to join', 'Join']:
                try:
                    await page.click(f'text="{text}"')
                    print(f"✅ Clicked: {text}")
                    joined = True
                    break
                except:
                    continue
            
            if joined:
                print("🎉 Bot joined successfully!")
                await asyncio.sleep(10)  # Stay for 10 seconds
            else:
                print("❌ Could not find join button")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

asyncio.run(test_single_bot())