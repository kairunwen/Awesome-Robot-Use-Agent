// Optional smoke check: use an installed Playwright and Chrome; no downloads.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1280, height: 900}});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    const url = process.env.PREVIEW_URL || 'http://127.0.0.1:8765/Awesome-Robot-Use-Agent/website/dist/';
    await page.goto(url, {waitUntil: 'domcontentloaded'});
    const total = await page.locator('.entry').count();
    const count = () => page.locator('.entry:not([hidden])').count();
    await page.locator('#search').fill('AgenticROS');
    const tool = page.locator('details.entry').filter({has: page.locator('.entry-title', {hasText: /^AgenticROS$/})});
    await tool.locator(':scope > summary').click();
    const note = tool.locator('.entry-notes');
    assert.equal(await note.getAttribute('open'), null);
    await note.locator('summary').click();
    assert.equal(await note.locator('p').last().isVisible(), true);
    assert.equal(await note.locator('summary').evaluate(el => getComputedStyle(el).display), 'list-item');
    await note.locator('summary').click();
    assert.equal(await note.locator('p').last().isVisible(), false);
    await page.locator('#clear').click();
    const initial = await page.locator('table[data-demo] tbody').evaluateAll(bodies => bodies.map(b => [...b.rows].map(r => r.id)));
    for (const kind of ['demos', 'real', 'simulation', 'perception']) {
      await page.locator('#demo-filter').selectOption(kind);
      const expected = await page.locator(kind === 'demos' ? '.entry[data-demo]' : `.entry[data-demo="${kind}"]`).count();
      assert.equal(await count(), expected);
      assert.equal(await page.locator('.entry:visible').count(), expected);
    }
    await page.locator('#demo-filter').selectOption('demos');
    await page.locator('#code-filter').check();
    assert.equal(await count(), await page.locator('.entry[data-demo][data-code="true"]').count());
    assert.equal(await page.locator('[data-demo-intro="simulation"]:visible').count(), 0);
    await page.locator('#search').fill('StationeryBench'); assert.equal(await count(), 1);
    await page.locator('#search').fill('not-a-real-resource-123'); assert.equal(await count(), 0);
    assert.equal(await page.locator('#empty').isVisible(), true);
    await page.locator('#clear').click(); assert.equal(await count(), total);
    for (const order of ['oldest', 'newest']) {
      await page.locator('#demo-order').selectOption(order);
      const dates = await page.locator('table[data-demo] tbody').evaluateAll(bodies => bodies.map(b => [...b.rows].map(r => r.dataset.date)));
      for (const list of dates) assert.deepEqual(list, [...list].sort((a, b) => order === 'oldest' ? a.localeCompare(b) : b.localeCompare(a)));
    }
    await page.locator('#clear').click();
    assert.deepEqual(await page.locator('table[data-demo] tbody').evaluateAll(bodies => bodies.map(b => [...b.rows].map(r => r.id))), initial);
    await page.locator('[data-filter="papers"]').click();
    await page.locator('#demo-filter').selectOption('real'); assert.equal(await count(), 0);
    await page.goto(url + '#real-robot-demonstrations', {waitUntil: 'domcontentloaded'});
    assert.equal(await page.locator('#demo-filter').inputValue(), 'all');
    assert.equal(await count(), total);
    for (const width of [390, 320]) {
      await page.setViewportSize({width, height: 844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Overflow at ${width}`);
    }
    await page.setViewportSize({width: 1280, height: 900});
    await page.locator('#demo-filter').selectOption('demos');
    await page.locator('#code-filter').check();
    await page.locator('#discovery-tools').scrollIntoViewIfNeeded();
    if (process.env.SCREENSHOT_PATH) await page.screenshot({path: process.env.SCREENSHOT_PATH});
    const nojs = await browser.newPage({javaScriptEnabled: false});
    await nojs.goto(url, {waitUntil: 'domcontentloaded'});
    assert.equal(await nojs.locator('#discovery-tools').isVisible(), false);
    assert.equal(await nojs.locator('.entry').count(), total);
    assert.deepEqual(errors, []);
    console.log('Passed demo/code filters, search, empty state, sorting/reset, category combinations, anchor reset, mobile widths, and no-JS fallback.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
