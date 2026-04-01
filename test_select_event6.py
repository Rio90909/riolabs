import os
import subprocess
import time
from playwright.sync_api import sync_playwright

def run_test():
    pwd = os.getcwd()
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"], cwd=pwd)
    time.sleep(1)

    with sync_playwright() as p:
        iphone_13 = p.devices['iPhone 13']
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**iphone_13)
        page = context.new_page()

        # We need to catch console logs
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))

        page.goto("http://localhost:8000/index.html")

        # Mock admin state
        page.evaluate("""
            window.user = { uid: 'test_admin_user' };
            window.myProfile = { isAdmin: true };
            window.shopData = {
                bubbles: [{ id: 'b_test1', name: 'Test Bubble 1', color: '#ff0000', text: '#fff', price: 100 }],
                themes: [{ id: 't_test1', name: 'Test Theme 1', bg: '#000', acc: '#f00', isl: '#111', txt: '#fff', txtSec: '#aaa', price: 0 }]
            };

            // Force open sheet directly
            document.getElementById('adminShopSheet').classList.add('show');
            document.getElementById('adminShopMode').value = 'edit';
            window.adminUpdateShopFields(false);
        """)

        page.wait_for_timeout(500)

        # Let's interact
        page.evaluate("""
            console.log("Checking options in adminShopEditSelect:");
            const sel = document.getElementById('adminShopEditSelect');
            for(let i = 0; i < sel.options.length; i++) {
                console.log("Option " + i + ": value='" + sel.options[i].value + "', text='" + sel.options[i].text + "'");
            }
        """)
        page.wait_for_timeout(500)

        browser.close()

    server_process.kill()

if __name__ == "__main__":
    run_test()
