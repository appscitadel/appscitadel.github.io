// Screenshots the local site at desktop and mobile sizes, in light and dark: node tools/shoot.mjs <url-path> <name>
import { createRequire } from 'node:module';
const require = createRequire('D:/appscitadel/play-revival/store-frames/package.json');
const { chromium } = require('playwright');

const [path = 'privacy/fatawyibnbaz.html', name = 'pp'] = process.argv.slice(2);
const browser = await chromium.launch({ channel: 'chrome' });
for (const scheme of ['light', 'dark']) {
  for (const [label, viewport, isMobile] of [['desktop', { width: 1366, height: 900 }, false], ['mobile', { width: 390, height: 844 }, true]]) {
    const page = await browser.newPage({ viewport, isMobile, deviceScaleFactor: 1, colorScheme: scheme });
    await page.goto(`http://127.0.0.1:8765/${path}`, { waitUntil: 'networkidle' });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    await page.screenshot({ path: `_shots/${name}-${label}-${scheme}.png`, fullPage: true });
    console.log(`${name}-${label}-${scheme}: horizontal overflow ${overflow}px`);
    await page.close();
  }
}
await browser.close();
