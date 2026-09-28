#!/usr/bin/env python3
"""Audit report/ledger URLs; never equate a network restriction with a dead link."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
from urllib.parse import urlsplit, urlencode
import markdown

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.urls = set()
        self.feed(markdown.markdown(text))

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value.startswith(('https://', 'http://')):
                self.urls.add(value)


class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.in_title = False
        self.title = ''
        self.description = ''
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta' and (values.get('name') == 'description' or values.get('property') == 'og:description'):
            self.description = values.get('content', '')[:650]

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check(url):
    # GET catches sites that reject HEAD. Curl uses the host's certificate store.
    proc = subprocess.run(['curl', '-L', '-sS', '--max-time', '22',
                           '--connect-timeout', '8', '--retry', '1',
                           '-A', 'PaperRadar-LinkCheck/1.0',
                           '-w', '\nRADAR_STATUS\n%{http_code}\n%{url_effective}', url],
                          capture_output=True, text=True, errors='replace')
    body, _, status = proc.stdout.rpartition('\nRADAR_STATUS\n')
    parts = status.splitlines()
    code = int(parts[0]) if parts and parts[0].isdigit() else 0
    state = ('reachable' if 200 <= code < 300 else 'missing' if code in (404, 410)
             else 'restricted' if code in (401, 403, 429, 999) else 'unverified')
    result = dict(url=url, status=state, http=code,
                  final_url=parts[-1] if len(parts) > 1 else url)
    meta = Metadata(body)
    result['title'] = meta.title.strip()[:650]
    if state == 'reachable' and (not meta.title or any(x in meta.title.lower() for x in ('just a moment', 'access denied', 'page not found'))):
        result['status'] = 'unverified'
    if any(x in meta.title.lower() for x in ('verifying your browser', 'just a moment', 'access denied')):
        result['status'] = 'restricted'
    host = urlsplit(url).netloc
    if host in ('x.com', 'twitter.com', 'www.x.com') and '/status/' in url:
        if ' on X:' in meta.title or ' on Twitter:' in meta.title:
            result.update(status='x-original', evidence='Original X page includes author and post text')
        endpoint = 'https://publish.twitter.com/oembed?' + urlencode({'url': url, 'omit_script': 'true'})
        embed = subprocess.run(['curl', '-sS', '--max-time', '15', endpoint], capture_output=True, text=True, errors='replace')
        try:
            data = json.loads(embed.stdout)
            if data.get('html') and data.get('author_name'):
                result.update(status='x-oembed', author=data['author_name'],
                              evidence='Official X oEmbed returned post content and author')
        except (ValueError, TypeError):
            pass
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT/'site/link-audit.json')
    parser.add_argument('--workers', type=int, default=12)
    args = parser.parse_args()
    sources = {}
    for path in sorted([*(ROOT/'reports').glob('*.md'), *(ROOT/'state').glob('*.md')]):
        for url in Links(path.read_text()).urls:
            sources.setdefault(url, []).append(str(path.relative_to(ROOT)))
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {pool.submit(check, url): url for url in sources}
        for future in as_completed(pending):
            result = future.result()
            result['sources'] = sources[result['url']]
            results.append(result)
            if len(results) % 40 == 0:
                print(f'Checked {len(results)}/{len(sources)}', flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({'checked_at': datetime.now(timezone.utc).isoformat(),
                                   'method': 'HTTP GET; X original posts supplemented by official oEmbed',
                                   'links': sorted(results, key=lambda x: x['url'])},
                                  ensure_ascii=False, indent=2)+'\n')
    counts = {}
    for result in results:
        counts[result['status']] = counts.get(result['status'], 0) + 1
    print(json.dumps(counts), flush=True)


if __name__ == '__main__':
    main()
