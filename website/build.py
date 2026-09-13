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
    star_callout = soup.find(id="star-callout").extract()
    # Section borders are styled outside collapsible content on the website.
    for divider in soup.find_all("hr", recursive=False):
        divider.decompose()
    for summary in soup.select('summary'):
        if not set(summary.parent.get('class', [])) & {'project-group', 'entry-notes'}:
            summary.decompose()
    for details in soup.select('details'):
        if not set(details.get('class', [])) & {'project-group', 'entry-notes'}:
            details.unwrap()
    for img in soup.select('img'):
        cell = img.find_parent('td')
        table = img.find_parent('table')
        is_preview = cell and not cell.find_previous_sibling('td') and table.find('th').get_text(strip=True) == 'Preview'
        if not is_preview:
            img.decompose()  # Keep resource previews; remove badges and star charts.
    for link in list(soup.select('a[href]')):
        if not link.get_text(strip=True) and not link.find(['picture', 'img']):
            link.decompose()
    for link in soup.select('a[href]'):
        href = link['href']
        if href == 'CONTRIBUTING.md':
            link['href'] = REPO + '/blob/main/CONTRIBUTING.md'
    # The template provides the citation anchor.
    for anchor in soup.select('a#citation'):
        anchor.decompose()
    heading_ids = set()
    for heading in soup.select('h1,h2,h3,h4,h5,h6'):
        base = slug(heading.get_text())
        ident = base
        suffix = 0
        while ident in heading_ids:
            suffix += 1
            ident = f'{base}-{suffix}'
        heading['id'] = ident
        heading_ids.add(ident)
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
    citation = ''
    acknowledgements = ''
    for title, ident, content in groups:
        if title in ('Contents', 'Contributing', 'Star History'):
            continue
        if title in ('Citation', '📖 Citation'):
            citation = str(content)
            continue
        if title == '🙏 Acknowledgements':
            acknowledgements = str(content)
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
        for anchor, kind in [('real-robot-demonstrations', 'real'), ('simulation-demonstrations', 'simulation'), ('perception-and-reconstruction', 'perception')]:
            marker = content.find(id=anchor)
            if marker:
                demo_table = marker.find_next('table')
                demo_table['data-demo'] = kind
                marker_block = marker.parent if marker.parent.name == 'p' else marker
                for node in marker_block.next_siblings:
                    if node is demo_table:
                        break
                    if getattr(node, 'name', None) == 'p':
                        node['data-demo-intro'] = kind
        for table in list(content.select('table')):
            labels = [c.get_text(' ', strip=True) for c in table.select('thead th')]
            if labels[0] == 'Preview':
                table['class'] = 'preview-table'
                for row in table.select('tbody tr'):
                    cells = row.find_all('td', recursive=False)
                    assert len(cells) == len(labels), (title, labels)
                    row['class'] = ['entry', 'preview-entry']
                    row['id'] = f'{ident}-entry-{count}'
                    row['data-date'] = cells[2].get_text(strip=True)
                    if table.has_attr('data-demo'):
                        row['data-demo'] = table['data-demo']
                    count += 1
                table.wrap(content.new_tag('div', attrs={'class': 'preview-scroll', 'tabindex': '0', 'role': 'region', 'aria-label': f'{title} previews'}))
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
                description_index = labels.index('Mechanism / release notes') if 'Mechanism / release notes' in labels else name_index+1
                abstract = BeautifulSoup(cells[description_index].decode_contents(), 'html.parser')
                for note in abstract.select('details.entry-notes'):
                    note.decompose()
                description = abstract.get_text(' ', strip=True)
                date = cells[0].get_text(strip=True) if has_date else ''
                fields = ''.join(f'<div><dt>{escape(label)}</dt><dd>{cell.decode_contents()}</dd></div>' for label, cell in zip(labels, cells) if cell is not primary and label != 'Date')
                project = ''.join(str(a) for a in primary.find_all('a'))
                if project:
                    fields = f'<div><dt>Related links</dt><dd>{project}</dd></div>' + fields
                rows.append(entry(name, description, date, fields, ident, count))
                count += 1
            table.replace_with(BeautifulSoup(''.join(rows), 'html.parser'))
        if title == 'Articles':
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
        for item in content.select('.entry'):
            item['data-code'] = str(any(re.search(r'\bcode\b', a.get_text(), re.I) and a.get('href', '').startswith('https://github.com/') for a in item.select('a[href]'))).lower()
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
    for key, value in {'GUIDE':guide, 'CITATION':citation, 'STAR':str(star_callout), 'ACKNOWLEDGEMENTS':acknowledgements, 'SECTIONS':''.join(sections), 'NAV':''.join(nav), 'TOTAL':str(total), 'REPO':REPO}.items():
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
