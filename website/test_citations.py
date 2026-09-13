import unittest
import json
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup

from update_citations import merge_records, scholar_record, update_scholar, serpapi

class CitationTest(unittest.TestCase):
    def test_scholar_matching_zero_failure_and_cooldown(self):
        identifier, title = 'ARXIV:2209.07753', 'Code as Policies'
        now = '2026-09-13T00:00:00+00:00'
        result = {'title': title, 'link': 'https://arxiv.org/abs/2209.07753',
                  'inline_links': {'serpapi_cite_link': 'https://serpapi.com/search.json',
                                   'cited_by': {'total': 2262, 'cites_id': '123'}}}
        payload = {'search_metadata': {'status': 'Success'}, 'organic_results': [result]}
        record = scholar_record(identifier, title, payload, now)
        self.assertEqual(record['count'], 2262)
        alternative = dict(result, inline_links=dict(result['inline_links'], cited_by={'total': 5, 'cites_id': '456'}))
        self.assertIsNone(scholar_record(identifier, title, dict(payload, organic_results=[result, alternative]), now))
        self.assertEqual(scholar_record(identifier, title, dict(payload, organic_results=[result, alternative]), now, '123')['count'], 2262)
        self.assertIsNone(scholar_record('ARXIV:2609.10522', title, payload, now))
        fragment = dict(result); fragment.pop('link')
        self.assertIsNone(scholar_record(identifier, title, dict(payload, organic_results=[fragment]), now))
        for count in [-1, True, None, '5']:
            result['inline_links']['cited_by']['total'] = count
            with self.assertRaises(ValueError):
                scholar_record(identifier, title, payload, now)
        del result['inline_links']['cited_by']
        self.assertEqual(scholar_record(identifier, title, payload, now)['count'], 0)
        empty = {'search_metadata': {'status': 'Success'}, 'error': "Google hasn't returned any results for this query."}
        with patch('update_citations.urlopen', return_value=BytesIO(json.dumps(empty).encode())):
            self.assertIsNone(scholar_record(identifier, title, serpapi('search.json', 'test-key'), now))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'citations-out.json'
            output.write_text(json.dumps({'source': 'Google Scholar', 'papers': {identifier: record}}))
            page = BeautifulSoup(f'<article><h4 class="reading-title">{title}</h4><span data-citation-id="{identifier}"></span></article>', 'html.parser')
            with patch('update_citations.HERE', root), patch('update_citations.urlopen', side_effect=OSError('offline')), patch('update_citations.serpapi', side_effect=[{'total_searches_left': 250, 'account_rate_limit_per_hour': 50}, OSError('secret URL')]) as fetch:
                update_scholar(page, output, 'test-key')
                self.assertEqual(json.loads(output.read_text())['papers'][identifier], record)
                update_scholar(page, output, 'test-key')
                self.assertEqual(fetch.call_count, 2, 'Cooldown must prevent repeated paid requests')
            output.write_text(json.dumps({'source': 'Semantic Scholar', 'papers': {}}))
            with patch('update_citations.HERE', root), patch('update_citations.urlopen', side_effect=OSError('offline')), patch('update_citations.serpapi', return_value={'total_searches_left': 0, 'account_rate_limit_per_hour': 50}) as fetch:
                update_scholar(page, output, 'test-key')
                self.assertEqual(fetch.call_count, 1, 'Exhausted quota must prevent queries')
                self.assertEqual(json.loads(output.read_text())['source'], 'Semantic Scholar')

    def test_exact_ids_counts_and_stale_fallback(self):
        old = {'count': 12, 'url': 'https://www.semanticscholar.org/paper/' + 'a' * 40,
               'updated_at': '2026-09-12T00:00:00+00:00'}
        ids = ['ARXIV:2209.07753', 'ARXIV:2609.10522', 'ARXIV:2608.16590']
        result = {'externalIds': {'ArXiv': '2609.10522'}, 'citationCount': 0,
                  'url': old['url'], 'title': 'Example'}
        now = '2026-09-13T00:00:00+00:00'
        merged = merge_records({ids[0]: old}, ids, [None, result, None], now)
        self.assertEqual(merged[ids[0]], old)
        self.assertEqual(merged[ids[1]]['count'], 0)
        self.assertEqual(merged[ids[1]]['updated_at'], now)
        self.assertNotIn(ids[2], merged)
        for bad in (-1, True, None, '12'):
            with self.assertRaises(ValueError):
                merge_records({}, [ids[1]], [dict(result, citationCount=bad)], now)
        with self.assertRaises(ValueError):
            merge_records({}, [ids[0]], [result], now)


if __name__ == '__main__':
    unittest.main()
