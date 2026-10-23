"""Validate HTML, local references, anchors, and deployment exclusions."""

from fnmatch import fnmatchcase
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

import html5lib

ROOT = Path(__file__).resolve().parents[1]
pages = sorted(ROOT.glob('*.html'))
errors = []
documents = {}


def fail(path, message):
    errors.append(f'{path.relative_to(ROOT)}: {message}')


for page in pages:
    parser = html5lib.HTMLParser(namespaceHTMLElements=False)
    doc = parser.parse(page.read_text(encoding='utf-8'))
    documents[page] = doc
    for (line, column), code, detail in parser.errors:
        fail(page, f'HTML error at {line}:{column}: {code} {detail}')
    ids = [e.get('id') for e in doc.iter() if e.get('id')]
    if len(ids) != len(set(ids)):
        fail(page, 'duplicate element IDs')
    if not doc.get('lang'):
        fail(page, 'missing document language')
    if not doc.findtext('head/title', '').strip():
        fail(page, 'missing page title')
    if doc.find('.//main') is None:
        fail(page, 'missing main landmark')

for page, doc in documents.items():
    for element in doc.iter():
        if element.tag == 'style' or element.get('style'):
            fail(page, 'page styles should live in a stylesheet')
        if element.tag == 'iframe' and not element.get('title'):
            fail(page, 'embedded frame needs a title')
        if element.tag == 'a' and element.get('target') == '_blank':
            if 'noopener' not in element.get('rel', '').split():
                fail(page, 'new-tab link missing noopener')
        for attr in ('href', 'src', 'poster'):
            value = element.get(attr)
            if not value:
                continue
            url = urlsplit(value.strip())
            if url.scheme or url.netloc:
                if url.scheme.lower() in ('javascript', 'data'):
                    fail(page, f'unexpected {url.scheme} URL')
                continue
            if url.path.startswith('/'):
                target = ROOT / unquote(url.path.lstrip('/'))
            else:
                target = page.parent / unquote(url.path) if url.path else page
            target = target.resolve()
            if not target.is_relative_to(ROOT):
                fail(page, f'local reference leaves the site: {value}')
                continue
            if target.is_relative_to(ROOT / 'archive'):
                fail(page, f'public page references a preserved archive file: {value}')
                continue
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                fail(page, f'missing local file: {value}')
                continue
            if url.fragment and target in documents:
                if not any(e.get('id') == unquote(url.fragment) for e in documents[target].iter()):
                    fail(page, f'missing anchor: {value}')

patterns = [line.strip() for line in (ROOT / '.assetsignore').read_text().splitlines()
            if line.strip() and not line.startswith('#')]
for path in ROOT.rglob('*'):
    if '.git' in path.parts:
        continue
    if path.name == '.DS_Store':
        fail(path, 'Mac Finder metadata should not be tracked')
    if path.is_file() and 'archive' in path.relative_to(ROOT).parts:
        relative = path.relative_to(ROOT).as_posix()
        if not any(fnmatchcase(relative, pattern) for pattern in patterns):
            fail(path, 'preserved archive file is not excluded from asset uploads')
    if path.suffix.lower() == '.mp3' and path.is_relative_to(ROOT / 'images'):
        fail(path, 'archived audio belongs outside deployed images')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(pages)} pages; valid HTML, local files and anchors, and archive exclusions.')
