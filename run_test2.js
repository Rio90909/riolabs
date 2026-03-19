const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => {
      console.log('PAGE ERROR:', error.message);
      console.log('STACK:', error.stack);
  });

  await page.goto('file://' + __dirname + '/index.html');
  await page.waitForTimeout(1000);

  console.log('Triggering switchScreen...');
  await page.evaluate(() => {
     window.enterRoom('GlobalLobby');
  });
  await page.waitForTimeout(1000);

  await browser.close();
})();
