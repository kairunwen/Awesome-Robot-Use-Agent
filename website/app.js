const search = document.querySelector('#search');
const clear = document.querySelector('#clear');
const groups = [...document.querySelectorAll('.resource-group')];
const entries = [...document.querySelectorAll('.entry')];
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

function sortDemos() {
  for (const {body, rows} of demoTables) {
    const sorted = [...rows];
    if (demoOrder.value !== 'curated') sorted.sort((a, b) => demoOrder.value === 'newest' ? b.dataset.date.localeCompare(a.dataset.date) : a.dataset.date.localeCompare(b.dataset.date));
    for (const row of sorted) body.append(row);
  }
}
function resetFilters() {
  category = 'all'; search.value = ''; demoFilter.value = 'all'; codeFilter.checked = false; demoOrder.value = 'curated'; sortDemos();
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
  clear.hidden = category === 'all' && terms.length === 0 && demoFilter.value === 'all' && !codeFilter.checked && demoOrder.value === 'curated';
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
  target.scrollIntoView({block:'start'});
}
window.addEventListener('hashchange', revealAnchor);
update();
if (location.hash) revealAnchor();
