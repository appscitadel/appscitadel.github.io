import { createRequire } from 'node:module';
const require = createRequire('D:/appscitadel/play-revival/store-frames/package.json');
const { chromium } = require('playwright');
const b = await chromium.launch({ channel: 'chrome' });
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.goto('http://127.0.0.1:8765/tools/og.html'); await p.waitForTimeout(500);
await p.screenshot({ path: 'assets/hub-og.png' }); await b.close();
