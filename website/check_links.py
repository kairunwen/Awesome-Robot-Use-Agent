"""Check README links and previews without downloading media files."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from build import ROOT


def check(target):
    url, is_image = target
    try:
        request = Request(url, headers={'User-Agent': 'RUA-link-check/1.0'}, method='HEAD')
        try:
            response = urlopen(request, timeout=12)
        except HTTPError as error:
            if error.code not in (404, 405, 410):
                raise
            response = urlopen(Request(url, headers={'User-Agent': 'RUA-link-check/1.0'}), timeout=12)
        with response:
            content_type = response.headers.get_content_type()
            if is_image and not content_type.startswith('image/'):
                return 'REVIEW', url, 'Preview returned ' + content_type
        return 'OK', url, ''
    except HTTPError as error:
        return ('FAIL' if error.code in (404, 410) else 'REVIEW'), url, f'HTTP {error.code}'
    except (URLError, TimeoutError, OSError, ValueError) as error:
        return 'REVIEW', url, str(error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', action='append', help='Check only this URL; repeat for multiple URLs')
    args = parser.parse_args()
    page = BeautifulSoup(MarkdownIt('commonmark').enable('table').render((ROOT / 'README.md').read_text()), 'html.parser')
    targets = {}
    for element, attribute, is_image in [('a', 'href', False), ('img', 'src', True)]:
        for tag in page.select(f'{element}[{attribute}]'):
            url = tag[attribute]
            if urlparse(url).scheme in ('http', 'https'):
                targets[url] = targets.get(url, False) or is_image
    if args.url:
        targets = {url: targets.get(url, False) for url in args.url}
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, targets.items()))
    for status, url, detail in results:
        if status != 'OK':
            print(f'{status} {url} — {detail}')
    print(', '.join(f'{status}: {sum(r[0] == status for r in results)}' for status in ['OK', 'REVIEW', 'FAIL']))
    return int(any(r[0] == 'FAIL' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
