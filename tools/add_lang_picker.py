# -*- coding: utf-8 -*-
"""Add a language picker to the primary nav of every page.

The links are derived from each page's own hreflang block, so a page only ever
offers the languages that actually exist for it - no invented URLs. Reuses the
site's existing .nav-toggle / .dropdown classes, which are pure CSS, so no new
JavaScript is needed.

Idempotent: a page that already has the picker is skipped.

Run:  python tools/add_lang_picker.py [--dry]
"""
import re, io, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')

# hreflang code -> (short label for the toggle, full name in the menu)
LANGS = [
    ('en-MY',      'EN',   'English'),
    ('ms-MY',      'BM',   'Bahasa Malaysia'),
    ('zh-Hans-MY', '中文', '中文'),
]
MARKER = 'class="lang-pick"'


# Where to send someone when this exact page has no twin in that language.
# Better to land them on that language's home than to hide the option entirely.
# Malay now has a hub at /ms/, so all three languages are always offered.
FALLBACK = {'en-MY': '/', 'ms-MY': '/ms/', 'zh-Hans-MY': '/zh/'}


def build_picker(alts, current):
    """alts: {hreflang: href}. current: this page's hreflang code."""
    items = []
    for code, short, full in LANGS:
        href = alts.get(code)
        exact = href is not None
        if not exact:
            href = FALLBACK.get(code)
        if not href:
            continue
        cur = ' aria-current="true"' if code == current else ''
        # flag the ones that go to the language home rather than this page,
        # so the markup stays honest about what the link does
        rel = '' if exact else ' data-lang-fallback="home"'
        items.append('<a href="%s" hreflang="%s" role="menuitem"%s%s>%s</a>'
                     % (href, code, cur, rel, full))
    if len(items) < 2:
        return None                      # nothing to switch between
    short = dict((c, s) for c, s, f in LANGS).get(current, 'EN')
    return (
        '\n        <li class="lang-pick">\n'
        '          <a href="#" class="nav-toggle" aria-haspopup="true" '
        'aria-label="Language">%s<span class="caret"></span></a>\n'
        '          <div class="dropdown" role="menu" aria-label="Language">\n'
        '            %s\n'
        '          </div>\n'
        '        </li>' % (short, '\n            '.join(items))
    )


def process(path, write=True):
    with io.open(path, encoding='utf-8') as fh:
        html = fh.read()
    if MARKER in html:
        return 'already'

    nav = re.search(r'<ul class="nav-list">', html)
    if not nav:
        return 'no-nav'

    end = html.find('</ul>', nav.end())
    if end < 0:
        return 'no-nav-end'

    alts = dict(re.findall(
        r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)">', html))
    alts.pop('x-default', None)
    if not alts:
        return 'no-hreflang'

    m = re.search(r'<html lang="([^"]*)"', html)
    current = m.group(1) if m else 'en-MY'

    # hrefs in the hreflang block are absolute; make them root-relative so the
    # links stay on whichever host is serving the page
    alts = dict((k, re.sub(r'^https?://[^/]+', '', v)) for k, v in alts.items())

    picker = build_picker(alts, current)
    if not picker:
        return 'single-language'

    html = html[:end] + picker + '\n      ' + html[end:]
    if write:
        with io.open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(html)
    return 'added'


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    counts = {}
    files = sorted(glob.glob(os.path.join(DOCS, '**', '*.html'), recursive=True))
    for f in files:
        r = process(f, write=not dry)
        counts[r] = counts.get(r, 0) + 1
    print('%s%d files scanned' % ('[dry] ' if dry else '', len(files)))
    for k in sorted(counts):
        print('   %-16s %d' % (k, counts[k]))
