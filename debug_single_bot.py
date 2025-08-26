import asyncio
from playwright.async_api import async_playwright

async def debug_meet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Show browser window
            args=["--no-sandbox", "--use-fake-device-for-media-stream"]
        )
        
        page = await browser.new_page()
        
        try:
            print("🔄 Opening Meet link...")
            await page.goto("https://meet.google.com/jzn-xoee-pvr")
            await asyncio.sleep(5)
            
            # Check what we actually see
            title = await page.title()
            url = page.url
            print(f"📄 Title: {title}")
            print(f"🔗 URL: {url}")
            
            # Check for different types of inputs
            text_inputs = await page.query_selector_all('input[type="text"]')
            email_inputs = await page.query_selector_all('input[type="email"]')
            all_inputs = await page.query_selector_all('input')
            buttons = await page.query_selector_all('button')
            
            print(f"📝 Text inputs: {len(text_inputs)}")
            print(f"📧 Email inputs: {len(email_inputs)}")
            print(f"📋 All inputs: {len(all_inputs)}")
            print(f"🔘 Buttons: {len(buttons)}")
            
            # Show button text
            for i, btn in enumerate(buttons[:10]):
                try:
                    text = await btn.inner_text()
                    print(f"  Button {i}: '{text.strip()}'")
                except:
                    print(f"  Button {i}: [no text]")
            
            # Check for sign-in indicators
            page_content = await page.content()
            if "sign in" in page_content.lower() or "login" in page_content.lower():
                print("⚠️  LOGIN REQUIRED - Guest join disabled!")
            elif len(text_inputs) > 0:
                print("✅ Guest name input found - should work")
            else:
                print("❓ Unknown page state")
            
            # Keep browser open for manual inspection
            print("🔍 Browser will stay open for 60 seconds for inspection...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

asyncio.run(debug_meet())