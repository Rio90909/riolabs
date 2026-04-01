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

        page.goto("http://localhost:8000/index.html")

        # Mock admin state
        page.evaluate("""
            window.user = { uid: 'test_admin_user' };
            window.myProfile = { isAdmin: true };
            window.shopData = {
                bubbles: [{ id: 'b_test1', name: 'Test Bubble 1', color: '#ff0000', text: '#fff', price: 100 }],
                themes: [{ id: 't_test1', name: 'Test Theme 1', bg: '#000', acc: '#f00', isl: '#111', txt: '#fff', txtSec: '#aaa', price: 0 }]
            };
        """)

        page.wait_for_timeout(500)

        page.evaluate("window.openAdminShopManager()")
        page.wait_for_selector('#adminShopSheet.show', timeout=5000)

        page.evaluate("window.adminToggleShopModeTab('edit')")
        page.wait_for_timeout(1000)

        # Select the item
        page.select_option('#adminShopEditSelect', 'b_test1')
        page.wait_for_timeout(1000)

        # Print the current value of the select
        val = page.evaluate("document.getElementById('adminShopEditSelect').value")
        print(f"Selected value after select_option: {val}")

        name = page.evaluate("document.getElementById('adminShopName').value")
        print(f"Name value: {name}")

        price = page.evaluate("document.getElementById('adminShopPrice').value")
        print(f"Price value: {price}")

        browser.close()

    server_process.kill()

if __name__ == "__main__":
    run_test()
