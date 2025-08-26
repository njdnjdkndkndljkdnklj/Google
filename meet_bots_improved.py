# meet_bots.py
# Usage example:
#   python meet_bots.py --link "https://meet.google.com/xxx-xxxx-xxx" --bots 5 --headless False --leave-after 0
#
# Requirements:
#   pip install playwright
#   python -m playwright install chromium
#
# Recommended on Linux servers:
#   xvfb-run -s "-screen 0 1920x1080x24" python meet_bots.py ...

import asyncio
import argparse
import random
import string
import re
import sys
import logging
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# ---------- helpers ----------
def random_name(prefix="Bot", length=4):
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{suffix}"

async def click_if_visible(page: Page, selector: str, timeout: int = 3000) -> bool:
    try:
        elm = page.locator(selector)
        if await elm.count() and await elm.first.is_visible():
            await elm.first.click(timeout=timeout)
            return True
    except Exception:
        pass
    return False

async def fill_name_field(page: Page, name: str) -> bool:
    # Try a series of strategies to locate the "your name" text field
    selectors = [
        "input[placeholder*='name']",
        "input[aria-label*='name']",
        "input[aria-label*='Name']",
        "input[type='text']",
    ]
    for sel in selectors:
        try:
            el = page.locator(sel)
            if await el.count():
                # pick the first visible one
                for i in range(await el.count()):
                    item = el.nth(i)
                    if await item.is_visible():
                        await item.fill(name)
                        logging.info("Filled name using selector: %s", sel)
                        return True
        except Exception:
            pass

    # fallback: fill first visible textbox role
    try:
        boxes = page.get_by_role("textbox")
        for i in range(await boxes.count()):
            b = boxes.nth(i)
            if await b.is_visible():
                await b.fill(name)
                logging.info("Filled name using role=textbox fallback")
                return True
    except Exception:
        pass

    logging.warning("Could not find name input field")
    return False

async def mute_mic_camera(page: Page):
    # Attempt to ensure mic & camera are off by reading aria-label and toggling if needed.
    # These aria-label values may vary by locale; we try to be defensive.
    try:
        # micro
        mic_btn = page.locator("button[aria-label*='microphone'], button[aria-label*='Microphone'], button[aria-label*='mic']")
        if await mic_btn.count():
            lbl = await mic_btn.first.get_attribute("aria-label") or ""
            if re.search(r"turn off|mute|on", lbl, re.I):
                # if label indicates "Turn off microphone" or similar -> it's currently ON, so click to turn OFF
                if re.search(r"turn off|mute", lbl, re.I):
                    await mic_btn.first.click()
                    logging.info("Clicked mic toggle to mute (label=%s)", lbl)
            else:
                # fallback: click once if visible (best-effort)
                await mic_btn.first.click()
                logging.info("Clicked mic toggle (fallback)")
    except Exception:
        logging.debug("Mute mic step failed", exc_info=True)

    try:
        cam_btn = page.locator("button[aria-label*='camera'], button[aria-label*='Camera'], button[aria-label*='video']")
        if await cam_btn.count():
            lbl = await cam_btn.first.get_attribute("aria-label") or ""
            if re.search(r"turn off|stop video|camera on|on camera", lbl, re.I):
                if re.search(r"turn off|stop", lbl, re.I):
                    await cam_btn.first.click()
                    logging.info("Clicked camera toggle to turn camera off (label=%s)", lbl)
            else:
                await cam_btn.first.click()
                logging.info("Clicked camera toggle (fallback)")
    except Exception:
        logging.debug("Mute camera step failed", exc_info=True)

async def press_join(page: Page) -> bool:
    # Try common join button texts
    join_texts = [r"join now", r"join", r"ask to join", r"ask to join", r"ask to join meeting", r"ask to join"]
    for txt in join_texts:
        try:
            btn = page.get_by_role("button", name=re.compile(txt, re.I))
            if await btn.count() and await btn.first.is_visible():
                await btn.first.click()
                logging.info("Clicked button with text match: %s", txt)
                return True
        except Exception:
            pass

    # fallback: button with text 'Ask to join' or generic click on first visible button near center
    try:
        fallback_btn = page.locator("button:visible").filter(has_text=re.compile(r"join|ask", re.I)).first
        if await fallback_btn.count() and await fallback_btn.is_visible():
            await fallback_btn.click()
            logging.info("Clicked fallback visible join-like button")
            return True
    except Exception:
        pass

    logging.warning("Could not find a Join/Ask button on the page")
    return False

# ---------- single-bot routine ----------
async def bot_join(page: Page, meet_link: str, display_name: str, join_timeout=45_000):
    logging.info("Bot '%s' going to: %s", display_name, meet_link)
    await page.goto(meet_link, timeout=40_000)

    # optional: handle cookie/consent dialog by clicking Accept if present (best-effort)
    try:
        await click_if_visible(page, "button:has-text('I agree'), button:has-text('Accept'), button:has-text('Agree')", 3000)
    except Exception:
        pass

    # Wait a bit for UI to load
    await asyncio.sleep(1 + random.random() * 1.5)

    # Fill name (guest) if available
    await fill_name_field(page, display_name)
    await asyncio.sleep(0.5 + random.random() * 1.0)

    # Mute camera and mic before joining (best-effort)
    await mute_mic_camera(page)
    await asyncio.sleep(0.3 + random.random() * 0.7)

    # Click Join / Ask to join
    joined = await press_join(page)
    if not joined:
        logging.error("Bot '%s' could not press Join/Ask. It may need manual approval or Google changed UI.", display_name)
        return False

    # Optionally wait for an element that indicates we're in the meeting (best-effort)
    try:
        # Wait for something that usually appears in the meeting UI: a 'Present now' or 'People' button
        await page.wait_for_selector("text=Present now, text=People, button[aria-label*='Present']", timeout=30_000)
        logging.info("Bot '%s' appears to be in the meeting.", display_name)
        return True
    except Exception:
        logging.info("Bot '%s' press Join, but couldn't confirm inside state (it might be in lobby awaiting admit).", display_name)
        return True

# ---------- main orchestration ----------
async def run_all(meet_link: str, count: int, headless: bool, leave_after: int):
    async with async_playwright() as p:
        # Launch single browser instance; create multiple contexts for isolation
        browser: Browser = await p.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--use-fake-ui-for-media-stream",      # helps bypass getUserMedia permission dialogs
                "--use-fake-device-for-media-stream",
                "--autoplay-policy=no-user-gesture-required",
                "--disable-gpu",
            ],
        )
        pages = []
        contexts = []
        tasks = []

        for i in range(count):
            ctx = await browser.new_context()  # separate context = separate localStorage/cookies
            contexts.append(ctx)
            page = await ctx.new_page()
            pages.append(page)

            # unique display name
            name = f"Bot-{i+1}-{random_name('', 3)}"
            # stagger joins a bit
            delay = random.uniform(1.0, 6.0) * i / max(1, min(10, count))
            tasks.append(asyncio.create_task(single_bot_lifecycle(page, meet_link, name, delay, leave_after)))

        try:
            await asyncio.gather(*tasks)
        finally:
            # cleanup
            for ctx in contexts:
                try:
                    await ctx.close()
                except Exception:
                    pass
            await browser.close()

async def single_bot_lifecycle(page: Page, meet_link: str, name: str, delay: float, leave_after: int):
    await asyncio.sleep(delay)  # stagger
    joined = await bot_join(page, meet_link, name)
    if not joined:
        logging.warning("Bot %s failed to join properly", name)
        # keep page open a little while for debugging, then close
        await asyncio.sleep(10)
        await page.context.close()
        return

    # Stay until meeting ends or until leave_after seconds pass (0 => indefinite)
    if leave_after and leave_after > 0:
        logging.info("Bot %s will stay for %s seconds", name, leave_after)
        await asyncio.sleep(leave_after)
        logging.info("Bot %s leaving after timeout", name)
        await page.context.close()
    else:
        logging.info("Bot %s will stay indefinitely. Stop with Ctrl+C.", name)
        # indefinite sleep; keep context open
        while True:
            await asyncio.sleep(60)

# ---------- CLI ----------
def parse_args():
    parser = argparse.ArgumentParser(description="Auto-join Google Meet as guest bots (Playwright)")
    parser.add_argument("--link", "-l", required=True, help="Google Meet link (e.g. https://meet.google.com/xxx-xxxx-xxx)")
    parser.add_argument("--bots", "-n", type=int, default=1, help="Number of bots to spawn")
    parser.add_argument("--headless", action="store_true", help="Run in headless chromium (may break WebRTC). Default: headful recommended on servers with Xvfb")
    parser.add_argument("--leave-after", type=int, default=0, help="Auto-leave after this many seconds (0 = stay until killed)")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        asyncio.run(run_all(args.link, args.bots, args.headless, args.leave_after))
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()