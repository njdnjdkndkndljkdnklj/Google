import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=VizDisplayCompositor"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        await context.add_init_script("""
            delete navigator.__proto__.webdriver;
            navigator.webdriver = false;
            window.chrome = {runtime: {}};
        """)
        
        # Launch ONE bot that works
        page = await context.new_page()
        await page.goto("https://meet.google.com/oru-azsu-cmo")
        await asyncio.sleep(3)
        
        await page.fill('input', 'Rajesh Sharma')
        
        buttons = await page.query_selector_all('button')
        for btn in buttons:
            try:
                text = await btn.inner_text()
                if 'join' in text.lower():
                    await btn.click()
                    break
            except:
                continue
        
        await asyncio.sleep(2)
        await page.keyboard.type('Rajesh Sharma joined! 🙏')
        await page.keyboard.press('Enter')
        
        print('✅ Single bot joined successfully!')
        print('🔄 To get 50 bots: Run this script 50 times from different IPs/servers')
        
        # Stay in meeting
        while True:
            await asyncio.sleep(300)

asyncio.run(main())