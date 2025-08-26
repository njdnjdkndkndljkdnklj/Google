import asyncio
from playwright.async_api import async_playwright

async def test_single_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("🔄 Navigating to Google Meet...")
            await page.goto("https://meet.google.com/ptp-ahde-vxd")
            await page.wait_for_load_state('domcontentloaded')
            
            # Take screenshot to see current state
            await page.screenshot(path="meet_page.png")
            print("📸 Screenshot saved as meet_page.png")
            
            # Print page title and URL
            title = await page.title()
            url = page.url
            print(f"Page title: {title}")
            print(f"Current URL: {url}")
            
            # Wait and see what elements are available
            await asyncio.sleep(5)
            
            # Try to find name input
            print("🔍 Looking for name input field...")
            name_inputs = await page.query_selector_all('input')
            print(f"Found {len(name_inputs)} input elements")
            
            for i, input_elem in enumerate(name_inputs):
                placeholder = await input_elem.get_attribute('placeholder')
                aria_label = await input_elem.get_attribute('aria-label')
                input_type = await input_elem.get_attribute('type')
                print(f"Input {i}: type={input_type}, placeholder={placeholder}, aria-label={aria_label}")
            
            # Try to find buttons
            print("🔍 Looking for buttons...")
            buttons = await page.query_selector_all('button')
            print(f"Found {len(buttons)} button elements")
            
            for i, button in enumerate(buttons[:10]):  # Show first 10 buttons
                text = await button.inner_text()
                aria_label = await button.get_attribute('aria-label')
                print(f"Button {i}: text='{text}', aria-label={aria_label}")
            
            # Keep browser open for manual inspection
            print("Browser will stay open for 60 seconds for manual inspection...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_single_bot())