"""Check generated content consistency using only the Python standard library."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.schemas, self.questions, self.answers, self.links = [], [], [], []
        self.canonical = None
        self.noindex = False
        self.capture = None
        self.buffer = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.capture, self.buffer = 'schema', []
        elif tag == 'summary':
            self.capture, self.buffer = 'question', []
        elif tag == 'div' and a.get('class') == 'qbody':
            self.capture, self.buffer = 'answer', []
        if tag == 'a': self.links.append(a.get('href', ''))
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a['href']
        if tag == 'meta' and a.get('name') == 'robots': self.noindex = 'noindex' in a.get('content', '')
    def handle_data(self, data):
        if self.capture: self.buffer.append(data)
    def handle_endtag(self, tag):
        if (self.capture, tag) not in [('schema','script'), ('question','summary'), ('answer','div')]: return
        value = ''.join(self.buffer)
        if self.capture == 'schema': self.schemas.append(json.loads(value))
        elif self.capture == 'question': self.questions.append(' '.join(value.split()))
        else: self.answers.append(' '.join(value.split()))
        self.capture = None

urls = [n.text for n in ET.parse(root / 'sitemap.xml').findall('.//{*}loc')]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
for url in urls:
    path = urlsplit(url).path
    file = root / path.lstrip('/') / 'index.html'
    source = file.read_text()
    page = Page(source)
    assert page.canonical == url, f'Canonical mismatch: {file}'
    assert not page.noindex, f'Indexable page marked noindex: {file}'
    for schema in page.schemas:
        if schema.get('@type') == 'FAQPage':
            pairs = [(q['name'], q['acceptedAnswer']['text']) for q in schema['mainEntity']]
            assert pairs == list(zip(page.questions, page.answers)), f'FAQ mismatch: {file}'
    for link in page.links:
        dest = urlsplit(link).path
        if not urlsplit(link).netloc and dest.startswith('/'):
            target = root / dest.lstrip('/')
            if dest.endswith('/'): target /= 'index.html'
            assert target.exists(), f'Broken local link {link} in {file}'
    assert not re.search(r'\$(19|49|99)\b|Confirm current rates before publishing|included from the entry tier', source), f'Stale pricing: {file}'
wa = Page((root / 'whatsapp-business/index.html').read_text())
assert all('offers' not in s for s in wa.schemas), 'Quote-based page must not advertise an Offer'
for path in ['404.html', 'preview-standalone.html']:
    assert Page((root / path).read_text()).noindex, f'Utility page must be noindex: {path}'
assert not re.search(r'\$(19|49|99)\b|Starter|Growth|Scale', (root / 'llms.txt').read_text()), 'Stale llms pricing'
print(f'PASS: {len(urls)} sitemap pages; valid JSON-LD, FAQ parity, canonicals, local links, pricing removal and utility noindex')
