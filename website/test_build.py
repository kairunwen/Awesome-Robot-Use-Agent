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
        projects = source.split('## Projects\n', 1)[1].split('\n## ', 1)[0]
        project_source = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(projects), 'html.parser')
        self.assertEqual(len(page.select('#projects .entry')), len(project_source.select('tbody tr')))
        self.assertEqual([(h.name, h.get_text()) for h in page.select('#projects h3, #projects h4, #projects h5')], [
            ('h3', 'Open Source'), ('h4', 'Systems & Frameworks'),
            ('h4', 'Environment & Sandbox'), ('h4', 'Other Tools'), ('h4', 'Components'),
            ('h3', 'Social Demos'),
        ])
        self.assertEqual([h.get_text() for h in page.select('.group-heading h2')], ['Articles', 'Papers', 'Projects', 'Benchmarks'])
        self.assertEqual([h.get_text() for h in page.select('#papers h3')], ['Surveys', 'Models & Frameworks', 'Datasets', 'Benchmarks'])
        self.assertIsNotNone(page.select_one('#papers h3#benchmarks'))
        self.assertIsNotNone(page.select_one('section#benchmarks-1'))
        for ident, count in [('articles', 2), ('papers', 17), ('benchmarks-1', 4)]:
            self.assertEqual(len(page.select(f'#{ident} .entry')), count)
        self.assertNotIn('Closed-source multimodal model families', page.select_one('#projects').get_text())
        disclosures = page.select('#projects details.project-group')
        self.assertEqual([len(d.select('.entry')) for d in disclosures], [14, 4, 3, 10, 31])
        self.assertEqual([d.has_attr('open') for d in disclosures], [False, False, False, False, True])
        self.assertTrue(all(d.find('summary', recursive=False) for d in disclosures))
        self.assertEqual([d.select_one('summary > h4').get_text() for d in disclosures[:4]], ['Systems & Frameworks', 'Environment & Sandbox', 'Other Tools', 'Components'])
        self.assertNotRegex(page.select_one('#projects').get_text(), r'Browse \d+ resources')
        self.assertEqual(len(page.select('#projects .preview-entry img')), 31)
        self.assertEqual(len(page.select('#benchmarks-1 .preview-entry img')), 4)
        self.assertFalse(page.select('#papers .preview-table, #papers img'))
        for row in page.select('.preview-entry'):
            self.assertEqual(len(row.find_all('td', recursive=False)), 5)
            self.assertTrue(row.select_one('td:first-child a img')['alt'])
            self.assertIsNotNone(row.select_one('details.entry-notes summary'))
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
