import asyncio
from playwright.async_api import async_playwright

async def create_working_bot():
    async with async_playwright() as p:
        # Use more aggressive anti-detection flags
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
        
        # Set user agent to look more human
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        
        # Add extra headers
        await page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9"
        })
        
        try:
            print("🔄 Navigating to Meet...")
            await page.goto("https://meet.google.com/jzn-xoee-pvr", wait_until="domcontentloaded")
            
            # Wait longer for dynamic content
            await asyncio.sleep(5)
            
            print(f"📍 URL: {page.url}")
            print(f"📄 Title: {await page.title()}")
            
            # Check elements again
            inputs = await page.query_selector_all('input')
            buttons = await page.query_selector_all('button')
            print(f"🔍 Found {len(inputs)} inputs and {len(buttons)} buttons")
            
            # If still no inputs, try refreshing
            if len(inputs) == 0:
                print("🔄 No inputs found, trying refresh...")
                await page.reload(wait_until="domcontentloaded")
                await asyncio.sleep(3)
                
                inputs = await page.query_selector_all('input')
                buttons = await page.query_selector_all('button')
                print(f"🔍 After refresh: {len(inputs)} inputs and {len(buttons)} buttons")
            
            # Show button text for debugging
            if buttons:
                for i, btn in enumerate(buttons):
                    try:
                        text = await btn.inner_text()
                        print(f"  Button {i}: '{text.strip()}'")
                    except:
                        print(f"  Button {i}: [could not get text]")
            
            # Try to join if we find the right elements
            if len(inputs) > 0:
                await page.fill('input', 'WorkingBot')
                await page.click('text="Join now"')
                print("✅ Bot joined successfully!")
                await asyncio.sleep(30)
            else:
                print("❌ Still no input fields - Meet may be blocking automation")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

asyncio.run(create_working_bot())