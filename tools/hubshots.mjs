// Screenshots the hub: node tools/hubshots.mjs  (needs the site served on 127.0.0.1:8765)
import { createRequire } from 'node:module';
const require = createRequire('D:/appscitadel/play-revival/store-frames/package.json');
const { chromium } = require('playwright');
const browser = await chromium.launch({ channel: 'chrome' });
const sizes = [['390', { width: 390, height: 844 }, true], ['768', { width: 768, height: 1024 }, false], ['1440', { width: 1440, height: 900 }, false]];
const runs = [['', '/'], ['-from', '/?from=sabakalemat'], ['-en', '/en/']];
for (const [rl, path] of runs) for (const scheme of ['light', 'dark']) for (const [label, viewport, mob] of sizes) {
  if (rl === '-en' && label !== '390') continue;
  const ctx = await browser.newContext({ viewport, isMobile: mob, hasTouch: mob, deviceScaleFactor: 1, colorScheme: scheme,
    userAgent: mob ? 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/124.0 Mobile Safari/537.36' : undefined });
  const page = await ctx.newPage();
  let bytes = 0; page.on('response', async r => { try { bytes += (await r.body()).length } catch {} });
  await page.goto(`http://127.0.0.1:8765${path}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.querySelectorAll('.rv').forEach(e => e.classList.add('in')));
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
  await page.waitForTimeout(700);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  await page.screenshot({ path: `_shots/hub${rl}-${label}-${scheme}.png`, fullPage: true });
  console.log(`hub${rl}-${label}-${scheme}: overflow ${overflow}px, first-load bytes ${bytes}`);
  await ctx.close();
}
await browser.close();
