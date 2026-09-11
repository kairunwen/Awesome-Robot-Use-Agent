"""Build the resource website from the repository README."""
from pathlib import Path
from html import escape
import re
import shutil
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'dist'
REPO = 'https://github.com/kairunwen/Awesome-Robot-Use-Agent'


def slug(text):
    return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')


def build():
    soup = BeautifulSoup(MarkdownIt('commonmark').enable('table').render((ROOT / 'README.md').read_text()), 'html.parser')
    for summary in soup.select('summary'):
        summary.decompose()
    for details in soup.select('details'):
        details.unwrap()
    for img in soup.select('img'):
        img.decompose()  # Text links remain; no external badge requests in the catalogue.
    for link in list(soup.select('a')):
        if not link.get_text(strip=True):
            link.decompose()
    for link in soup.select('a[href]'):
        href = link['href']
        if href == 'CONTRIBUTING.md':
            link['href'] = REPO + '/blob/main/CONTRIBUTING.md'
    for heading in soup.select('h1,h2,h3,h4'):
        heading['id'] = slug(heading.get_text())
    for paragraph in soup.select('p'):
        if paragraph.get_text(strip=True) == 'Back to top':
            paragraph.decompose()

    groups = []
    for heading in soup.find_all('h2'):
        nodes = []
        for node in heading.next_siblings:
            if getattr(node, 'name', None) == 'h2':
                break
            nodes.append(str(node))
        groups.append((heading.get_text(), heading['id'], BeautifulSoup(''.join(nodes), 'html.parser')))

    sections, nav, total = [], [], 0
    guide = ''
    for title, ident, content in groups:
        if title in ('Contents', 'Contributing'):
            continue
        if title == 'Getting started':
            # The catalogue supplies its own counts and navigation.
            glance = content.find(id='at-a-glance')
            if glance:
                for node in list(glance.next_siblings):
                    node.extract()
                glance.extract()
            guide = str(content)
            continue
        count = 0
        if title == 'Research papers':
            content.find('p').string = 'Grouped by agent mechanism, newest first within each group. Dates refer to the first arXiv release. Expand a row for paper, code, and project links. Summaries reflect author reports; unverified releases are marked explicitly.'
        for table in list(content.select('table')):
            labels = [c.get_text(' ', strip=True) for c in table.select('thead th')]
            if title == 'Benchmarks and environments' and labels == ['Dimension', 'Record']:
                table['class'] = 'guide-table'
                continue
            rows = []
            for row in table.select('tbody tr'):
                cells = row.find_all('td', recursive=False)
                assert len(cells) == len(labels), (title, labels)
                has_date = labels[0] == 'Date'
                name_index = 1 if has_date else 0
                primary = cells[name_index]
                strong = primary.find('strong')
                name = strong.get_text(' ', strip=True) if strong else primary.get_text(' ', strip=True)
                description_index = len(cells)-1 if title == 'Research papers' else name_index+1
                description = cells[description_index].get_text(' ', strip=True)
                date = cells[0].get_text(strip=True) if has_date else ''
                fields = ''.join(f'<div><dt>{escape(label)}</dt><dd>{cell.decode_contents()}</dd></div>' for label, cell in zip(labels, cells) if cell is not primary and label != 'Date')
                project = ''.join(str(a) for a in primary.find_all('a'))
                if project:
                    fields = f'<div><dt>Project</dt><dd>{project}</dd></div>' + fields
                rows.append(entry(name, description, date, fields, ident, count))
                count += 1
            table.replace_with(BeautifulSoup(''.join(rows), 'html.parser'))
        if title in ('Blogs and demos', 'Resource'):
            for listing in list(content.find_all('ul')):
                rows = []
                for item in listing.find_all('li', recursive=False):
                    first = item.find('a')
                    if not first:
                        continue
                    name = first.get_text(' ', strip=True)
                    description = item.get_text(' ', strip=True).removeprefix(name).strip(' —')
                    rows.append(entry(name, description, '', '<div><dt>Source and context</dt><dd>'+item.decode_contents()+'</dd></div>', ident, count))
                    count += 1
                listing.replace_with(BeautifulSoup(''.join(rows), 'html.parser'))
        # Comparison guidance remains available without competing with resources.
        comparison = content.find(id='how-to-compare-systems')
        if comparison:
            wrapper = content.new_tag('details', attrs={'class':'reading-notes'})
            summary = content.new_tag('summary'); summary.string = 'How to compare systems'
            wrapper.append(summary)
            for node in list(comparison.next_siblings):
                wrapper.append(node.extract())
            comparison.replace_with(wrapper)
        sections.append(f'<section class="resource-group" id="{ident}" data-category="{ident}"><header class="group-heading"><h2>{escape(title)}</h2><span>{count:02d}</span></header>{content}</section>')
        nav.append(f'<button type="button" data-filter="{ident}" aria-pressed="false"><span>{escape(title)}</span><span>{count}</span></button>')
        total += count

    template = (HERE / 'template.html').read_text()
    for key, value in {'GUIDE':guide, 'SECTIONS':''.join(sections), 'NAV':''.join(nav), 'TOTAL':str(total), 'REPO':REPO}.items():
        template = template.replace('{{'+key+'}}', value)
    assert not re.search(r'\{\{[A-Z]+\}\}', template)
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(template)
    for asset in ('style.css', 'app.js'):
        shutil.copyfile(HERE / asset, OUT / asset)
    shutil.copyfile(HERE / 'logo-warm.png', OUT / 'logo.png')
    return total


def entry(name, description, date, fields, category, index):
    return f'''<details class="entry" data-date="{escape(date)}" id="{category}-entry-{index}">
<summary><span class="entry-title">{escape(name)}</span><span class="entry-description">{escape(description)}</span><span class="entry-date">{escape(date) if date else '—'}</span><span class="entry-toggle" aria-hidden="true">+</span></summary>
<dl class="entry-body">{fields}</dl></details>'''


if __name__ == '__main__':
    print(f'Built {build()} catalogue entries → {OUT / "index.html"}')
