const puppeteer = require('puppeteer');

(async () => {
  console.log("Launching Puppeteer...");
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  
  try {
    console.log("Navigating to login page...");
    await page.goto('http://localhost:3000/auth/sign-in', { waitUntil: 'networkidle2' });
    
    console.log("Waiting for email input...");
    await page.waitForSelector('input[name="email"]', { timeout: 10000 });
    
    console.log("Entering credentials...");
    await page.type('input[name="email"]', 'admin@test.com');
    await page.type('input[name="password"]', 'password123');
    
    console.log("Submitting form...");
    await page.keyboard.press('Enter');
    
    console.log("Waiting for successful login navigation...");
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 15000 });
    
    console.log("Navigating directly to traces for seed-project...");
    await page.goto('http://localhost:3000/project/seed-project/traces', { waitUntil: 'networkidle2' });
    
    console.log("Checking for trace rows in the table...");
    await page.waitForFunction(() => {
        const rows = document.querySelectorAll('table tbody tr');
        return rows.length > 0;
    }, { timeout: 15000 });
    
    console.log("✅ Verification SUCCESS: Found trace data on the page!");
  } catch (error) {
    console.error("❌ Verification FAILED:", error);
    await page.screenshot({ path: '/Users/kathi.s/AGravity/ExpSolver/scripts/error.png' });
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
