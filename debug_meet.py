import asyncio
from playwright.async_api import async_playwright

async def debug_meet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("🔄 Navigating to Google Meet...")
            await page.goto("https://meet.google.com/ptp-ahde-vxd")
            await page.wait_for_load_state('domcontentloaded')
            
            # Take screenshot
            await page.screenshot(path="debug_meet.png")
            print("📸 Screenshot saved as debug_meet.png")
            
            # Get page content
            title = await page.title()
            url = page.url
            content = await page.content()
            
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Content length: {len(content)} characters")
            
            # Check if meeting exists
            if "not found" in content.lower() or "invalid" in content.lower():
                print("❌ Meeting appears to be invalid or not found")
            elif "join" in content.lower():
                print("✅ Meeting page loaded, join options should be available")
            else:
                print("⚠️ Unclear meeting status")
            
            # Print first 500 chars of content for debugging
            print("\nFirst 500 characters of page content:")
            print(content[:500])
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_meet())