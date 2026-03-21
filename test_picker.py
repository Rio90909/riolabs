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

        # force emoji picker
        await page.evaluate("""() => {
            const picker = document.getElementById('emojiPicker');
            picker.style.bottom = '90px';
        }""")
        await asyncio.sleep(1)

        await page.screenshot(path='picker_before.png')

        # apply css
        await page.add_style_tag(content='''
        #emojiPicker .picker-tabs {
            display: flex;
            width: 100%;
            gap: 5px;
            box-sizing: border-box;
        }
        #emojiPicker .p-tab {
            flex: 1;
            min-width: 0 !important;
            width: auto !important;
            box-sizing: border-box;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        ''')
        await asyncio.sleep(1)

        await page.screenshot(path='picker_after.png')
        await browser.close()

asyncio.run(run())
