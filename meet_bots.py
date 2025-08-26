import asyncio
import os
from playwright.async_api import async_playwright

async def create_bot(context, name):
    try:
        page = await context.new_page()
        await page.goto(os.getenv('MEET_URL', 'https://meet.google.com/oru-azsu-cmo'))
        await asyncio.sleep(3)
        
        await page.fill('input', name)
        buttons = await page.query_selector_all('button')
        if len(buttons) >= 4:
            await buttons[3].click()
        
        await asyncio.sleep(2)
        await page.keyboard.type(f'{name} joined! 🙏')
        await page.keyboard.press('Enter')
        
        print(f'✅ {name} joined')
        
        while True:
            await asyncio.sleep(300)
            
    except Exception as e:
        print(f'❌ {name}: {str(e)[:30]}')

async def main():
    names = [
        'Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 'Dipesh Shrestha',
        'Sunita Tamang', 'Bibek Karki', 'Mina Poudel', 'Kiran Adhikari', 'Gita Neupane',
        'Ramesh Bhandari', 'Laxmi Ghimire', 'Suresh Pandey', 'Radha Koirala', 'Naresh Joshi',
        'Sarita Basnet', 'Mahesh Regmi', 'Purnima Dahal', 'Ganesh Khadka', 'Sabita Oli',
        'Umesh Gautam', 'Bishnu Aryal', 'Shanti Bhattarai', 'Ramhari Subedi', 'Devi Chaudhary',
        'Surya Magar', 'Indira Limbu', 'Hari Sherpa', 'Kamana Thakuri', 'Rajan Yadav',
        'Nirmala Chhetri', 'Deepak Rijal', 'Sangita Kc', 'Mohan Sapkota', 'Geeta Mainali',
        'Ashok Pokhrel', 'Sundar Acharya', 'Rama Devkota', 'Tek Bahadur', 'Sushila Dhakal',
        'Binod Kafle', 'Saraswoti Upreti', 'Tilak Bhusal', 'Durga Lamichhane', 'Ravi Pandey',
        'Shova Maharjan', 'Dinesh Khatri', 'Parbati Silwal', 'Gopal Humagain', 'Kamala Bhatta'
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        print('🚀 Launching 50 Nepali bots...')
        
        tasks = []
        for name in names:
            task = asyncio.create_task(create_bot(context, name))
            tasks.append(task)
            await asyncio.sleep(2)
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())