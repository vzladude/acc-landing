#!/usr/bin/env python3
"""Package a static production release; original source assets remain untouched."""
import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / '.qa' / 'production-site'
PRODUCTION_URL = 'https://inversionesacc.com/'
EXTENSIONS = {'.css', '.js', '.jpg', '.jpeg', '.png', '.webp', '.svg'}


def fingerprint(relative, data):
    path = Path(relative)
    digest = hashlib.sha256(data).hexdigest()[:16]
    return path.with_name(f'{path.stem}.{digest}{path.suffix}').as_posix()


def build():
    page = (ROOT / 'index.html').read_text()
    for expected in [f'rel="canonical" href="{PRODUCTION_URL}"',
                     f'property="og:url" content="{PRODUCTION_URL}"',
                     f'"url": "{PRODUCTION_URL}"']:
        if expected not in page:
            raise ValueError('Production metadata must use the official ACC URL.')
    if re.search(r'\bnoindex\b|vzladude\.github\.io', page, re.I):
        raise ValueError('Production HTML contains preview metadata.')

    sources = [ROOT / 'favicon.svg']
    for directory in ['img', 'js', 'css']:
        sources.extend(sorted((ROOT / directory).rglob('*')))
    assets, names = {}, {}
    # Images are named first so CSS hashes include the rewritten image URLs.
    for source in sources:
        if source.is_symlink():
            raise ValueError(f'Symlink is not a deployable asset: {source}')
        if not source.is_file() or source.suffix.lower() not in EXTENSIONS:
            continue
        relative = source.relative_to(ROOT).as_posix()
        if source.suffix == '.css':
            continue
        data = source.read_bytes()
        names[relative] = fingerprint(relative, data)
        assets[names[relative]] = data
    for source in sources:
        if source.suffix != '.css' or not source.is_file():
            continue
        css = source.read_text()
        for original, renamed in names.items():
            css = css.replace('../' + original, '../' + renamed)
        data = css.encode()
        relative = source.relative_to(ROOT).as_posix()
        names[relative] = fingerprint(relative, data)
        assets[names[relative]] = data
    for original, renamed in names.items():
        page = page.replace('./' + original, './' + renamed)
        page = page.replace(PRODUCTION_URL + original, PRODUCTION_URL + renamed)

    class AssetValidator(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key not in ('href', 'src') or not value or value.startswith('#'):
                    continue
                url = urlsplit(value)
                if url.scheme or url.netloc:
                    continue
                if url.path.removeprefix('./') not in assets:
                    raise ValueError(f'Missing runtime asset: {value}')

    AssetValidator().feed(page)
    for relative, data in assets.items():
        if relative.endswith('.css'):
            for raw in re.findall(r'url\([\s\'\"]*([^\)\'\"\s]+)', data.decode()):
                if urlsplit(raw).scheme or raw.startswith(('#', '//')):
                    continue
                target = (ROOT / Path(relative).parent / urlsplit(raw).path).resolve()
                if not target.is_relative_to(ROOT) or target.relative_to(ROOT).as_posix() not in assets:
                    raise ValueError(f'Missing CSS asset: {raw}')

    # The small stylesheet belongs in the first response: this avoids a blocking
    # network round trip on mobile while preserving the editable source CSS.
    stylesheet = names['css/styles.css']
    marker = f'<link rel="stylesheet" href="./{stylesheet}">'
    if page.count(marker) != 1:
        raise ValueError('Expected one local stylesheet link.')
    css = assets.pop(stylesheet).decode().replace('url("../', 'url("./')
    page = page.replace(marker, '<style>\n' + css + '\n</style>')

    assets['index.html'] = page.encode()
    assets['robots.txt'] = (ROOT / 'robots.txt').read_bytes()
    assets['sitemap.xml'] = (ROOT / 'sitemap.xml').read_bytes()
    if DESTINATION.is_symlink():
        raise ValueError('Release destination must not be a symlink.')
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.mkdir(parents=True)
    for relative, data in assets.items():
        target = DESTINATION / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    manifest = {relative: hashlib.sha256(data).hexdigest() for relative, data in sorted(assets.items())}
    (DESTINATION.parent / 'release-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'{len(assets)} public files; {sum(map(len, assets.values())):,} bytes; {DESTINATION}')
    return DESTINATION


if __name__ == '__main__':
    build()
