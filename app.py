from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import asyncio
import subprocess
import threading
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_bots')
def handle_run_bots(data):
    meet_url = data['meet_url']
    bot_count = int(data['bot_count'])
    
    def run_bots():
        try:
            # Create bot script with user parameters
            script = f"""
import asyncio
from playwright.async_api import async_playwright
import random

async def create_bot(browser, name):
    try:
        context = await browser.new_context(
            viewport={{'width': random.randint(1200, 1920), 'height': random.randint(800, 1080)}},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        await context.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
            Object.defineProperty(navigator, 'plugins', {{get: () => [1, 2, 3, 4, 5]}});
            window.chrome = {{runtime: {{}}}};
        ''')
        
        page = await context.new_page()
        await page.goto("{meet_url}")
        await asyncio.sleep(1)
        
        inputs = await page.query_selector_all('input')
        if len(inputs) == 0:
            print(f'⚠️ {{name}}: Error page detected')
            return
        
        await page.fill('input', name)
        await asyncio.sleep(0.5)
        
        buttons = await page.query_selector_all('button')
        for btn in buttons:
            try:
                text = await btn.inner_text()
                if 'join' in text.lower():
                    box = await btn.bounding_box()
                    await btn.click()
                    break
            except:
                continue
        
        await asyncio.sleep(0.5)
        await page.keyboard.type(f'{{name}} joined! 🙏')
        await page.keyboard.press('Enter')
        
        print(f'✅ {{name}} joined successfully')
        
        while True:
            await asyncio.sleep(300)
            
    except Exception as e:
        print(f'❌ {{name}}: {{str(e)[:30]}}')

async def main():
    names = ['Rajesh Sharma', 'Sita Gurung', 'Prakash Thapa', 'Kamala Rai', 'Dipesh Shrestha', 'Sunita Tamang', 'Bibek Karki', 'Mina Poudel', 'Kiran Adhikari', 'Gita Neupane', 'Ramesh Bhandari', 'Laxmi Ghimire', 'Suresh Pandey', 'Radha Koirala', 'Naresh Joshi', 'Sarita Basnet', 'Mahesh Regmi', 'Purnima Dahal', 'Ganesh Khadka', 'Sabita Oli', 'Umesh Gautam', 'Bishnu Aryal', 'Shanti Bhattarai', 'Ramhari Subedi', 'Devi Chaudhary', 'Surya Magar', 'Indira Limbu', 'Hari Sherpa', 'Kamana Thakuri', 'Rajan Yadav', 'Nirmala Chhetri', 'Deepak Rijal', 'Sangita Kc', 'Mohan Sapkota', 'Geeta Mainali', 'Ashok Pokhrel', 'Sundar Acharya', 'Rama Devkota', 'Tek Bahadur', 'Sushila Dhakal', 'Binod Kafle', 'Saraswoti Upreti', 'Tilak Bhusal', 'Durga Lamichhane', 'Ravi Pandey', 'Shova Maharjan', 'Dinesh Khatri', 'Parbati Silwal', 'Gopal Humagain', 'Kamala Bhatta'][:{bot_count}]
    
    async with async_playwright() as p:
        # Bright Data residential proxy
        proxy_server = "http://brd-customer-hl_12345678-zone-residential:password@zproxy.lum-superproxy.io:22225"
        
        browser = await p.chromium.launch(
            headless=True,
            proxy={{"server": proxy_server}},
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=VizDisplayCompositor"
            ]
        )
        
        tasks = []
        for i, name in enumerate(names):
            task = asyncio.create_task(create_bot(browser, name))
            tasks.append(task)
            if i % 5 == 4:  # Every 5 bots
                await asyncio.sleep(1)
        
        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())
"""
            
            with open('/tmp/run_bots.py', 'w') as f:
                f.write(script)
            
            socketio.emit('console_output', {'data': f'🔧 Enhanced stealth bot script created'})
            socketio.emit('console_output', {'data': f'🎯 Target: {meet_url}'})
            socketio.emit('console_output', {'data': f'👥 Bot count: {bot_count}'})
            
            # Run the script and stream output
            process = subprocess.Popen(['python', '/tmp/run_bots.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     universal_newlines=True)
            
            for line in iter(process.stdout.readline, ''):
                socketio.emit('console_output', {'data': line.strip()})
                
        except Exception as e:
            socketio.emit('console_output', {'data': f'Error: {str(e)}'})
    
    threading.Thread(target=run_bots).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)