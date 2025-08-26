import asyncio
from playwright.async_api import async_playwright

async def join_meet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        
        tasks = []
        for i in range(10):
            page = await browser.new_page()
            tasks.append(bot_task(page, f'Bot-{i+1}'))
        
        await asyncio.gather(*tasks)
        await browser.close()

async def bot_task(page, name):
    try:
        await page.goto('https://meet.google.com/jzn-xoee-pvr')
        
        # Wait for page load
        await page.wait_for_selector('input, button', timeout=10000)
        
        # Fill name if input exists
        inputs = await page.query_selector_all('input')
        if inputs:
            await inputs[0].fill(name)
        
        # Click any join-related button
        buttons = await page.query_selector_all('button')
        for btn in buttons:
            text = await btn.inner_text()
            if 'join' in text.lower() or 'ask' in text.lower():
                await btn.click()
                break
        
        print(f'✅ {name} attempted join')
        await asyncio.sleep(60)
        
    except Exception as e:
        print(f'❌ {name}: {str(e)[:30]}')

asyncio.run(join_meet())