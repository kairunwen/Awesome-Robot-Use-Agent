import re
import json
import unittest
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from build import build, read_readme, ROOT, OUT


class WebsiteTest(unittest.TestCase):
    def test_readme_resources_survive_build(self):
        total = build()
        html = (OUT / 'index.html').read_text()
        page = BeautifulSoup(html, 'html.parser')
        # Video CDN rejects a localhost Referer; media requests must omit it.
        self.assertIsNotNone(page.select_one('meta[name="referrer"][content="no-referrer"]'))
        self.assertEqual(len(page.select('.entry')), total)
        cucumber = page.select_one('.demo-card img[src="assets/demos/box2ai-cucumber-peeling.jpg"]')
        self.assertIsNotNone(cucumber)
        self.assertTrue((OUT / cucumber['src']).is_file())
        self.assertIsNone(page.select_one('.system-comparison'))
        self.assertFalse(any('⭐' in title.get_text() for title in page.select('#papers .reading-title')))
        starred = [entry.select_one('.reading-title').get_text() for entry in page.select('#papers .entry') if '⭐' in entry.select_one('.reading-publication').get_text()]
        self.assertEqual({title.split(':')[0] for title in starred}, {'ASPIRE', 'ENPIRE', 'CaP-X'})
        self.assertIsNotNone(page.find(id='models--frameworks'))
        bibtex = re.search(r'```bibtex\n(.*?)```', (ROOT / 'README.md').read_text(), re.S).group(1)
        code = page.select_one('#citation code.language-bibtex')
        self.assertEqual(code.get_text(), bibtex)
        self.assertFalse(code.select('span[style]'))
        self.assertIn('Awesome Computer Use Agent', page.select_one('#acknowledgements').get_text())
        source = (ROOT / 'README.md').read_text()
        gallery_source = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(source), 'html.parser')
        gallery_cards = gallery_source.select('.demo-gallery-card')
        self.assertEqual(len(gallery_cards), len(page.select('.demo-card')))
        self.assertTrue(all(1 <= len(row.find_all('td', recursive=False)) <= 3 for row in gallery_source.select('.demo-gallery tr')))
        for gallery in gallery_source.select('.demo-gallery'):
            self.assertTrue(all(len(row.find_all('td', recursive=False)) == 3 for row in gallery.select('tr')[:-1]))
            dates = [card.select_one('.layout-meta').get_text() for card in gallery.select('.demo-gallery-card') if card.get('data-demo-pinned') != 'true']
            self.assertEqual(dates, sorted(dates, reverse=True))
        self.assertTrue(all(card.select_one('.gallery-description > summary') for card in gallery_cards))
        for card in gallery_cards:
            self.assertEqual(len(card.select('.layout-tasks img')), 1)
            self.assertLessEqual(len(card.select('img[src*="img.shields.io"]')), 5)
            labels = [a.img['alt'] for a in card.select('.layout-links a')]
            self.assertIn(labels[0], ('Post', 'RedNote'))
            self.assertTrue(all(label in ('Post', 'RedNote', 'Video', 'Code · GitHub stars') for label in labels))
            self.assertEqual(len(card.select('details')), 1)
            self.assertEqual(card.select_one('summary img')['alt'], 'Details')
            outside = {a['href'] for a in card.select('.layout-links a[href]')}
            self.assertFalse(outside & {a['href'] for a in card.select_one('details').select('a[href]')})

        self.assertIn(f'/badge/Resources-{total}-', source)
        self.assertIn(f'/badge/Demo-{len(page.select(".entry[data-demo]"))}-', source)
        projects = source.split('## Projects\n', 1)[1].split('\n## ', 1)[0]
        project_source = read_readme(projects)
        self.assertEqual(len(page.select('#projects .entry')), len(project_source.select('tbody tr')))
        self.assertEqual([(h.name, h.get_text()) for h in page.select('#projects h3, #projects h4:not(.demo-title), #projects h5')], [
            ('h3', 'Open Source'), ('h4', 'Systems & Frameworks'),
            ('h4', 'Environment & Sandbox'), ('h4', 'Tools & Utilities'),
            ('h3', 'Social Demos'),
        ])
        self.assertEqual([h.get_text() for h in page.select('.group-heading h2')], ['Articles', 'Papers', 'Projects', 'Datasets', 'Benchmarks'])
        self.assertEqual([h.get_text() for h in page.select('#papers h3')], ['Surveys', 'Methods & Frameworks', 'Dataset Papers', 'Benchmarks'])
        self.assertIsNotNone(page.select_one('#papers h3#benchmarks'))
        self.assertIsNotNone(page.select_one('section#benchmarks-1'))
        for ident, count in [('articles', 6), ('papers', 51), ('datasets', 3), ('benchmarks-1', 18)]:
            self.assertEqual(len(page.select(f'#{ident} .entry')), count)
        self.assertNotIn('Closed-source multimodal model families', page.select_one('#projects').get_text())
        disclosures = page.select('#projects details.project-group')
        self.assertEqual([len(d.select('.entry')) for d in disclosures], [5, 9, 25, 43])
        self.assertEqual([d.has_attr('open') for d in disclosures], [False, False, False, True])
        self.assertTrue(all(d.find('summary', recursive=False) for d in disclosures))
        self.assertEqual([d.select_one('summary > h4').get_text() for d in disclosures[:3]], ['Systems & Frameworks', 'Environment & Sandbox', 'Tools & Utilities'])
        self.assertNotRegex(page.select_one('#projects').get_text(), r'Browse \d+ resources')
        self.assertEqual(len(page.select('#projects .demo-card')), 43)
        self.assertEqual(len(page.select('#benchmarks-1 .reading-cover img')), 18)
        self.assertEqual(len(page.select('#benchmarks-1 .reading-entry')), 18)
        self.assertFalse(page.select('#benchmarks-1 .preview-table'))
        benchmark_source = read_readme(source.rsplit('## Benchmarks\n', 1)[1].split('\n## ', 1)[0])
        for index, row in enumerate(benchmark_source.select('tbody tr')):
            card = page.select_one(f'#benchmarks-1-entry-{index}')
            cells = row.find_all('td')
            self.assertIn(cells[3].get_text(' ', strip=True), card.select_one('.reading-environment').get_text(' ', strip=True))
            self.assertEqual(cells[2].get_text(' ', strip=True).split(' · ')[0], card['data-date'])
            self.assertEqual(cells[0].find('img')['src'], card.select_one('.reading-cover img')['src'])
            for link in row.select('a[href]'):
                self.assertIsNotNone(card.find('a', href=link['href']), 'Benchmark source link lost')
            notes = cells[4].select_one('.entry-notes')
            for node in notes.select('summary, .layout-links'):
                node.decompose()
            self.assertIn(notes.get_text(' ', strip=True), card.select_one('.reading-details').get_text(' ', strip=True))
            self.assertFalse(card.select('.reading-details details, .reading-details .layout-links'))
        for section in ('papers', 'benchmarks-1'):
            cards = page.select(f'#{section} .reading-entry')
            dates = [(c['data-date'] + '-01-01')[:10] if c['data-date'] else '' for c in cards]
            self.assertEqual(dates, sorted(dates, reverse=True))
            self.assertEqual([b.get_text() for b in page.select(f'#{section} [data-reading-sort]')], ['Newest', 'Most stars', 'Most cited'])
        self.assertFalse(page.select('#papers .preview-table'))
        self.assertEqual(len(page.select('#papers .reading-entry')), 51)
        self.assertEqual(len(page.select('#articles .reading-entry')), 6)
        for card in page.select('.reading-entry'):
            link_labels = [a.get_text(strip=True) for a in card.select('.reading-links a')]
            priorities = [{'Paper': 0, 'Report': 1, 'Project': 2, 'PDF': 3}.get(label, 4) for label in link_labels]
            self.assertEqual(priorities, sorted(priorities))
            self.assertFalse(card.select('.reading-details .layout-links'))
            self.assertIsNotNone(card.select_one('.reading-title a[href]'))
            self.assertTrue(card.select_one('.reading-description').get_text(strip=True))
            self.assertTrue(card.select('.reading-links a[href]'))
            self.assertIsNotNone(card.select_one('.reading-details .entry-body'))
            image = card.select_one('.reading-cover img')
            if image and not image['src'].startswith('https://'):
                self.assertTrue((OUT / image['src']).is_file())
            if card['data-date']:
                meta = card.select_one('.reading-meta')
                self.assertEqual(meta.find().name, 'time')
                self.assertEqual(meta.find()['datetime'], card['data-date'])
            for logo in card.select('.institution-logo img'):
                self.assertTrue(logo['alt'])
                self.assertTrue((OUT / logo['src']).is_file())
        cap = page.select_one('.reading-title a[href="https://arxiv.org/abs/2209.07753"]').find_parent('article')
        self.assertEqual(cap['data-date'], '2022-09-16')
        self.assertIn('Jacky Liang, Wenlong Huang, Fei Xia, +5 authors', cap.select_one('.reading-meta').get_text())
        self.assertIn('Robotics at Google', cap.select_one('.reading-meta').get_text())
        self.assertIn('Andy Zeng', cap.select_one('.reading-details').get_text())
        self.assertEqual(cap.select_one('.reading-publication dd').get_text(), 'ICRA 2023')
        for card in page.select('#papers .reading-entry, #benchmarks-1 .reading-entry'):
            publication = card.select_one('.reading-details .reading-publication dd')
            self.assertIsNotNone(publication)
            self.assertIsNotNone(publication.select_one('a[href]'))
            self.assertRegex(publication.get_text(), r'20\d{2}')
        embodied = [c.select_one('.reading-publication').get_text(' ', strip=True) for c in page.select('.reading-entry') if c.select_one('[data-citation-id="ARXIV:2502.09560"]')]
        self.assertEqual(embodied, ['Publication ICML 2025'] * 2)
        # Thumbnail destinations do not replace visible paper/project badges.
        compact = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(source), 'html.parser')
        for name in ('EmbodiedBench', 'Embodied Agent Interface (EAI)'):
            row = compact.find('strong', string=name).find_parent('tr')
            labels = {img['alt'] for img in row.select('.layout-links img')}
            self.assertTrue({'Paper', 'Project', 'Data'} <= labels, name)
            self.assertEqual(row.select_one('.layout-links img')['alt'], 'Paper')
        for arxiv_id in ('2502.09560', '2410.07166'):
            card = page.select_one(f'#benchmarks-1 [data-citation-id="ARXIV:{arxiv_id}"]').find_parent('article')
            self.assertIsNotNone(card.select_one('.reading-links a[href*="github.io"]'))
            self.assertIsNotNone(card.select_one('a[href*="huggingface.co"]'))
        show_harness = page.select_one('#papers [data-citation-id="ARXIV:2609.10522"]').find_parent('article')
        self.assertNotIn('Show-Harness Data', page.select_one('#papers').get_text())
        dataset = page.select_one('#datasets .entry')
        self.assertEqual(dataset.select_one('.entry-title').get_text(), 'Show-Harness Data')
        self.assertIsNotNone(dataset.select_one('a[href="https://huggingface.co/datasets/showlab/Show-Harness-Data"]'))
        survey_pdf = page.select_one('.reading-links a[href="https://github.com/showlab/Awesome-Multimodal-Embodied-Agent/blob/main/assets/Awesome_Multimodal_Embodied_Agent.pdf"]')
        self.assertEqual(survey_pdf.get_text(), 'PDF')
        self.assertIn('ArXiv 2026', show_harness.select_one('.reading-publication').get_text())
        self.assertEqual(show_harness.get_text().count(show_harness.select_one('.reading-description').get_text()), 1)
        self.assertIsNone(show_harness.select_one('.reading-details details'))
        self.assertNotIn('not independently deployed here', show_harness.get_text())
        self.assertIn('GUMI demonstration collection', show_harness.get_text())
        self.assertIn('documented dependencies and site configuration', show_harness.get_text())
        for publication in page.select('.reading-publication'):
            self.assertNotRegex(publication.get_text(), r'(?i)unverified|not verified|not independently verified|maintainer|no conference or journal')
        self.assertIn('Extended version: Autonomous Robots · 2023', html)
        # Paper/project/code links stay outside the disclosure; evidence stays inside.
        doremi = page.select_one('.reading-title a[href="https://arxiv.org/abs/2307.00329"]').find_parent('article')
        self.assertEqual([a['href'] for a in doremi.select('.reading-links a')], [
            'https://arxiv.org/abs/2307.00329', 'https://sites.google.com/view/doremi-paper',
            'https://arxiv.org/pdf/2307.00329',
        ])
        self.assertNotIn('implementation availability is unverified', doremi.select_one('.reading-details').get_text())
        self.assertIn('disturbances or imperfect controllers', doremi.select_one('.reading-details').get_text())
        for field in page.select('.reading-details .entry-body > div > dt'):
            self.assertNotIn(field.get_text(), ['Paper', 'Code', 'Related links', 'Metadata source', 'Release date'])
        for row in page.select('.preview-entry'):
            self.assertEqual(len(row.find_all('td', recursive=False)), 5)
            self.assertTrue(row.select_one('td:first-child a img')['alt'])
            self.assertIsNotNone(row.select_one('details.entry-notes summary'))
        tool_tables = [t for t in project_source.select('table') if 'Deployment & evidence' in [h.get_text() for h in t.select('th')]]
        self.assertEqual(sum(len(t.select('tbody tr')) for t in tool_tables), 10)
        for table in tool_tables:
            self.assertEqual([h.get_text() for h in table.select('th')], ['Resource', 'Role', 'Interface', 'Deployment & evidence', 'Official source'])
            for row in table.select('tbody tr'):
                self.assertIsNotNone(row.find_all('td')[-1].select_one('a[href]'), 'Official source link missing')
        # Folded notes must remain searchable but never leak into card summaries.
        for item in page.select('details.entry'):
            for note in item.select('.entry-notes'):
                note_text = note.get_text(' ', strip=True)
                self.assertNotIn(note_text, item.select_one('.entry-description').get_text())
        show = show_harness
        self.assertEqual([a.find('span').get_text(strip=True) for a in show.select('.reading-resources a')], ['Data', 'Models', 'Code', 'Citation'])
        self.assertEqual([a['href'] for a in show.select('.reading-resources a')], [
            'https://huggingface.co/datasets/showlab/Show-Harness-Data',
            'https://huggingface.co/showlab/Show-Harness-VLMs',
            'https://github.com/showlab/Show-Harness',
            'https://arxiv.org/abs/2609.10522',
        ])
        self.assertFalse(page.select('.reading-resource.is-unlisted[href]'))
        self.assertEqual(len(page.select('#articles .reading-resources')), 6)
        self.assertNotIn('not independently deployed here', show.select_one('.entry-body').get_text())
        self.assertNotIn('not independently deployed here', show.select_one('.reading-description').get_text())
        source_demos = project_source.select('table:has(th:first-child)')
        source_demos = [t for t in source_demos if t.select_one('th').get_text() == 'Preview']
        cards = page.select('.demo-card')
        source_rows = [r for t in source_demos for r in t.select('tbody tr')]
        self.assertEqual(len(cards), len(source_rows))
        self.assertEqual(len(page.select('.demo-grid')), 3)
        for post_id in ('2099191606280863951', '2098813770730471827'):
            card = next(c for c in cards if post_id in str(c))
            self.assertIsNotNone(card.select_one('video source[src]'))
            self.assertNotIn('unverified', card.get_text().lower())
            self.assertTrue(card.select_one('.entry-notes').get_text(strip=True))
            self.assertEqual(card['data-demo'], 'simulation')
        task_labels = set()
        for card in cards:
            labels = json.loads(card['data-tasks'])
            self.assertTrue(labels, 'Every demo needs task labels')
            self.assertTrue(set(tag.get_text() for tag in card.select('.demo-task')) <= set(labels))
            task_labels.update(labels)
        self.assertEqual(task_labels, {option['value'] for option in page.select('#demo-task option') if option['value'] != 'all'})
        self.assertEqual(len(page.select('.demo-card[data-demo-pinned="true"]')), 1)
        self.assertEqual(cards[0]['data-demo-pinned'], 'true')
        self.assertIn('2098427488787730636', str(cards[0]))
        for row, card in zip(source_rows, cards):
            cells = row.find_all('td', recursive=False)
            for link in row.select('a[href]'):
                self.assertIn(link['href'], str(card), 'A demo source link was lost')
            self.assertEqual(card['data-date'], cells[2].get_text(strip=True))
            self.assertIn(cells[0].find('img')['src'].replace('&', '&amp;'), str(card))
            for linkbar in cells[4].select('.layout-links'):
                linkbar.decompose()
            self.assertEqual(card.select_one('.entry-notes').get_text(), cells[4].select_one('.entry-notes').get_text())
            primary_links = {a['href'] for a in card.select('.demo-links a')}
            self.assertFalse(primary_links & {a['href'] for a in card.select('.entry-notes a')})
            self.assertNotIn(card.select_one('.entry-notes').get_text(), card.select_one('.demo-description').get_text())
            video = card.select_one('video')
            if video:
                self.assertEqual(video['preload'], 'none')
                self.assertTrue(video.has_attr('controls') and video.has_attr('playsinline'))
                self.assertFalse(video.has_attr('autoplay'))
                self.assertTrue(video['aria-label'])
            else:
                self.assertEqual(card.select_one('img')['loading'], 'lazy')
        self.assertEqual(len(page.select('.entry[data-demo]')), 43)
        self.assertEqual({e['data-demo'] for e in page.select('.entry[data-demo]')}, {'real', 'simulation', 'perception'})
        self.assertTrue(page.select('.entry[data-demo][data-code="true"]'))
        self.assertEqual({e['data-demo-intro'] for e in page.select('[data-demo-intro]')}, {'real', 'simulation', 'perception'})
        for table in project_source.select('table'):
            names = [r.find('strong').get_text() for r in table.select('tbody tr') if r.find('strong')]
            self.assertEqual(len(names), len(set(names)), 'Duplicate entry within a table')
        for img in page.select('.preview-entry img'):
            self.assertTrue(img['src'].startswith('https://'))
        self.assertIn('progress scores from 0 to 100 in 25-point increments', page.select_one('#benchmarks-1').get_text())
        self.assertIsNone(page.find(id='resource'))
        rendered_source = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(source), 'html.parser')
        posts = {a['href'] for a in rendered_source.select('a[href^="https://x.com/"]')}
        for url in posts:
            self.assertIn(url, html)
        ids = [tag['id'] for tag in page.select('[id]')]
        self.assertEqual(len(ids), len(set(ids)), 'Duplicate HTML IDs')
        for link in page.select('a[href^="#"]'):
            self.assertIn(link['href'][1:], ids)
        for word in ('19/20', '2/20', 'non-blind'):
            self.assertIn(word, html)
        self.assertNotIn('better viewed on the', html.lower())
        self.assertNotIn('+1 authors', html)
        stationery = next(c for c in cards if 'StationeryBench' in c.get_text())
        self.assertIn('Pouring & pipetting', json.loads(stationery['data-tasks']))
        self.assertNotIn('localhost', html)
        self.assertNotIn('127.0.0.1', html)
        self.assertNotIn('star-history', html)
        for link in page.select('.reading-resources a[href^="https://github.com/"]'):
            if link.find('span').get_text(strip=True) != 'Code':
                continue
            repo = '/'.join(link['href'].split('/')[3:5])
            self.assertEqual(f'https://img.shields.io/github/stars/{repo}.json', link.select_one('.reading-stars')['data-stars-url'])


if __name__ == '__main__':
    unittest.main()
