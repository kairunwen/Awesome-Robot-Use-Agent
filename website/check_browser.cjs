// Optional smoke check: use an installed Playwright and Chrome; no downloads.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1280, height: 900}});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.route('https://img.shields.io/github/stars/**/*.json', route => route.fulfill({json: {value: '1.2k'}}));
    await page.route('**/citations.json', route => route.fulfill({json: {source: 'Semantic Scholar', papers: {
      'ARXIV:2609.10522': {count: 1234, url: 'https://www.semanticscholar.org/paper/' + 'a'.repeat(40), updated_at: '2026-09-13T00:00:00+00:00'},
      'ARXIV:2209.07753': {count: 0, url: 'https://www.semanticscholar.org/paper/' + 'b'.repeat(40), updated_at: '2026-09-13T00:00:00+00:00'},
    }}}));
    const url = process.env.PREVIEW_URL || 'http://127.0.0.1:8765/Awesome-Robot-Use-Agent/website/dist/';
    await page.goto(url, {waitUntil: 'domcontentloaded'});
    const total = await page.locator('.entry').count();
    await page.locator('.institution-logo img').evaluateAll(images => images.forEach(image => { image.loading = 'eager'; }));
    await page.waitForFunction(() => [...document.querySelectorAll('.institution-logo img')].every(image => image.complete));
    assert.ok(await page.locator('.institution-logo img').evaluateAll(images => images.length > 0 && images.every(image => image.naturalWidth > 0 && image.alt)));
    const count = () => page.locator('.entry:not([hidden])').count();
    await page.goto(url + '#system-comparison', {waitUntil: 'domcontentloaded'});
    await page.addStyleTag({content: 'html { scroll-behavior: auto !important; }'});
    assert.equal(await page.locator('.system-comparison table').isVisible(), true);
    assert.equal(await page.locator('.system-comparison tbody tr').count(), 10);
    for (const width of [390, 320]) {
      await page.setViewportSize({width, height: 844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Comparison overflow at ${width}`);
      assert.ok(await page.locator('.comparison-scroll').evaluate(el => el.scrollWidth > el.clientWidth));
    }
    await page.setViewportSize({width: 1280, height: 900});
    if (await page.locator('#clear').isVisible()) await page.locator('#clear').click();
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
    await page.locator('[data-filter="benchmarks-1"]').click();
    assert.equal(await page.locator('.reading-entry:visible').count(), 18);
    assert.equal(await page.locator('#benchmarks-1 .reading-environment').count(), 18);
    const benchmarkDates = () => page.locator('#benchmarks-1 .reading-entry').evaluateAll(rows => rows.map(row => Date.parse(row.dataset.date) || -1));
    const newestBenchmarks = await benchmarkDates();
    assert.deepEqual(newestBenchmarks, [...newestBenchmarks].sort((a, b) => b - a));
    assert.equal(await page.locator('#benchmarks-1 [data-reading-sort="newest"]').getAttribute('aria-pressed'), 'true');
    for (const order of ['citations', 'stars']) {
      await page.locator(`#benchmarks-1 [data-reading-sort="${order}"]`).click();
      await page.waitForFunction(() => document.querySelector('#benchmark-sort-status').textContent === '');
      const values = await page.locator('#benchmarks-1 .reading-entry').evaluateAll((rows, order) => rows.map(row => Math.max(-1, ...[...row.querySelectorAll(order === 'stars' ? '.reading-stars[data-count]' : '.reading-citations[data-count]')].map(c => Number(c.dataset.count)))), order);
      assert.deepEqual(values, [...values].sort((a, b) => b - a));
      assert.equal(await page.locator('#papers [data-reading-sort="newest"]').getAttribute('aria-pressed'), 'true');
    }
    await page.locator('#clear').click();
    assert.deepEqual(await benchmarkDates(), newestBenchmarks);
    await page.locator('[data-filter="benchmarks-1"]').click();
    const benchmark = page.locator('#benchmarks-1-entry-0');
    assert.ok((await benchmark.locator('.reading-cover').boundingBox()).width > 200);
    assert.equal(await benchmark.evaluate(el => getComputedStyle(el).paddingTop), '16px');
    await benchmark.locator('.reading-details > summary').click();
    assert.equal(await benchmark.locator('.entry-body').isVisible(), true);
    assert.match(await benchmark.locator('.reading-publication').textContent(), /CVPR · 2020/);
    await benchmark.locator('.reading-details > summary').click();
    for (const width of [390, 320]) {
      await page.setViewportSize({width, height: 844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Benchmark overflow at ${width}`);
    }
    await page.setViewportSize({width: 1280, height: 900});
    await page.locator('[data-filter="papers"]').click();
    assert.equal(await page.locator('.reading-entry:visible').count(), 56);
    const citations = page.locator('[data-citation-id="ARXIV:2609.10522"]').first();
    assert.equal(await citations.textContent(), '1,234');
    assert.equal(await citations.locator('..').getAttribute('href'), 'https://www.semanticscholar.org/paper/' + 'a'.repeat(40));
    assert.equal(await page.locator('[data-citation-id="ARXIV:2209.07753"]').textContent(), '0');
    assert.equal(await page.locator('[data-citation-id="ARXIV:2510.10991"]').textContent(), '—');
    const paper = page.locator('#papers .reading-entry').first();
    await paper.locator('.reading-details > summary').click();
    assert.equal(await paper.locator('.entry-body').isVisible(), true);
    await paper.locator('.reading-details > summary').click();
    const cover = paper.locator('.reading-cover img');
    await cover.evaluate(image => image.dispatchEvent(new Event('error')));
    assert.equal(await cover.isHidden(), true);
    assert.equal(await paper.locator('.reading-cover-text').isVisible(), true);
    await page.locator('#code-filter').check();
    assert.equal(await count(), await page.locator('#papers .entry[data-code="true"]').count());
    await page.locator('#code-filter').uncheck();
    const stars = page.locator('#papers .reading-stars').first();
    await stars.scrollIntoViewIfNeeded();
    await page.waitForFunction(() => document.querySelector('#papers .reading-stars').textContent === '☆ 1.2k');
    const paperOrder = await page.locator('#papers .reading-entry').evaluateAll(rows => rows.map(row => row.id));
    const projectOrder = await page.locator('#projects .entry').evaluateAll(rows => rows.map(row => row.id));
    await page.locator('#papers [data-reading-sort="citations"]').click();
    assert.equal(await page.locator('#paper-sorted .reading-entry').count(), 56);
    assert.equal(await page.locator('#paper-sorted .reading-entry').first().locator('[data-citation-id]').getAttribute('data-citation-id'), 'ARXIV:2609.10522');
    const citationValues = await page.locator('#paper-sorted .reading-entry').evaluateAll(rows => rows.map(row => Number(row.querySelector('.reading-citations')?.dataset.count ?? -1)));
    assert.ok(citationValues.includes(0) && citationValues.includes(-1));
    assert.deepEqual(citationValues, [...citationValues].sort((a, b) => b - a));
    await page.locator('#papers [data-reading-sort="newest"]').click();
    const paperDates = await page.locator('#paper-sorted .reading-entry').evaluateAll(rows => rows.map(row => Date.parse(row.dataset.date) || -1));
    assert.deepEqual(paperDates, [...paperDates].sort((a, b) => b - a));
    assert.deepEqual(await page.locator('#paper-sorted .reading-entry').evaluateAll(rows => rows.map(row => row.id)), paperOrder);
    const repoUrls = await page.locator('#papers [data-stars-url]').evaluateAll(counters => [...new Set(counters.map(c => c.dataset.starsUrl))]);
    await page.route('https://img.shields.io/github/stars/**/*.json', route => {
      const target = route.request().url();
      return route.fulfill({json: target === repoUrls[1] ? {value: 'invalid', isError: true}
        : {value: target === repoUrls.at(-1) ? '12.5k' : target === repoUrls[0] ? '0' : '1,200'}});
    });
    await page.goto(url, {waitUntil: 'domcontentloaded'});
    await page.locator('[data-filter="papers"]').click();
    await page.locator('#papers [data-reading-sort="stars"]').click();
    await page.waitForFunction(() => document.querySelector('#paper-sort-status').textContent === '');
    const starValues = await page.locator('#paper-sorted .reading-entry').evaluateAll(rows => rows.map(row => Math.max(-1, ...[...row.querySelectorAll('.reading-stars[data-count]')].map(c => Number(c.dataset.count)))));
    assert.equal(starValues.length, 56);
    assert.equal(starValues[0], 12500, 'An offscreen repository must be loaded before ranking');
    assert.ok(starValues.includes(0) && starValues.includes(-1));
    assert.deepEqual(starValues, [...starValues].sort((a, b) => b - a));
    await page.locator('#code-filter').check();
    assert.equal(await count(), await page.locator('#papers .entry[data-code="true"]').count());
    await page.locator('#code-filter').uncheck();
    assert.deepEqual(await page.locator('#projects .entry').evaluateAll(rows => rows.map(row => row.id)), projectOrder);
    for (const width of [390, 320]) {
      await page.setViewportSize({width, height: 844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Reading list overflow at ${width}`);
    }
    await page.setViewportSize({width: 1280, height: 900});
    await page.locator('#clear').click();
    assert.deepEqual(await page.locator('#paper-sorted .reading-entry').evaluateAll(rows => rows.map(row => row.id)), paperOrder);
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
    assert.equal(await nojs.locator('.paper-toolbar:visible').count(), 0);
    for (const section of ['papers', 'benchmarks-1']) {
      const dates = await nojs.locator(`#${section} .reading-entry`).evaluateAll(rows => rows.map(row => Date.parse(row.dataset.date) || -1));
      assert.deepEqual(dates, [...dates].sort((a, b) => b - a));
    }
    assert.equal(await nojs.locator('.entry').count(), total);
    assert.deepEqual(errors, []);
    await page.route('https://img.shields.io/github/stars/**/*.json', route => route.fulfill({json: {value: 'repository not found', isError: true}}));
    await page.reload({waitUntil: 'domcontentloaded'});
    await page.locator('#papers .reading-stars').first().scrollIntoViewIfNeeded();
    await page.waitForFunction(() => document.querySelector('#papers .reading-stars').title.startsWith('Star count unavailable'));
    assert.equal(await page.locator('#papers .reading-stars').first().textContent(), '☆ —');
    await page.route('**/citations.json', route => route.fulfill({json: {source: 'Google Scholar', papers: {
      'ARXIV:2609.10522': {count: 0, url: 'https://scholar.google.com/scholar?q=2609.10522&hl=en', updated_at: '2026-09-13T00:00:00+00:00'},
      'ARXIV:2209.07753': {count: 2262, url: 'https://scholar.google.com/scholar?cluster=123&hl=en', updated_at: '2026-09-13T00:00:00+00:00'},
    }}}));
    await page.reload({waitUntil: 'domcontentloaded'});
    await page.waitForFunction(() => document.querySelector('[data-citation-id="ARXIV:2609.10522"]').textContent === '0');
    assert.match(await citations.getAttribute('title'), /^Google Scholar/);
    assert.equal(await page.locator('[data-citation-id="ARXIV:2209.07753"]').textContent(), '2,262');
    assert.equal(await page.locator('[data-citation-id="ARXIV:2209.07753"]').locator('..').getAttribute('href'), 'https://scholar.google.com/scholar?cluster=123&hl=en');
    console.log('Passed demo/code filters, comparison navigation and mobile scrolling, search, empty state, sorting/reset, category combinations, anchor reset, and no-JS fallback.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
