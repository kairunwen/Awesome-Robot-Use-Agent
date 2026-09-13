"""Refresh optional reading-list covers; requires pdftoppm. Builds stay offline."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from build import read_readme

HERE = Path(__file__).resolve().parent


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
        return response.read()


def refresh():
    soup = read_readme((HERE.parent / 'README.md').read_text())
    manifest_path = HERE / 'previews.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    jobs = {}
    for title in ('Articles', 'Papers'):
        heading = next(h for h in soup.select('h2') if h.get_text() == title)
        for node in heading.next_siblings:
            if getattr(node, 'name', None) == 'h2':
                break
            if not getattr(node, 'select', None):
                continue
            targets = node.select('tbody tr') if title == 'Papers' else node.select('li')
            for item in targets:
                links = item.select('a[href]')
                source = next((a['href'] for a in links if a.get_text(strip=True) == 'Paper'), None) if title == 'Papers' else (links[0]['href'] if links else None)
                if source:
                    jobs[source] = title
    (HERE / 'previews').mkdir(exist_ok=True)

    def cover(job):
        url, kind = job
        cached = manifest.get(url)
        if cached and (cached['image'].startswith('https://') or (HERE / cached['image']).exists()):
            return url, cached
        try:
            if kind == 'Articles':
                page = BeautifulSoup(fetch(url), 'html.parser')
                image = page.select_one('meta[property="og:image"], meta[name="twitter:image"]')
                if not image or not image.get('content'):
                    raise ValueError('No official social cover')
                image_url = urljoin(url, image['content'])
                if not image_url.startswith('https://'):
                    raise ValueError('Cover must use HTTPS')
                return url, {'image': image_url, 'source': url}
            pdf = re.sub(r'arxiv.org/abs/', 'arxiv.org/pdf/', url)
            pdf = pdf.replace('github.com/', 'raw.githubusercontent.com/').replace('/blob/', '/')
            if '/pdf/' not in pdf and not pdf.lower().endswith('.pdf'):
                raise ValueError('No direct PDF source')
            data = fetch(pdf)
            if not data.startswith(b'%PDF'):
                raise ValueError('Source did not return a PDF')
            name = sha256(url.encode()).hexdigest()[:16]
            target = HERE / 'previews' / name
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'paper.pdf'
                path.write_bytes(data)
                subprocess.run(['pdftoppm', '-f', '1', '-singlefile', '-scale-to', '560', '-jpeg', str(path), str(target)], check=True, capture_output=True, timeout=45)
            return url, {'image': f'previews/{name}.jpg', 'source': pdf}
        except Exception as error:
            print(f'Cover unavailable: {url}: {error}', flush=True)
            return url, None

    with ThreadPoolExecutor(max_workers=6) as pool:
        for url, result in pool.map(cover, jobs.items()):
            if result:
                manifest[url] = result
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'{sum(url in manifest for url in jobs)}/{len(jobs)} covers available', flush=True)


if __name__ == '__main__':
    refresh()
