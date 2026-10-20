const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUT_DIR = path.join(__dirname, 'outputs', 'screenshots', 'responsive_darkmode');

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function dismissPopups(page) {
  try {
    await page.evaluate(() => {
      // Find and click "Don't show again" or close buttons
      const buttons = Array.from(document.querySelectorAll('button'));
      for (const b of buttons) {
        if (b.innerText && (b.innerText.includes("Don't show again") || b.innerText.includes("Dismiss"))) {
          b.click();
        }
      }
      // Hide any toast notifications in screenshot
      const toasts = document.querySelectorAll('div[data-testid="stToast"]');
      toasts.forEach(t => t.style.display = 'none');
    });
  } catch (e) {}
}

async function selectNav(page, keyword) {
  // If sidebar is collapsed (mobile/tablet), open it first
  try {
    await page.evaluate(() => {
      const collapsedControl = document.querySelector('[data-testid="stSidebarCollapsedControl"] button, [data-testid="collapsedControl"]');
      if (collapsedControl) {
        collapsedControl.click();
      }
    });
    await sleep(600);
  } catch(e) {}

  // Click the radio option matching keyword
  await page.evaluate((kw) => {
    const labels = Array.from(document.querySelectorAll('[data-testid="stRadio"] label'));
    for (const l of labels) {
      if (l.innerText.includes(kw)) {
        l.click();
        return;
      }
    }
  }, keyword);

  await sleep(1500);

  // If on mobile/narrow screen, close sidebar to see full content
  try {
    await page.evaluate(() => {
      if (window.innerWidth <= 768) {
        const closeBtn = document.querySelector('[data-testid="stSidebarCollapseButton"] button');
        if (closeBtn) closeBtn.click();
      }
    });
    await sleep(600);
  } catch(e) {}
}

async function runPrediction(page, presetName) {
  // Click preset chip
  await page.evaluate((pName) => {
    const buttons = Array.from(document.querySelectorAll('button'));
    for (const b of buttons) {
      if (b.innerText && b.innerText.includes(pName)) {
        b.click();
        return;
      }
    }
  }, presetName);

  await sleep(1200);

  // Click predict button
  await page.evaluate(() => {
    const buttons = Array.from(document.querySelectorAll('button'));
    for (const b of buttons) {
      if (b.innerText && b.innerText.includes("Jalankan Analisis Prediksi")) {
        b.click();
        return;
      }
    }
  });

  await sleep(1500);
}

async function run() {
  console.log('=== Memulai Pengujian Otomatis & Screenshot Matrix ===');

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  const themes = ['light', 'dark'];
  
  for (const theme of themes) {
    console.log(`\n--- Menguji Tema: ${theme.toUpperCase()} ---`);
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: theme }]);

    // 1. Desktop 1440x900 (Semua 4 Halaman + Hasil Prediksi)
    await page.setViewport({ width: 1440, height: 900 });
    await page.goto('http://localhost:8501', { waitUntil: 'networkidle0', timeout: 30000 });
    await sleep(2000);
    await dismissPopups(page);

    // Halaman 1: Dashboard
    await selectNav(page, 'Dashboard');
    await dismissPopups(page);
    let filename = `desktop_1440x900_${theme}_dashboard.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // Halaman 2: Prediction Workspace (Form Default)
    await selectNav(page, 'Prediction');
    await dismissPopups(page);
    filename = `desktop_1440x900_${theme}_prediction_form.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // Halaman 2b: Prediction Workspace (Hasil Prediksi Positif)
    await runPrediction(page, 'Niat Beli Tinggi');
    await dismissPopups(page);
    filename = `desktop_1440x900_${theme}_prediction_result_positive.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // Halaman 3: Evaluasi Model
    await selectNav(page, 'Evaluasi Model');
    await dismissPopups(page);
    filename = `desktop_1440x900_${theme}_evaluation.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // Halaman 4: Tentang Model
    await selectNav(page, 'Tentang Model');
    await dismissPopups(page);
    filename = `desktop_1440x900_${theme}_about.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // 2. Desktop 1280x800
    await page.setViewport({ width: 1280, height: 800 });
    await selectNav(page, 'Dashboard');
    await dismissPopups(page);
    filename = `desktop_1280x800_${theme}_dashboard.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // 3. Tablet 1024x768 (Landscape)
    await page.setViewport({ width: 1024, height: 768 });
    await selectNav(page, 'Dashboard');
    await dismissPopups(page);
    filename = `tablet_1024x768_${theme}_dashboard.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // 4. Tablet 768x1024 (Portrait)
    await page.setViewport({ width: 768, height: 1024 });
    await selectNav(page, 'Dashboard');
    await dismissPopups(page);
    filename = `tablet_768x1024_${theme}_dashboard.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // 5. Mobile 430x932 (Large Smartphone)
    await page.setViewport({ width: 430, height: 932, isMobile: true, hasTouch: true });
    await selectNav(page, 'Dashboard');
    await dismissPopups(page);
    filename = `mobile_430x932_${theme}_dashboard.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    await selectNav(page, 'Prediction');
    await dismissPopups(page);
    filename = `mobile_430x932_${theme}_prediction.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    await selectNav(page, 'Evaluasi Model');
    await dismissPopups(page);
    filename = `mobile_430x932_${theme}_evaluation.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    // 6. Mobile 375x812 (Compact Smartphone)
    await page.setViewport({ width: 375, height: 812, isMobile: true, hasTouch: true });
    await selectNav(page, 'Dashboard');
    await dismissPopups(page);
    filename = `mobile_375x812_${theme}_dashboard.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);

    await selectNav(page, 'Prediction');
    await dismissPopups(page);
    filename = `mobile_375x812_${theme}_prediction.png`;
    await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
    console.log(`[OK] Screenshot: ${filename}`);
  }

  await browser.close();
  console.log('\n=== Semua Screenshot Berhasil Dihasilkan dan Tersimpan di: ===');
  console.log(OUT_DIR);
}

run().catch(err => {
  console.error('Error running screenshot generator:', err);
  process.exit(1);
});
