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

        # Let's test interaction
        page.evaluate("""
            const sel = document.getElementById('adminShopEditSelect');
            sel.value = 'b_test1';

            console.log("Calling adminLoadExistingShopItem directly...");
            window.adminLoadExistingShopItem();

            setTimeout(() => {
                console.log("Done. id input value: " + document.getElementById('adminShopId').value);
                console.log("Done. name input value: " + document.getElementById('adminShopName').value);
                console.log("Done. price input value: " + document.getElementById('adminShopPrice').value);
                console.log("Done. bubble bg value: " + document.getElementById('adminShopBubbleBg').value);
            }, 100);
        """)
        page.wait_for_timeout(1000)

        browser.close()

    server_process.kill()

if __name__ == "__main__":
    run_test()
