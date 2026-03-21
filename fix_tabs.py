from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 812})

    file_path = f"file://{os.path.abspath('index.html')}"
    page.goto(file_path)

    # Wait for the app to initialize
    time.sleep(1)

    # Log in as guest
    page.click("text=Continue as Guest")
    time.sleep(2)

    # Take screenshot of hub
    page.screenshot(path="tabs_real_hub.png")

    # Open global lounge sheet
    page.click("h3:text('Global Lounge')")
    time.sleep(1)

    page.screenshot(path="tabs_real_sheet.png")

    # Click join
    page.click("text=Join Global Lounge")
    time.sleep(2)

    page.screenshot(path="tabs_real_chat.png")

    # Click the emoji button to open the picker
    # If the selector is wrong, let's use document evaluate
    page.evaluate("""() => {
        let btn = document.querySelector('#emoji-btn') || document.querySelector('.emoji-btn');
        if(btn) btn.click();
    }""")
    time.sleep(1)

    # Take screenshot of the picker with GIF tab before fix
    page.screenshot(path="tabs_real_before.png")

    # Apply dynamic CSS fix
    page.evaluate("""() => {
        const style = document.createElement('style');
        style.innerHTML = `
            #emojiPicker .picker-tabs {
                gap: 5px;
            }
            #emojiPicker .p-tab {
                flex: 1;
                min-width: 0 !important;
                width: auto !important;
            }
        `;
        document.head.appendChild(style);
    }""")
    time.sleep(1)
    page.screenshot(path="tabs_real_after.png")
    browser.close()
