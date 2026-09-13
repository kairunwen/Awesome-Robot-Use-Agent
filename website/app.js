const search = document.querySelector('#search');
const clear = document.querySelector('#clear');
const groups = [...document.querySelectorAll('.resource-group')];
const entries = [...document.querySelectorAll('.entry')];
const starRequests = new Map();
function loadStars(counter) {
  const url = counter.dataset.starsUrl;
  if (!starRequests.has(url)) starRequests.set(url, fetch(url, {signal: AbortSignal.timeout(10000)})
    .then(response => {
      if (!response.ok) throw new Error('Stars unavailable');
      return response.json();
    })
    .then(data => {
      const match = typeof data.value === 'string' && data.value.match(/^(\d+(?:,\d{3})*)(?:\.(\d+))?([kmbt])?$/i);
      if (data.isError || !match) throw new Error('Invalid star count');
      const count = Number(match[1].replaceAll(',', '') + (match[2] ? '.' + match[2] : ''))
        * ({k: 1e3, m: 1e6, b: 1e9, t: 1e12}[match[3]?.toLowerCase()] || 1);
      if (!Number.isSafeInteger(count) || count < 0) throw new Error('Invalid star count');
      return {count, label: data.value};
    }).catch(() => null));
  return starRequests.get(url).then(data => {
    if (data) {
      counter.dataset.count = data.count;
      counter.textContent = `☆ ${data.label}`;
      counter.title = `${data.label} GitHub stars`;
    } else counter.title = 'Star count unavailable; open the repository to check';
  });
}
const starObserver = new IntersectionObserver(items => {
  for (const item of items) {
    if (!item.isIntersecting) continue;
    starObserver.unobserve(item.target);
    loadStars(item.target);
  }
}, {rootMargin: '200px'});
document.querySelectorAll('[data-stars-url]').forEach(counter => starObserver.observe(counter));
fetch('citations.json')
  .then(response => {
    if (!response.ok) throw new Error('Citations unavailable');
    return response.json();
  })
  .then(data => {
    const pattern = data.source === 'Google Scholar'
      ? /^https:\/\/scholar\.google\.com\/scholar\?(?:cluster=\d+|q=[^&#]+)&hl=en$/
      : data.source === 'Semantic Scholar' ? /^https:\/\/www\.semanticscholar\.org\/paper\/[a-f0-9]{40}$/ : null;
    if (!pattern) return;
    for (const counter of document.querySelectorAll('[data-citation-id]')) {
      const record = data.papers?.[counter.dataset.citationId];
      if (!record || !Number.isSafeInteger(record.count) || record.count < 0
          || !pattern.test(record.url)
          || !Number.isFinite(Date.parse(record.updated_at))) continue;
      counter.dataset.count = record.count;
      counter.textContent = record.count.toLocaleString('en-US');
      counter.title = `${data.source} · updated ${new Date(record.updated_at).toLocaleString()}`;
      const link = counter.closest('a');
      link.href = record.url;
      link.title = counter.title;
      link.setAttribute('aria-label', `${link.getAttribute('aria-label')} — ${record.count} citations on ${data.source}`);
    }
    for (const list of readingLists) if (list.order === 'citations') sortReadingList(list);
  })
  .catch(() => {}); // Leave unavailable counts as a dash.
for (const image of document.querySelectorAll('.reading-cover img')) {
  image.addEventListener('error', () => { image.hidden = true; });
  if (image.complete && !image.naturalWidth) image.hidden = true;
}
const filters = [...document.querySelectorAll('[data-filter]')];
const text = new Map(entries.map(entry => [entry, entry.textContent.toLowerCase()]));
const demoFilter = document.querySelector('#demo-filter');
const codeFilter = document.querySelector('#code-filter');
const demoOrder = document.querySelector('#demo-order');
const demoTables = [...document.querySelectorAll('.demo-grid')].map(body => ({body, rows: [...body.children]}));
document.querySelector('#discovery-tools').hidden = false;
const demoTabs = [...document.querySelectorAll('[data-demo-kind]')];
const demoToolbar = document.querySelector('.demo-toolbar');
if (demoToolbar) demoToolbar.hidden = false;
const videos = [...document.querySelectorAll('.demo-card video')];
for (const video of videos) {
  video.addEventListener('play', () => {
    for (const other of videos) if (other !== video) other.pause();
  });
  const showError = () => { video.closest('.demo-card').querySelector('.demo-media-error').hidden = false; };
  video.addEventListener('error', showError);
  video.querySelector('source').addEventListener('error', showError);
}
let category = 'all';

const readingLists = ['papers', 'benchmarks-1'].map(id => {
  const section = document.getElementById(id);
  section.querySelector('.paper-toolbar').hidden = false;
  return {section, body: section.querySelector('.reading-sorted'), rows: [...section.querySelectorAll('.reading-entry')], order: 'newest', loading: false};
});
function readingValue(row, order) {
  if (order === 'newest') {
    const date = row.dataset.date;
    const value = Date.parse(date.length === 4 ? date + '-01-01' : date.length === 7 ? date + '-01' : date);
    return Number.isFinite(value) ? value : -1;
  }
  const counters = row.querySelectorAll(order === 'stars' ? '.reading-stars[data-count]' : '.reading-citations[data-count]');
  // Multiple code repositories: rank by the largest star count, not their sum.
  return Math.max(-1, ...[...counters].map(counter => Number(counter.dataset.count)));
}
function sortReadingList(list) {
  // Stable ties preserve release order; unavailable values rank last.
  list.body.append(...[...list.rows].sort((a, b) => readingValue(b, list.order) - readingValue(a, list.order)));
  for (const button of list.section.querySelectorAll('[data-reading-sort]')) button.setAttribute('aria-pressed', String(button.dataset.readingSort === list.order));
  list.section.querySelector('.reading-sort-status').textContent = list.order === 'stars' && list.loading ? 'Loading stars…' : '';
}
for (const list of readingLists) {
  for (const button of list.section.querySelectorAll('[data-reading-sort]')) button.addEventListener('click', async () => {
    list.order = button.dataset.readingSort;
    if (list.order === 'stars') {
      list.loading = true;
      sortReadingList(list); update();
      await Promise.all(list.rows.flatMap(row => [...row.querySelectorAll('[data-stars-url]')]).map(loadStars));
      list.loading = false;
    }
    sortReadingList(list); update();
  });
  sortReadingList(list);
}

function sortDemos() {
  for (const {body, rows} of demoTables) {
    const sorted = [...rows];
    if (demoOrder.value !== 'curated') sorted.sort((a, b) => demoOrder.value === 'newest' ? b.dataset.date.localeCompare(a.dataset.date) : a.dataset.date.localeCompare(b.dataset.date));
    for (const row of sorted) body.append(row);
  }
}
function resetFilters() {
  category = 'all'; search.value = ''; demoFilter.value = 'all'; codeFilter.checked = false; demoOrder.value = 'curated'; sortDemos(); for (const list of readingLists) { list.order = 'newest'; sortReadingList(list); }
}

function update() {
  const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  let count = 0;
  for (const group of groups) {
    let matches = 0;
    for (const entry of group.querySelectorAll('.entry')) {
      entry.hidden = !(category === 'all' || category === group.dataset.category) || !terms.every(term => text.get(entry).includes(term))
        || (demoFilter.value !== 'all' && !(demoFilter.value === 'demos' ? entry.dataset.demo : entry.dataset.demo === demoFilter.value))
        || (codeFilter.checked && entry.dataset.code !== 'true');
      if (!entry.hidden) matches++;
      else entry.querySelector('video')?.pause();
    }
    for (const table of group.querySelectorAll('.preview-scroll, .demo-grid')) table.hidden = !table.querySelector('.entry:not([hidden])');
    for (const intro of group.querySelectorAll('[data-demo-intro]')) intro.hidden = !group.querySelector(`.entry[data-demo="${intro.dataset.demoIntro}"]:not([hidden])`);
    for (const disclosure of group.querySelectorAll('.project-group')) {
      disclosure.hidden = !disclosure.querySelector('.entry:not([hidden])');
      if ((terms.length || demoFilter.value !== 'all' || codeFilter.checked) && !disclosure.hidden) disclosure.open = true;
    }
    group.hidden = matches === 0;
    group.querySelector('.group-heading > span').textContent = String(matches).padStart(2, '0');
    count += matches;
  }
  for (const button of demoTabs) button.setAttribute('aria-pressed', String(button.dataset.demoKind === (demoFilter.value === 'all' ? 'demos' : demoFilter.value)));
  const demoCount = document.querySelectorAll('.demo-card:not([hidden])').length;
  if (demoToolbar) {
    demoToolbar.hidden = category !== 'all' && category !== 'projects';
    document.querySelector('#demo-count').textContent = `${demoCount} demos`;
  }
  const selected = filters.find(button => button.dataset.filter === category);
  for (const button of filters) button.setAttribute('aria-pressed', String(button === selected));
  document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'entry' : 'entries'} · ${category === 'all' ? 'all categories' : selected.firstElementChild.textContent}`;
  document.querySelector('#empty').hidden = count !== 0;
  clear.hidden = category === 'all' && terms.length === 0 && demoFilter.value === 'all' && !codeFilter.checked && demoOrder.value === 'curated' && readingLists.every(list => list.order === 'newest');
  document.querySelector('#resource-list').classList.toggle('is-filtering', terms.length > 0 || demoFilter.value !== 'all' || codeFilter.checked);
}

for (const button of demoTabs) button.addEventListener('click', () => {
  category = 'all';
  demoFilter.value = button.dataset.demoKind;
  update();
});
for (const disclosure of document.querySelectorAll('.project-group')) disclosure.addEventListener('toggle', () => {
  if (!disclosure.open) for (const video of disclosure.querySelectorAll('video')) video.pause();
});
search.addEventListener('input', update);
for (const control of [demoFilter, codeFilter]) control.addEventListener('change', update);
demoOrder.addEventListener('change', () => { sortDemos(); update(); });
for (const button of filters) button.addEventListener('click', () => {
  category = button.dataset.filter;
  update();
  document.querySelector('.catalogue-heading').scrollIntoView({block:'start'});
});
clear.addEventListener('click', () => { resetFilters(); update(); search.focus(); });
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !event.target.closest('input,textarea,[contenteditable]')) {
    event.preventDefault(); search.focus();
  }
  if (event.key === 'Escape' && event.target === search) { search.value = ''; update(); }
});
function revealAnchor() {
  let anchor;
  try { anchor = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(anchor);
  if (!target) return;
  if (target.closest('.resource-group') && !clear.hidden) {
    resetFilters(); update();
  }
  if (target.matches('.guide')) target.querySelector('details').open = true;
  let parent = target.parentElement;
  while (parent) { if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement; }
  (target.closest('.reading-outline') ? target.closest('.resource-group') : target).scrollIntoView({block:'start'});
}
window.addEventListener('hashchange', revealAnchor);
update();
if (location.hash) revealAnchor();

async function loadViews() {
  const counter = document.querySelector('#view-count');
  try {
    const response = await fetch('views.json', {cache: 'no-cache', signal: AbortSignal.timeout(10000)});
    if (!response.ok) throw new Error('Views unavailable');
    const data = await response.json();
    if (data.source !== 'ga4' || !Number.isSafeInteger(data.total) || data.total < 0
        || data.start_date !== '2026-09-13' || !Number.isFinite(Date.parse(data.updated_at))) throw new Error('Invalid views');
    counter.textContent = data.total.toLocaleString('en-US');
    counter.title = `Google Analytics page views since ${data.start_date}. Updated ${new Date(data.updated_at).toLocaleString()}. Refreshed hourly; GA processing may be delayed.`;
  } catch {
    counter.title = 'Google Analytics view count temporarily unavailable';
  }
}
loadViews();
