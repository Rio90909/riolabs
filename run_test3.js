const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  await page.goto('file://' + __dirname + '/index.html');
  await page.waitForTimeout(1000);

  console.log('Testing Global Lounge enterRoom');

  // Since firebase is restricted without auth, we just verify no crash happens when calling window.enterRoom
  try {
     await page.evaluate(() => {
        // Mock db.ref to avoid permission error for the test
        window.db = {
           ref: function() {
              return {
                 off: function(){},
                 on: function(){},
                 once: function() { return Promise.resolve({ forEach: ()=>{} }) },
                 set: function(){},
                 update: function(){},
                 push: function(){},
                 orderByChild: function() { return this; },
                 limitToLast: function() { return this; }
              }
           }
        };
        window.enterRoom('GlobalLobby');
     });
     console.log('enterRoom succeeded without JS crash!');
  } catch (err) {
     console.error('Error executing enterRoom:', err.message);
  }

  await page.waitForTimeout(1000);

  await browser.close();
})();
