// node website/check_analytics.cjs — no network calls or dependencies.
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
const html = readFileSync(__dirname + '/template.html', 'utf8');
const code = html.match(/<script id="google-analytics">([\s\S]*?)<\/script>/)[1];
for (const [url, enabled] of [
  ['http://127.0.0.1:8892/', false],
  ['https://example.com/Awesome-Robot-Use-Agent/', false],
  ['https://kairunwen.github.io/another-project/', false],
  ['https://kairunwen.github.io/Awesome-Robot-Use-Agent/?v=test#datasets', true],
  ['https://kairunwen.github.io/Awesome-Robot-Use-Agent/index.html', true],
]) {
  const scripts = [], window = {};
  runInNewContext(code, {location:new URL(url), window, document:{createElement:() => ({}), head:{append:tag => scripts.push(tag)}}});
  assert.equal(scripts.length, enabled ? 1 : 0);
  if (enabled) {
    assert.equal(scripts[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-BH0XB730MF');
    assert.equal(scripts[0].async, true);
    const configs = window.dataLayer.filter(args => args[0] === 'config');
    assert.equal(configs.length, 1);
    assert.equal(configs[0][1], 'G-BH0XB730MF');
    assert.equal(configs[0][2].page_location, 'https://kairunwen.github.io/Awesome-Robot-Use-Agent/');
    assert.equal(configs[0][2].allow_google_signals, false);
  } else assert.equal(window.dataLayer, undefined);
}
assert.ok(!html.includes('busuanzi'));
console.log('Passed production-only GA4 initialization and canonical page-view configuration.');

(async () => {
  const app = readFileSync(__dirname + '/app.js', 'utf8');
  const views = app.slice(app.indexOf('async function loadViews()'));
  const valid = {source:'ga4', total:1234, start_date:'2026-09-13', updated_at:'2026-09-13T10:00:00+00:00'};
  for (const [data, ok, expected] of [
    [valid, true, '1,234'], [{...valid, total:0}, true, '0'],
    [{...valid, total:-1}, true, '—'], [{...valid, total:'1234'}, true, '—'],
    [{...valid, updated_at:'bad date'}, true, '—'], [valid, false, '—'],
    [new Error('Network failure'), true, '—'],
  ]) {
    const counter = {textContent:'—'};
    await runInNewContext(views, {
      document:{querySelector:() => counter}, AbortSignal,
      fetch:async (url, options) => {
        assert.equal(url, 'views.json');
        assert.equal(options.cache, 'no-cache');
        if (data instanceof Error) throw data;
        return {ok, json:async () => data};
      },
    });
    assert.equal(counter.textContent, expected);
    assert.ok(counter.title.includes(expected === '—' ? 'unavailable' : 'Google Analytics page views since'));
  }
  assert.ok(html.indexOf('id="view-count"') > html.indexOf('{{STAR}}'));
  assert.match(html, /id="view-count"[\s\S]*?<\/p>\s*<\/body>/);
  console.log('Passed view display, zero, invalid data, network failure, and footer position checks.');
})().catch(error => { console.error(error); process.exitCode = 1; });
