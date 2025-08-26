import asyncio
from playwright.async_api import async_playwright

async def debug_new_meet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("🔄 Navigating to new Meet link...")
            await page.goto("https://meet.google.com/jzn-xoee-pvr")
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(3)
            
            # Check page title and URL
            title = await page.title()
            url = page.url
            print(f"Title: {title}")
            print(f"URL: {url}")
            
            # Look for any input fields
            inputs = await page.query_selector_all('input')
            print(f"\nFound {len(inputs)} input elements:")
            for i, inp in enumerate(inputs):
                placeholder = await inp.get_attribute('placeholder')
                aria_label = await inp.get_attribute('aria-label')
                input_type = await inp.get_attribute('type')
                visible = await inp.is_visible()
                print(f"  Input {i}: type={input_type}, placeholder='{placeholder}', aria-label='{aria_label}', visible={visible}")
            
            # Look for buttons
            buttons = await page.query_selector_all('button')
            print(f"\nFound {len(buttons)} button elements:")
            for i, btn in enumerate(buttons[:15]):  # Show first 15
                text = await btn.inner_text()
                aria_label = await btn.get_attribute('aria-label')
                visible = await btn.is_visible()
                print(f"  Button {i}: text='{text.strip()}', aria-label='{aria_label}', visible={visible}")
            
            # Check if we need to accept cookies or terms
            cookie_buttons = await page.query_selector_all('button:has-text("Accept"), button:has-text("I agree"), button:has-text("Agree")')
            if cookie_buttons:
                print(f"\n🍪 Found {len(cookie_buttons)} cookie/consent buttons")
                for btn in cookie_buttons:
                    text = await btn.inner_text()
                    print(f"  Cookie button: '{text.strip()}'")
            
            # Take screenshot for manual inspection
            await page.screenshot(path="meet_debug.png")
            print("\n📸 Screenshot saved as meet_debug.png")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_new_meet())