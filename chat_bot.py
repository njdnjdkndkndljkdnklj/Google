import asyncio
from playwright.async_api import async_playwright

async def join_and_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        
        tasks = []
        for i in range(10):
            page = await browser.new_page()
            tasks.append(bot_with_chat(page, f'Bot-{i+1}'))
        
        await asyncio.gather(*tasks)
        await browser.close()

async def bot_with_chat(page, name):
    try:
        await page.goto('https://meet.google.com/jzn-xoee-pvr')
        await page.wait_for_selector('input, button', timeout=10000)
        
        # Fill name
        inputs = await page.query_selector_all('input')
        if inputs:
            await inputs[0].fill(name)
        
        # Join
        buttons = await page.query_selector_all('button')
        for btn in buttons:
            text = await btn.inner_text()
            if 'join' in text.lower():
                await btn.click()
                break
        
        await asyncio.sleep(3)
        
        # Send chat message
        try:
            # Click chat button
            await page.click('[aria-label*="chat" i], [data-tooltip*="chat" i]')
            await asyncio.sleep(1)
            
            # Type message
            chat_input = page.locator('textarea, input[placeholder*="message" i]')
            await chat_input.fill(f'{name} has joined the meeting!')
            
            # Send message
            await page.keyboard.press('Enter')
            print(f'✅ {name} joined and sent message')
            
        except:
            print(f'✅ {name} joined (no chat)')
        
        await asyncio.sleep(300)
        
    except Exception as e:
        print(f'❌ {name}: {str(e)[:30]}')

asyncio.run(join_and_chat())