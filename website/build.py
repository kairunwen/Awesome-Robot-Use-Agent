"""Build the resource website from the repository README."""
from pathlib import Path
from html import escape
import re
import shutil
import json
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'dist'
REPO = 'https://github.com/kairunwen/Awesome-Robot-Use-Agent'


def slug(text):
    return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')

def read_readme(source):
    """Read compact README tables into the website's catalogue fields."""
    soup = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(source), 'html.parser')
    for gallery in soup.select('table.demo-gallery'):
        table = soup.new_tag('table', attrs={'class': 'layout-benchmark layout-social'})
        table.append(soup.new_tag('thead'))
        body = soup.new_tag('tbody'); table.append(body)
        for card in gallery.select('td.demo-gallery-card'):
            row = soup.new_tag('tr')
            if card.has_attr('data-demo-pinned'):
                row['data-demo-pinned'] = card['data-demo-pinned']
            for field in ('preview', 'name', 'environment', 'description'):
                cell = card.select_one('.gallery-' + field)
                if field == 'environment':
                    tasks = cell.select_one('.layout-tasks')
                    if tasks and tasks.select('img[alt]'):
                        tasks.string = ' · '.join(badge['alt'] for badge in tasks.select('img[alt]'))
                    for badge in cell.select('img[alt]'):
                        badge.replace_with(badge['alt'])
                for detail in cell.select('details.gallery-description'):
                    detail.find('summary', recursive=False).decompose()
                    detail.unwrap()
                for note in cell.select('.demo-notes'):
                    note.name = 'details'
                    note['class'] = ['entry-notes']
                    summary = soup.new_tag('summary'); summary.string = 'Details'
                    note.insert(0, summary)
                cell.name = 'td'
                row.append(cell.extract())
            body.append(row)
        gallery.replace_with(table)
    for table in soup.select('table.layout-paper, table.layout-benchmark'):
        paper = 'layout-paper' in table.get('class', [])
        social = 'layout-social' in table.get('class', [])
        for img in table.select('.layout-links img'):
            label = img.get('alt', '').split(' · GitHub stars')[0]
            if 'github/stars/' in img['src'] and not re.search(r'\bcode\b', label, re.I):
                label = 'Code'
            img.replace_with(label)
        for row in table.select('tbody tr'):
            cells = row.find_all('td', recursive=False)
            name = cells[0] if paper else cells[1]
            metadata = name.select_one('.layout-meta')
            assert metadata is not None, name.get_text()
            date = metadata.get_text(' ', strip=True)
            metadata.extract()
            for br in name.select('br'):
                br.decompose()
            date_cell = soup.new_tag('td')
            date_cell.string = date.split(' · ')[0] if paper or social else date
            if paper and date.endswith('⭐'):
                date_cell.string += ' ⭐'
            if paper:
                # Keep link and description fields separate for the reading-list renderer.
                ordered = [date_cell, name, cells[2], cells[1]]
            else:
                ordered = [cells[0], name, date_cell, cells[2], cells[3]]
                linkbar = cells[3].select_one('.layout-links')
                if social and linkbar:
                    # Video links moved out of the thumbnail in the README.
                    video = next((a for a in linkbar.select('a[href]') if a.get_text(strip=True) in ('Video', '▶ Video')), None)
                    if video:
                        cells[0].append(BeautifulSoup(str(video), 'html.parser'))
                if linkbar:
                    notes = cells[3].find('details')
                    if notes:
                        notes.append(linkbar.extract())
            row.clear()
            for cell in ordered:
                row.append(cell)
        labels = ['Date', 'Name', 'Mechanism / release notes', 'Paper'] if paper else ['Preview', 'Name', 'Date', 'Environment', 'Description']
        table.thead.clear()
        head = soup.new_tag('tr')
        for label in labels:
            th = soup.new_tag('th'); th.string = label; head.append(th)
        table.thead.append(head)
    return soup


def build():
    previews_path = HERE / 'previews.json'
    previews = json.loads(previews_path.read_text()) if previews_path.exists() else {}
    metadata_path = HERE / 'metadata.json'
    reading_metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
    source = (ROOT / 'README.md').read_text()
    # This invitation belongs in the README; visitors are already on the website.
    source = re.sub(r'(, better| Better) viewed on the \[website\]\(https://kairunwen.github.io/Awesome-Robot-Use-Agent/#social-demos\)\.', lambda match: '.' if match[1].startswith(',') else '', source)
    soup = read_readme(source)
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
        if not is_preview and not img.find_parent(class_="guide-visual"):
            img.decompose()  # Keep resource previews and the guide illustration; remove badges.
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
        if title in ('Contents', 'Contributing', '🤝 Contributing', 'Star History'):
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
            if labels[0] == 'Preview' and table.has_attr('data-demo'):
                kind = table['data-demo']
                cards = []
                for row in table.select('tbody tr'):
                    cells = row.find_all('td', recursive=False)
                    assert len(cells) == 5, (title, labels)
                    cards.append(demo_card(cells, kind, ident, count, row.get('data-demo-pinned') == 'true'))
                    count += 1
                table.replace_with(BeautifulSoup(f'<div class="demo-grid" data-demo="{kind}">{"".join(cards)}</div>', 'html.parser'))
                continue
            if labels[0] == 'Preview':
                if title == 'Benchmarks':
                    cards = []
                    for row in table.select('tbody tr'):
                        preview, name_cell, year, environment, description_cell = row.find_all('td', recursive=False)
                        name = name_cell.get_text(' ', strip=True)
                        abstract = BeautifulSoup(description_cell.decode_contents(), 'html.parser')
                        for note in abstract.select('details.entry-notes'):
                            note.decompose()
                        links = row.select('a[href]')
                        primary = next((a['href'] for a in links if a.get_text(strip=True) == 'Paper'), links[0]['href'])
                        image = preview.find('img')
                        covers = {**previews, primary: {'image': image['src']}} if image else previews
                        fields = f'<div><dt>Environment</dt><dd>{environment.decode_contents()}</dd></div><div><dt>Description &amp; evidence</dt><dd>{description_cell.decode_contents()}</dd></div>'
                        card = reading_entry(name, abstract.get_text(' ', strip=True), year.get_text(' ', strip=True), fields, ident, count, links, covers, reading_metadata)
                        card = BeautifulSoup(card, 'html.parser')
                        card.select_one('.reading-cover')['href'] = preview.find('a', href=True)['href']
                        cards.append(str(card))
                        count += 1
                    table.replace_with(BeautifulSoup(''.join(cards), 'html.parser'))
                    continue
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
                if title == 'Papers':
                    rows.append(reading_entry(name, description, date, fields, ident, count, row.select('a[href]'), previews, reading_metadata))
                else:
                    rows.append(entry(name, description, date, fields, ident, count))
                count += 1
            listing = ''.join(rows)
            if title == 'Papers':
                listing = f'<div class="paper-list">{listing}</div>'
            table.replace_with(BeautifulSoup(listing, 'html.parser'))
        if title == 'Articles':
            for listing in list(content.find_all('ul')):
                rows = []
                for item in listing.find_all('li', recursive=False):
                    first = item.find('a')
                    if not first:
                        continue
                    name = first.get_text(' ', strip=True)
                    description = item.get_text(' ', strip=True).removeprefix(name).strip(' —')
                    metadata, separator, description = description.partition('. ')
                    if not separator:
                        description, metadata = metadata, ''
                    rows.append(reading_entry(name, description, metadata, '<div><dt>Source and context</dt><dd>'+item.decode_contents()+'</dd></div>', ident, count, item.select('a[href]'), previews, reading_metadata))
                    count += 1
                listing.replace_with(BeautifulSoup(''.join(rows), 'html.parser'))
        demo_heading = content.find(id='social-demos')
        if demo_heading:
            tasks = sorted({task for card in content.select('.demo-card') for task in json.loads(card['data-tasks'])})
            task_options = ''.join(f'<option value="{escape(task, quote=True)}">{escape(task)}</option>' for task in tasks)
            for navigation in content.select('p:has(> a[href="#real-robot-demonstrations"]):has(> a[href="#simulation-demonstrations"])'):
                navigation.decompose()  # The website provides demo filter buttons above.
            demo_heading.insert_after(BeautifulSoup('''<div class="demo-toolbar" hidden>
<div class="demo-tabs" role="group" aria-label="Demo scenes">
<button type="button" data-demo-kind="demos" aria-pressed="true">All demos <span class="demo-tab-count">0</span></button>
<button type="button" data-demo-kind="real" aria-pressed="false">Real robots <span class="demo-tab-count">0</span></button>
<button type="button" data-demo-kind="simulation" aria-pressed="false">Simulation <span class="demo-tab-count">0</span></button>
<button type="button" data-demo-kind="perception" aria-pressed="false">Perception &amp; reconstruction <span class="demo-tab-count">0</span></button>
</div><label class="demo-task-filter">Task <select id="demo-task"><option value="all">All tasks</option>TASK_OPTIONS</select></label><span id="demo-count" role="status" aria-live="polite"></span></div>'''.replace('TASK_OPTIONS', task_options), 'html.parser'))
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
        if title in ('Papers', 'Benchmarks'):
            prefix = 'paper' if title == 'Papers' else 'benchmark'
            cards = content.select('.reading-entry')
            for card in cards:
                card.extract()
            cards.sort(key=lambda card: (card['data-date'] + '-01-01')[:10] if card['data-date'] else '', reverse=True)
            content = f'''<div class="paper-toolbar" hidden>
<div class="paper-sort" role="group" aria-label="Sort {title.lower()}">
<button type="button" data-reading-sort="newest" aria-pressed="true">Newest</button>
<button type="button" data-reading-sort="stars" aria-pressed="false">Most stars</button>
<button type="button" data-reading-sort="citations" aria-pressed="false">Most cited</button>
</div><span class="reading-sort-status" id="{prefix}-sort-status" role="status" aria-live="polite"></span></div>
<div class="reading-outline" hidden>{content}</div><div class="reading-sorted" id="{prefix}-sorted">{''.join(map(str, cards))}</div>'''
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
    if (HERE / 'citations.json').exists():
        shutil.copyfile(HERE / 'citations.json', OUT / 'citations.json')
    shutil.copytree(ROOT / 'assets' / 'demos', OUT / 'assets' / 'demos', dirs_exist_ok=True)
    shutil.copytree(ROOT / 'assets' / 'previews', OUT / 'assets' / 'previews', dirs_exist_ok=True)
    shutil.copyfile(HERE / 'logo-warm.png', OUT / 'logo.png')
    if (HERE / 'previews').exists():
        shutil.copytree(HERE / 'previews', OUT / 'previews', dirs_exist_ok=True)
    if (HERE / 'institutions').exists():
        shutil.copytree(HERE / 'institutions', OUT / 'institutions', dirs_exist_ok=True)
    return total


def reading_entry(name, description, metadata, fields, category, index, links, previews, reading_metadata):
    primary = next((a['href'] for a in links if a.get_text(strip=True) == 'Paper'), links[0]['href'] if links else '#papers')
    cover = previews.get(primary)
    record = reading_metadata.get(primary, {})
    kind = 'Article' if category == 'articles' else 'Benchmark' if category == 'benchmarks-1' else 'Paper'
    media = f'<span class="reading-cover-text"><span>{kind}</span><strong>{escape(name)}</strong><span>Robot Use Agent collection</span></span>'
    if cover:
        media += f'<img src="{escape(cover["image"], quote=True)}" alt="{escape(name, quote=True)} — {"first page" if kind == "Paper" else "official preview" if kind == "Benchmark" else "official cover"}" loading="lazy" decoding="async">'
    sources, seen = [], set()
    resources = {'Data': [], 'Models': [], 'Code': [], 'Citation': []}
    for link in links:
        if link.find_parent('details', class_='entry-notes') and not link.find_parent(class_='layout-links'):
            continue  # Contextual references remain beside the notes they support.
        url = link['href']
        label = link.get_text(' ', strip=True)
        if not label or url in seen:
            continue
        seen.add(url)
        if label == name:
            label = 'Read article' if kind == 'Article' else 'Paper'
        types = []
        if re.search(r'\b(data|datasets?)\b', label, re.I) or url.startswith('https://huggingface.co/datasets/'):
            types.append('Data')
        if re.search(r'\bcode\b', label, re.I) and url.startswith('https://github.com/'):
            types.append('Code')
        if re.search(r'\b(models?|weights|checkpoints?)\b', label, re.I):
            types.append('Models')
        for resource in types:
            resources[resource].append((url, label))
        if types:
            continue
        tone = 'code' if 'code' in label.lower() else 'paper' if label == 'Paper' else 'source'
        sources.append((label, f'<a class="reading-link reading-link-{tone}" href="{escape(url, quote=True)}">{escape(label)}</a>'))
    citation = next((a['href'] for a in links if a.get_text(strip=True) == 'Paper'), record.get('date_source') or (primary if kind in ('Article', 'Benchmark') else None))
    if citation:
        resources['Citation'].append((citation, 'Citation source'))
    icons = {
        'Data': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
        'Code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
        'Models': '<path d="m12 2 9 5v10l-9 5-9-5V7Zm0 10 9-5M12 12 3 7m9 5v10"/>',
        'Citation': '<path d="M12 5c-3-2-6-2-10-1v15c4-1 7-1 10 1 3-2 6-2 10-1V4c-4-1-7-1-10 1Zm0 0v15"/>',
    }
    actions = []
    for resource, targets in resources.items():
        actions.append('<div class="reading-resource-group">')
        icon = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icons[resource]}</svg>'
        if targets:
            for url, label in targets:
                stars = ''
                if resource == 'Code':
                    repo = '/'.join(url.removeprefix('https://github.com/').split('/')[:2])
                    stars = f'<span class="reading-stars" data-stars-url="https://img.shields.io/github/stars/{escape(repo, quote=True)}.json" title="GitHub stars">☆ —</span>'
                if resource == 'Citation':
                    arxiv = re.fullmatch(r'https://arxiv.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?', url)
                    identifier = f' data-citation-id="ARXIV:{arxiv[1]}"' if arxiv else ''
                    stars = f'<span class="reading-citations"{identifier} title="Citation count unavailable">—</span>'
                actions.append(f'<a class="reading-resource" href="{escape(url, quote=True)}" title="{escape(label, quote=True)}" aria-label="{escape(name + ": " + label, quote=True)}">{icon}<span>{resource}</span>{stars}</a>')
        else:
            actions.append(f'<span class="reading-resource is-unlisted" title="No {resource.lower()} link listed">{icon}<span>{resource}</span><span class="sr-only"> — no link listed</span></span>')
        actions.append('</div>')
    # Source links already appear in the visible link bar or resource panel.
    detail_fields = BeautifulSoup(fields, 'html.parser')
    for linkbar in detail_fields.select('.layout-links'):
        linkbar.decompose()
    for paragraph in detail_fields.select('.layout-description'):
        if paragraph.get_text(' ', strip=True) == description:
            paragraph.decompose()
    for note in detail_fields.select('details.entry-notes'):
        summary = note.find('summary', recursive=False)
        if summary:
            summary.decompose()
            first = note.find(string=lambda text: bool(text.strip()))
            if first and description and first.lstrip().startswith(description):
                first.replace_with(first.lstrip()[len(description):].lstrip())
            note.unwrap()
    for field in list(detail_fields.find_all('div', recursive=False)):
        label = field.find('dt').get_text(strip=True)
        if label in ('Paper', 'Code', 'Related links'):
            field.decompose()
        elif label == 'Sources':
            remainder = BeautifulSoup(field.dd.decode_contents(), 'html.parser')
            for link in remainder.select('a'):
                link.decompose()
            if not remainder.get_text(strip=True).strip(' ·'):
                field.decompose()
    fields = str(detail_fields)
    date_match = re.search(r'\b\d{4}(?:-\d{2}(?:-\d{2})?)?\b', metadata)
    date = record.get('date', date_match.group() if date_match else '')
    authors = record.get('authors', [])
    institutions = record.get('institutions', [])
    meta = [f'<time datetime="{escape(date, quote=True)}">{escape(date)}</time>'] if date else []
    if authors:
        extra = len(authors) - 3
        author_text = ', '.join(authors[:3]) + (f', +{extra} {"author" if extra == 1 else "authors"}' if extra > 0 else '')
        meta.append(f'<span class="reading-authors" title="{escape(", ".join(authors), quote=True)}">{escape(author_text)}</span>')
        fields = f'<div><dt>Authors</dt><dd>{escape(", ".join(authors))}</dd></div>' + fields
    if institutions:
        names = [i['name'] for i in institutions]
        institution_text = ', '.join(names[:2]) + (f' +{len(names)-2}' if len(names) > 2 else '')
        meta.append(f'<span class="reading-affiliations" title="{escape(", ".join(names), quote=True)}">{escape(institution_text)}</span>')
        fields = f'<div><dt>Institutions</dt><dd>{escape(", ".join(names))}</dd></div>' + fields
    if not authors and not institutions:
        remainder = metadata.replace(date, '').strip(' ·') if date else metadata
        if remainder and not (kind == 'Benchmark' and '(' in metadata):
            meta.append(escape(remainder))
    elif category == 'articles':
        meta.append(escape(metadata.split(' · ')[-1]))
    if kind == 'Benchmark' and '(' in metadata:
        meta.append(escape(metadata))
    if kind in ('Paper', 'Benchmark'):
        publication = record.get('publication')
        if publication:
            venue = 'ArXiv' if publication['venue'].lower() == 'arxiv' else publication['venue']
            label = f'{venue} {publication["year"]}'
            label += " · ⭐" if metadata.endswith("⭐") else ""
            publication_html = f'<a href="{escape(publication["source"], quote=True)}">{escape(label)}</a>'
            if publication.get('note'):
                publication_html += f' — {escape(publication["note"])}'
        else:
            arxiv_source = next((u for u in (primary, record.get('date_source', ''), record.get('source', '')) if 'arxiv.org/' in u), '')
            label = f'ArXiv {date[:4]}' if arxiv_source else f'Online resource {date[:4]}'
            label += " · ⭐" if metadata.endswith("⭐") else ""
            publication_html = escape(label)
        fields = f'<div class="reading-publication"><dt>Publication</dt><dd>{publication_html}</dd></div>' + fields
    environment = detail_fields.find('dt', string='Environment')
    environment_html = f'<p class="reading-meta reading-environment"><strong>Environment:</strong> {environment.find_next_sibling("dd").decode_contents()}</p>' if environment else ''
    # Environment is already visible; retain only additional context in Details.
    rendered_fields = BeautifulSoup(fields, 'html.parser')
    for field in rendered_fields.find_all('div', recursive=False):
        label = field.find('dt')
        if label and (label.get_text() in ('Environment', 'Source and context') or not field.dd.get_text(strip=True)):
            field.decompose()
    fields = str(rendered_fields)
    logos = []
    for institution in institutions[:2]:
        if institution.get('logo'):
            logos.append(f'<a class="institution-logo" href="{escape(institution["url"], quote=True)}" title="{escape(institution["name"], quote=True)}"><img src="{escape(institution["logo"], quote=True)}" alt="{escape(institution["name"], quote=True)}" width="20" height="20" loading="lazy"></a>')
    for url, label in [(record.get('source'), 'PDF' if re.search(r'/pdf/|\.pdf(?:[?#]|$)', record.get('source', ''), re.I) else 'Source'),
                       (record.get('date_source'), 'Paper' if kind == 'Benchmark' and 'arxiv.org/' in record.get('date_source', '') else 'Source')]:
        if url and url not in seen:
            sources.append((label, f'<a class="reading-link reading-link-source" href="{escape(url, quote=True)}">{label}</a>'))
            seen.add(url)
    sources.sort(key=lambda item: {'Paper': 0, 'Report': 1, 'Project': 2, 'PDF': 3}.get(item[0], 4))
    cover_accessibility = f'aria-label="Preview for {escape(name, quote=True)}"' if kind == 'Benchmark' else 'tabindex="-1" aria-hidden="true"'
    return f'''<article class="entry reading-entry" id="{category}-entry-{index}" data-date="{escape(date, quote=True)}">
<a class="reading-cover reading-cover-{category}" href="{escape(primary, quote=True)}" {cover_accessibility}>{media}</a>
<div class="reading-content"><h4 class="reading-title"><a href="{escape(primary, quote=True)}">{escape(name)}</a>{' ' + ''.join(logos) if logos else ''}</h4>
<p class="reading-meta">{' · '.join(meta) if meta else kind}</p>
{environment_html}
<p class="reading-description">{escape(description)}</p>
<nav class="reading-links" aria-label="Sources for {escape(name, quote=True)}">{''.join(html for label, html in sources)}</nav>
<details class="reading-details"><summary>Details &amp; sources</summary><dl class="entry-body">{fields}</dl></details>
</div><nav class="reading-resources" aria-label="Resources for {escape(name, quote=True)}">{''.join(actions)}</nav></article>'''


def demo_card(cells, kind, category, index, pinned=False):
    preview, name_cell, date_cell, environment, description = cells
    annotation = environment.select_one('.layout-tasks')
    tasks = annotation.get_text(strip=True).removeprefix('Task: ').split(' · ') if annotation else []
    if annotation:
        annotation.extract()
    task_labels = ''.join(f'<span class="demo-task">{escape(task)}</span>' for task in tasks)
    # Additional documented tasks remain searchable without adding more badges.
    for paragraph in description.select('.entry-notes p'):
        text = paragraph.get_text(' ', strip=True)
        if text.startswith('Tasks: '):
            tasks = list(dict.fromkeys(tasks + text[7:].rstrip('.').split(', ')))
    name = name_cell.get_text(' ', strip=True)
    author, separator, task = name.partition(' — ')
    date = date_cell.get_text(strip=True)
    image = preview.find('img')
    post = next((a['href'] for a in description.select('.layout-links a[href]') if a.get_text(strip=True).lower().endswith('post') or a.get_text(strip=True) == 'RedNote'), preview.find('a', href=True)['href'])
    video = next((a['href'] for a in preview.select('a[href]') if a.get_text(strip=True) in ('Video', '▶ Video')), None)
    extra_links = []
    for linkbar in description.select('.layout-links'):
        extra_links.extend(str(a) for a in linkbar.select('a[href]') if a['href'] not in (post, video))
        linkbar.decompose()
    notes = description.select_one('details.entry-notes')
    notes_html = str(notes.extract()) if notes else ''
    if video:
        media = f'<video controls playsinline preload="none" poster="{escape(image["src"], quote=True)}" aria-label="{escape(name, quote=True)}"><source src="{escape(video, quote=True)}" type="video/mp4"><a href="{escape(video, quote=True)}">Watch video</a></video>'
    else:
        media = f'<a href="{escape(post, quote=True)}"><img src="{escape(image["src"], quote=True)}" alt="{escape(image.get("alt", name), quote=True)}" loading="lazy" decoding="async"></a>'
    return f'''<article class="entry demo-card" id="{category}-entry-{index}" data-date="{escape(date)}" data-demo="{kind}" data-demo-pinned="{str(pinned).lower()}" data-tasks="{escape(json.dumps(tasks), quote=True)}">
<div class="demo-media">{media}</div>
<div class="demo-content"><div class="demo-meta"><span class="demo-environment">{escape(environment.get_text(' ', strip=True))}</span><time datetime="{escape(date)}">{escape(date)}</time></div>
<p class="demo-author">{escape(author) if separator else 'Community demo'}</p>
<h4 class="demo-title">{escape(task if separator else name)}</h4>
<div class="demo-tasks" aria-label="Task categories">{task_labels}</div>
<div class="demo-description">{description.decode_contents()}</div>
<p class="demo-media-error" hidden>Video unavailable here. Use the original post below.</p>
<div class="demo-links"><a href="{escape(post, quote=True)}">Open original post ↗</a>{f'<a href="{escape(video, quote=True)}">Video ↗</a>' if video else ''}{''.join(extra_links)}</div>
{notes_html}</div></article>'''


def entry(name, description, date, fields, category, index):
    return f'''<details class="entry" data-date="{escape(date)}" id="{category}-entry-{index}">
<summary><span class="entry-title">{escape(name)}</span><span class="entry-description">{escape(description)}</span><span class="entry-date">{escape(date) if date else '—'}</span><span class="entry-toggle" aria-hidden="true">+</span></summary>
<dl class="entry-body">{fields}</dl></details>'''


if __name__ == '__main__':
    print(f'Built {build()} catalogue entries → {OUT / "index.html"}')
