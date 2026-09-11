const search = document.querySelector('#search');
const clear = document.querySelector('#clear');
const groups = [...document.querySelectorAll('.resource-group')];
const entries = [...document.querySelectorAll('.entry')];
const filters = [...document.querySelectorAll('[data-filter]')];
const text = new Map(entries.map(entry => [entry, entry.textContent.toLowerCase()]));
let category = 'all';

function update() {
  const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  let count = 0;
  for (const group of groups) {
    let matches = 0;
    for (const entry of group.querySelectorAll('.entry')) {
      entry.hidden = !(category === 'all' || category === group.dataset.category) || !terms.every(term => text.get(entry).includes(term));
      if (!entry.hidden) matches++;
    }
    group.hidden = matches === 0;
    group.querySelector('.group-heading > span').textContent = String(matches).padStart(2, '0');
    count += matches;
  }
  const selected = filters.find(button => button.dataset.filter === category);
  for (const button of filters) button.setAttribute('aria-pressed', String(button === selected));
  document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'entry' : 'entries'} · ${category === 'all' ? 'all categories' : selected.firstElementChild.textContent}`;
  document.querySelector('#empty').hidden = count !== 0;
  clear.hidden = category === 'all' && terms.length === 0;
  document.querySelector('#resource-list').classList.toggle('is-filtering', !clear.hidden);
}

search.addEventListener('input', update);
for (const button of filters) button.addEventListener('click', () => {
  category = button.dataset.filter;
  update();
  document.querySelector('.catalogue-heading').scrollIntoView({block:'start'});
});
clear.addEventListener('click', () => { category = 'all'; search.value = ''; update(); search.focus(); });
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
    category = 'all'; search.value = ''; update();
  }
  if (target.matches('.guide')) target.querySelector('details').open = true;
  let parent = target.parentElement;
  while (parent) { if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement; }
  target.scrollIntoView({block:'start'});
}
window.addEventListener('hashchange', revealAnchor);
update();
if (location.hash) revealAnchor();
