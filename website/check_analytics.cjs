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
