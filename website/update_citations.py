"""Refresh verified citation records; optional Google Scholar via SerpApi."""
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
PUBLIC_URL = 'https://kairunwen.github.io/Awesome-Robot-Use-Agent/citations.json'
API_URL = 'https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,citationCount,url,externalIds'


def validate_record(record, source='Semantic Scholar'):
    pattern = (r'https://scholar\.google\.com/scholar\?(?:cluster=\d+|q=[^&#]+)&hl=en'
               if source == 'Google Scholar' else r'https://www\.semanticscholar\.org/paper/[a-f0-9]{40}')
    if (type(record.get('count')) is not int or not 0 <= record['count'] <= 2**53 - 1
            or not re.fullmatch(pattern, record.get('url', ''))
            or datetime.fromisoformat(record['updated_at']).tzinfo is None):
        raise ValueError('Invalid citation record')
    return record


def merge_records(previous, identifiers, response, now):
    if not isinstance(response, list) or len(response) != len(identifiers):
        raise ValueError('Unexpected Semantic Scholar batch response')
    papers = {key: validate_record(value) for key, value in previous.items() if key in identifiers}
    for identifier, result in zip(identifiers, response):
        if result is None:
            continue  # Unindexed is not zero; preserve any older verified record.
        if result.get('externalIds', {}).get('ArXiv') != identifier.removeprefix('ARXIV:'):
            raise ValueError(f'Paper ID mismatch: {identifier}')
        papers[identifier] = validate_record({'count': result.get('citationCount'),
            'url': result.get('url'), 'title': result.get('title'), 'updated_at': now})
    return papers


def scholar_record(identifier, title, response, now, expected_cluster=None):
    if response.get('error') or response.get('search_metadata', {}).get('status') != 'Success':
        raise ValueError('Scholar query failed')
    matches = {}
    normalize = lambda value: re.sub(r'[^\w]', '', value.casefold())
    for result in response.get('organic_results', []):
        # Exclude citation-only fragments that lack an actual paper link.
        if not result.get('link', '').startswith('https://'):
            continue
        urls = [result['link']] + [item.get('link', '') for item in result.get('resources', [])]
        ids = {match[1] for url in urls if (match := re.match(r'https?://arxiv.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?(?:[?#].*)?$', url))}
        if ids and ids != {identifier.removeprefix('ARXIV:')}:
            continue
        if not ids and normalize(result.get('title', '')) != normalize(title):
            continue
        links = result.get('inline_links', {})
        if not links.get('serpapi_cite_link'):
            continue
        # On a matched indexed result, Scholar omits Cited by when it has no citations.
        count = links['cited_by'].get('total') if 'cited_by' in links else 0
        cluster = str(links.get('versions', {}).get('cluster_id') or links.get('cited_by', {}).get('cites_id') or '')
        if expected_cluster and cluster != expected_cluster:
            continue  # Version listings can omit counts; keep the aggregate cluster record.
        query = f'cluster={cluster}' if cluster.isascii() and cluster.isdigit() else urlencode({'q': '"' + result['title'] + '"'})
        url = f'https://scholar.google.com/scholar?{query}&hl=en'
        if url in matches and matches[url]['count'] != count:
            return None
        matches[url] = validate_record({'count': count, 'title': result.get('title'),
            'url': url, 'updated_at': now}, 'Google Scholar')
    return next(iter(matches.values())) if len(matches) == 1 else None


def serpapi(path, key, **params):
    with urlopen('https://serpapi.com/' + path + '?' + urlencode(dict(params, api_key=key)), timeout=40) as response:
        data = json.load(response)
    if data.get('search_metadata', {}).get('status') == 'Success' and data.get('error') == "Google hasn't returned any results for this query.":
        data.pop('error')
    if data.get('error'):
        raise ValueError('SerpApi query failed')
    return data


def update_scholar(page, output, key):
    titles, papers, last_attempt = {}, {}, datetime.min.replace(tzinfo=timezone.utc)
    for node in page.select('[data-citation-id]'):
        titles.setdefault(node['data-citation-id'], node.find_parent('article').select_one('.reading-title').get_text(' ', strip=True))
    for source in (HERE / 'citations.json', output, PUBLIC_URL):
        try:
            if isinstance(source, Path):
                data = json.loads(source.read_text())
            else:
                with urlopen(source, timeout=15) as response:
                    data = json.load(response)
            attempted = datetime.fromisoformat(data.get('scholar_last_attempt_at', '1970-01-01T00:00:00+00:00'))
            last_attempt = max(last_attempt, attempted)
            for identifier, record in data['papers'].items():
                if identifier not in titles:
                    continue
                validate_record(record, data.get('source'))
                if record.get('title'):
                    titles[identifier] = record['title']
                if data.get('source') == 'Google Scholar' and (identifier not in papers or record['updated_at'] > papers[identifier]['updated_at']):
                    papers[identifier] = record
        except (OSError, ValueError, KeyError, TypeError):
            continue
    now = datetime.now(timezone.utc)
    if (now - last_attempt).total_seconds() >= 8 * 86400:
        last_attempt = now  # Persist even unsuccessful rounds to avoid spending quota on retries.
        try:
            account = serpapi('account.json', key)
            remaining = account.get('total_searches_left', 0)
            hourly = account.get('account_rate_limit_per_hour', 0)
            if type(remaining) is not int or type(hourly) is not int or min(remaining, hourly) < len(titles):
                raise ValueError('Insufficient quota for a complete round')
            for identifier, title in titles.items():
                old = papers.get(identifier, {})
                cluster = re.search(r'cluster=(\d+)', old.get('url', ''))
                query = {'cluster': cluster[1]} if cluster else {'q': old.get('search_query') or '"' + title.replace('"', '') + '"'}
                response = serpapi('search.json', key, engine='google_scholar', hl='en', **query)
                record = scholar_record(identifier, title, response, now.isoformat(), cluster[1] if cluster else None)
                if record and cluster and record['url'] != old['url']:
                    record = None
                if record:
                    if 'q' in query:
                        record['search_query'] = query['q']
                    papers[identifier] = record
                print(f'{identifier}: {record["count"] if record else "unmatched"}', flush=True)
        except Exception as error:
            # Request URLs contain the private key: never log exception messages or URLs.
            print(f'::warning::Google Scholar refresh stopped ({type(error).__name__}); retaining previous records.')
    data = {'source': 'Google Scholar', 'papers': papers} if papers else json.loads(output.read_text())
    data['scholar_last_attempt_at'] = last_attempt.isoformat()
    output.write_text(json.dumps(data, indent=2) + '\n')
    print(f'Google Scholar counts available for {len(papers)}/{len(titles)} unique papers.')


def update():
    output = HERE / 'dist' / 'citations.json'
    page = BeautifulSoup((HERE / 'dist' / 'index.html').read_text(), 'html.parser')
    if key := os.environ.get('SERPAPI_KEY', '').strip():
        update_scholar(page, output, key)
        return
    if json.loads(output.read_text()).get('source') == 'Google Scholar':
        print('SERPAPI_KEY unavailable; retaining the Google Scholar snapshot.')
        return
    identifiers = sorted({node['data-citation-id'] for node in page.select('[data-citation-id]')})
    papers = {}
    # Keep a bundled snapshot for first deployment and local previews.
    for source in (HERE / 'citations.json', output, PUBLIC_URL):
        try:
            if isinstance(source, Path):
                data = json.loads(source.read_text())
            else:
                with urlopen(source, timeout=15) as response:
                    data = json.load(response)
            if data.get('source') != 'Semantic Scholar':
                continue
            for key, value in data['papers'].items():
                record = validate_record(value)
                if key in identifiers and (key not in papers or record['updated_at'] > papers[key]['updated_at']):
                    papers[key] = record
        except (OSError, ValueError, KeyError, TypeError):
            continue
    try:
        request = Request(API_URL, data=json.dumps({'ids': identifiers}).encode(),
                          headers={'Content-Type': 'application/json', 'User-Agent': 'RUA-catalogue/1.0'})
        for attempt in range(3):
            try:
                with urlopen(request, timeout=30) as response:
                    results = json.load(response)
                break
            except HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise
                time.sleep(15 * (attempt + 1))
        papers = merge_records(papers, identifiers, results, datetime.now(timezone.utc).isoformat())
    except Exception as error:
        print(f'::warning::Citation refresh failed ({type(error).__name__} {getattr(error, "code", "")}); retaining previous counts and timestamps.')
    output.write_text(json.dumps({'source': 'Semantic Scholar', 'papers': papers}, indent=2) + '\n')
    print(f'Citation counts available for {len(papers)}/{len(identifiers)} unique papers.')


if __name__ == '__main__':
    update()
