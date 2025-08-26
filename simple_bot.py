import asyncio
from playwright.async_api import async_playwright

async def join_bot(name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--use-fake-ui-for-media-stream"])
        page = await browser.new_page()
        
        await page.goto("https://meet.google.com/jzn-xoee-pvr")
        await asyncio.sleep(3)
        
        # Fill name
        try:
            await page.fill('input[type="text"]', name)
        except:
            pass
            
        # Click join
        try:
            await page.click('text="Join now"')
        except:
            try:
                await page.click('text="Ask to join"')
            except:
                await page.click('button:has-text("Join")')
        
        print(f"✅ {name} joined")
        await asyncio.sleep(300)  # Stay 5 minutes
        await browser.close()

async def main():
    tasks = []
    for i in range(10):
        tasks.append(join_bot(f"Bot-{i+1}"))
        await asyncio.sleep(2)
    await asyncio.gather(*tasks)

asyncio.run(main())