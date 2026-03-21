import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        )
        await page.goto('http://localhost:8000')
        await asyncio.sleep(2)

        # Click Guest login
        await page.evaluate("""() => {
            document.querySelector('#guestBtn').click();
        }""")
        await asyncio.sleep(3)

        # Click Hub
        await page.evaluate("""() => {
            const hubBtn = document.querySelector('.icon-btn[onclick="enterHub()"]');
            if (hubBtn) hubBtn.click();
        }""")
        await asyncio.sleep(2)

        # Open Global Lounge Sheet
        await page.evaluate("""() => {
            const lounge = Array.from(document.querySelectorAll('.hub-card')).find(c => c.innerText.includes('Global Lounge'));
            if (lounge) lounge.click();
        }""")
        await asyncio.sleep(1)

        # Click Join Global Lounge in sheet
        await page.evaluate("""() => {
            const joinBtn = document.querySelector('.sheet-btn[onclick*="GlobalLobby"]');
            if (joinBtn) joinBtn.click();
        }""")
        await asyncio.sleep(2)

        # Open Emoji Picker (Using toggleChatPicker('emojiPicker'))
        await page.evaluate("""() => {
            const emojiBtn = document.querySelector('button[onclick*="toggleChatPicker(\\'emojiPicker\\')"]');
            if (emojiBtn) emojiBtn.click();
        }""")
        await asyncio.sleep(2)

        await page.screenshot(path='real_picker_final.png')
        await browser.close()

asyncio.run(run())
