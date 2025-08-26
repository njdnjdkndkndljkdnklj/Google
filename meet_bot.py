import asyncio
from playwright.async_api import async_playwright
import random

async def join_meet_bot(meet_url, bot_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Changed to visible for debugging
        page = await browser.new_page()
        
        try:
            print(f"🔄 {bot_name} navigating to meet...")
            await page.goto(meet_url, wait_until='domcontentloaded')
            await asyncio.sleep(3)
            
            # Wait for and fill name field - multiple possible selectors
            print(f"🔄 {bot_name} filling name...")
            name_selectors = [
                'input[placeholder*="name" i]',
                'input[aria-label*="name" i]', 
                'input[type="text"]',
                '[data-testid="name-input"]',
                '.VfPpkd-fmcmS-wGMbrd'
            ]
            
            name_filled = False
            for selector in name_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.fill(selector, bot_name)
                    name_filled = True
                    break
                except:
                    continue
            
            if not name_filled:
                print(f"❌ {bot_name} couldn't find name field")
                return
            
            # Turn off camera and mic before joining
            print(f"🔄 {bot_name} disabling camera/mic...")
            camera_selectors = ['[data-testid="camera-button"]', '[aria-label*="camera" i]', '[aria-label*="Turn off camera" i]']
            mic_selectors = ['[data-testid="mic-button"]', '[aria-label*="microphone" i]', '[aria-label*="Turn off microphone" i]']
            
            for selector in camera_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=3000)
                    if element:
                        await element.click()
                        break
                except:
                    continue
                    
            for selector in mic_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=3000)
                    if element:
                        await element.click()
                        break
                except:
                    continue
            
            # Join meeting - multiple possible selectors
            print(f"🔄 {bot_name} attempting to join...")
            join_selectors = [
                'text="Join now"',
                'text="Ask to join"', 
                '[data-testid="join-button"]',
                'button:has-text("Join")',
                '.VfPpkd-LgbsSe'
            ]
            
            joined = False
            for selector in join_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=5000)
                    if element:
                        await element.click()
                        joined = True
                        break
                except:
                    continue
            
            if not joined:
                print(f"❌ {bot_name} couldn't find join button")
                return
                
            print(f"✅ {bot_name} joined successfully")
            
            # Stay in meeting
            while True:
                try:
                    # Check if still in meeting by looking for leave button or meeting UI
                    meeting_indicators = [
                        '[aria-label*="Leave call"]',
                        '[data-testid="leave-button"]', 
                        '.google-material-icons:has-text("call_end")',
                        '[aria-label*="End call"]'
                    ]
                    
                    found_indicator = False
                    for indicator in meeting_indicators:
                        try:
                            await page.wait_for_selector(indicator, timeout=10000)
                            found_indicator = True
                            break
                        except:
                            continue
                    
                    if not found_indicator:
                        print(f"❌ {bot_name} lost meeting connection")
                        break
                        
                    await asyncio.sleep(30)
                except Exception as e:
                    print(f"❌ {bot_name} disconnected: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ {bot_name} failed: {e}")
        finally:
            await browser.close()

async def spawn_bots(meet_url, num_bots):
    tasks = []
    for i in range(1, num_bots + 1):
        bot_name = f"Bot-{i}"
        task = asyncio.create_task(join_meet_bot(meet_url, bot_name))
        tasks.append(task)
        await asyncio.sleep(5)  # Longer stagger to avoid rate limiting
    
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    meet_url = "https://meet.google.com/ptp-ahde-vxd"
    num_bots = 10
    
    print(f"🚀 Spawning {num_bots} bots for: {meet_url}")
    asyncio.run(spawn_bots(meet_url, num_bots))