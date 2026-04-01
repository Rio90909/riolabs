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

            // Add a logging wrapper around the functions
            const origLoad = window.adminLoadExistingShopItem;
            window.adminLoadExistingShopItem = function() {
                console.log("adminLoadExistingShopItem started");
                try {
                    origLoad();
                    console.log("adminLoadExistingShopItem completed. select value is: " + document.getElementById('adminShopEditSelect').value);
                } catch(e) {
                    console.log("Error in adminLoadExistingShopItem: " + e.message);
                }
            };

            const origUpdate = window.adminUpdateShopFields;
            window.adminUpdateShopFields = function(skip) {
                console.log("adminUpdateShopFields started. skipRepopulate: " + skip);
                try {
                    origUpdate(skip);
                    console.log("adminUpdateShopFields completed");
                } catch(e) {
                    console.log("Error in adminUpdateShopFields: " + e.message);
                }
            };

            window.adminUpdateShopFields(false);
        """)

        page.wait_for_timeout(500)

        # Select the item using javascript, simulating change event
        page.evaluate("""
            const sel = document.getElementById('adminShopEditSelect');
            sel.value = 'b_test1';
            sel.dispatchEvent(new Event('change'));
        """)
        page.wait_for_timeout(1000)

        browser.close()

    server_process.kill()

if __name__ == "__main__":
    run_test()
