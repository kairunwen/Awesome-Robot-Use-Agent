import re
import unittest
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from build import build, ROOT, OUT


class WebsiteTest(unittest.TestCase):
    def test_readme_resources_survive_build(self):
        total = build()
        html = (OUT / 'index.html').read_text()
        page = BeautifulSoup(html, 'html.parser')
        self.assertEqual(len(page.select('.entry')), total)
        source = (ROOT / 'README.md').read_text()
        self.assertIn(f'/badge/Resources-{total}-', source)
        self.assertIn(f'/badge/Demo-{len(page.select(".entry[data-demo]"))}-', source)
        projects = source.split('## Projects\n', 1)[1].split('\n## ', 1)[0]
        project_source = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(projects), 'html.parser')
        self.assertEqual(len(page.select('#projects .entry')), len(project_source.select('tbody tr')))
        self.assertEqual([(h.name, h.get_text()) for h in page.select('#projects h3, #projects h4, #projects h5')], [
            ('h3', 'Open Source'), ('h4', 'Systems & Frameworks'),
            ('h4', 'Environment & Sandbox'), ('h4', 'Components'), ('h4', 'Other Tools'),
            ('h3', 'Social Demos'),
        ])
        self.assertEqual([h.get_text() for h in page.select('.group-heading h2')], ['Articles', 'Papers', 'Projects', 'Benchmarks'])
        self.assertEqual([h.get_text() for h in page.select('#papers h3')], ['Surveys', 'Models & Frameworks', 'Datasets', 'Benchmarks'])
        self.assertIsNotNone(page.select_one('#papers h3#benchmarks'))
        self.assertIsNotNone(page.select_one('section#benchmarks-1'))
        for ident, count in [('articles', 4), ('papers', 23), ('benchmarks-1', 4)]:
            self.assertEqual(len(page.select(f'#{ident} .entry')), count)
        self.assertNotIn('Closed-source multimodal model families', page.select_one('#projects').get_text())
        disclosures = page.select('#projects details.project-group')
        self.assertEqual([len(d.select('.entry')) for d in disclosures], [5, 8, 12, 4, 31])
        self.assertEqual([d.has_attr('open') for d in disclosures], [False, False, False, False, True])
        self.assertTrue(all(d.find('summary', recursive=False) for d in disclosures))
        self.assertEqual([d.select_one('summary > h4').get_text() for d in disclosures[:4]], ['Systems & Frameworks', 'Environment & Sandbox', 'Components', 'Other Tools'])
        self.assertNotRegex(page.select_one('#projects').get_text(), r'Browse \d+ resources')
        self.assertEqual(len(page.select('#projects .preview-entry img')), 31)
        self.assertEqual(len(page.select('#benchmarks-1 .preview-entry img')), 4)
        self.assertFalse(page.select('#papers .preview-table, #papers img'))
        for row in page.select('.preview-entry'):
            self.assertEqual(len(row.find_all('td', recursive=False)), 5)
            self.assertTrue(row.select_one('td:first-child a img')['alt'])
            self.assertIsNotNone(row.select_one('details.entry-notes summary'))
        tool_tables = [t for t in project_source.select('table') if 'Deployment & evidence' in [h.get_text() for h in t.select('th')]]
        self.assertEqual(sum(len(t.select('tbody tr')) for t in tool_tables), 9)
        for table in tool_tables:
            self.assertEqual([h.get_text() for h in table.select('th')], ['Resource', 'Role', 'Interface', 'Deployment & evidence', 'Official source'])
        # Folded notes must remain searchable but never leak into card summaries.
        for item in page.select('details.entry'):
            for note in item.select('.entry-notes'):
                note_text = note.get_text(' ', strip=True)
                self.assertNotIn(note_text, item.select_one('.entry-description').get_text())
        show = page.select_one('#papers .entry:has(.entry-notes)')
        self.assertIn('not independently deployed here', show.select_one('.entry-body').get_text())
        self.assertNotIn('not independently deployed here', show.select_one('.entry-description').get_text())
        self.assertEqual(len(page.select('.entry[data-demo]')), 31)
        self.assertEqual({e['data-demo'] for e in page.select('.entry[data-demo]')}, {'real', 'simulation', 'perception'})
        self.assertTrue(page.select('.entry[data-demo][data-code="true"]'))
        self.assertEqual({e['data-demo-intro'] for e in page.select('[data-demo-intro]')}, {'real', 'simulation', 'perception'})
        for table in project_source.select('table'):
            names = [r.find('strong').get_text() for r in table.select('tbody tr') if r.find('strong')]
            self.assertEqual(len(names), len(set(names)), 'Duplicate entry within a table')
        for img in page.select('.preview-entry img'):
            self.assertTrue(img['src'].startswith('https://'))
        self.assertIn('binary operator verdicts', page.select_one('#benchmarks-1').get_text())
        self.assertIsNone(page.find(id='resource'))
        posts = set(re.findall(r'https://x\.com/[^\s)]+', source))
        for url in posts:
            self.assertIn(url, html)
        ids = [tag['id'] for tag in page.select('[id]')]
        self.assertEqual(len(ids), len(set(ids)), 'Duplicate HTML IDs')
        for link in page.select('a[href^="#"]'):
            self.assertIn(link['href'][1:], ids)
        for word in ('19/20', '2/20', 'non-blind', 'unverified'):
            self.assertIn(word, html)
        self.assertNotIn('localhost', html)
        self.assertNotIn('127.0.0.1', html)
        self.assertNotIn('star-history', html)
        self.assertNotIn('img.shields.io/github/stars', html)


if __name__ == '__main__':
    unittest.main()
