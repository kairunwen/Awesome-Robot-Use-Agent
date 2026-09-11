import re
import unittest
from bs4 import BeautifulSoup
from build import build, ROOT, OUT


class WebsiteTest(unittest.TestCase):
    def test_readme_resources_survive_build(self):
        total = build()
        html = (OUT / 'index.html').read_text()
        page = BeautifulSoup(html, 'html.parser')
        self.assertEqual(len(page.select('.entry')), total)
        source = (ROOT / 'README.md').read_text()
        agents = source.split('## Agents and frameworks\n', 1)[1].split('\n## ', 1)[0]
        self.assertEqual(len(page.select('#agents-and-frameworks .entry')), len(re.findall(r'^\| (?:\d{4}-\d{2} \||\*\*)', agents, re.M)))
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


if __name__ == '__main__':
    unittest.main()
