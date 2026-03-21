import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Using a typical mobile viewport size
        context = await browser.new_context(viewport={'width': 390, 'height': 844})
        page = await context.new_page()

        # Assume there's a simple local server running
        await page.goto("http://localhost:8000")

        await page.wait_for_timeout(1000)

        # Click Guest login button
        await page.click('button.start-btn:has-text("Guest")')
        await page.wait_for_timeout(1000)

        # In Hub view, open Global Lounge
        await page.evaluate("openGlobalLounge()")
        await page.wait_for_timeout(1000)

        # Open emoji picker
        await page.evaluate("toggleChatPicker('emojiPicker')")
        await page.wait_for_timeout(1000)

        # Take a screenshot to verify the fix
        await page.screenshot(path="final_picker.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
