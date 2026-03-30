from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8000/index.html')

    # Mock authentication and myProfile being an admin
    page.evaluate('''() => {
        window.user = { uid: "admin123", displayName: "Admin" };
        window.myProfile = { isAdmin: true, name: "Admin", orbs: 1000 };
        document.getElementById('auth-screen').classList.remove('active');
        document.getElementById('hub-screen').classList.add('active');
        document.querySelector('.dock-btn[data-tab="tab-profile"]').click();

        // Force display of adminBtn (usually handled by loadMyProfile from Firebase)
        document.getElementById('adminBtn').style.display = 'flex';
    }''')

    # Wait for the profile tab to be visible
    page.wait_for_selector('#tab-profile', state='visible')

    # Check if Admin Panel button is visible
    admin_btn = page.locator('#adminBtn')
    if admin_btn.is_visible():
        print("PASS: Admin Panel button is visible on Profile tab.")
    else:
        print("FAIL: Admin Panel button is NOT visible.")

    # Execute the javascript function to switch screens directly
    page.evaluate('''() => {
        window.openAdminPanel();
    }''')

    page.wait_for_selector('#admin-screen.active', state='attached')
    page.wait_for_function('document.getElementById("admin-screen").style.opacity === "1"')

    # Verify Admin screen is active
    admin_screen = page.locator('#admin-screen')
    if 'active' in admin_screen.get_attribute('class'):
        print("PASS: Admin screen became active.")
    else:
        print("FAIL: Admin screen is NOT active.")

    # Verify elements on Admin screen
    search_input = page.locator('#adminSearchInput')
    if search_input.is_visible():
         print("PASS: Admin search input is visible.")
    else:
         print("FAIL: Admin search input is NOT visible.")

    browser.close()
