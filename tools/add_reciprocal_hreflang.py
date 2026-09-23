# -*- coding: utf-8 -*-
"""Declare the Chinese alternate on the English (and Malay) pages.

hreflang has to be reciprocal: if /zh/x/ points at /x/, then /x/ must point
back at /zh/x/, otherwise Google discards the pairing and the Chinese page is
treated as an unrelated duplicate. The generator only wrote the cluster onto
the pages it produced, so the English originals were missing the return link.

Only adds where the Chinese twin actually exists on disk. Idempotent.

Run:  python tools/add_reciprocal_hreflang.py [--dry]
"""
import re, io, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
SITE = 'https://www.storagesystem.com.my'


def zh_twin_path(rel):
    """rel is like '/perforated-board/'. Returns the /zh/ path if built."""
    cand = os.path.join(DOCS, 'zh', rel.strip('/'), 'index.html')
    return ('/zh' + rel) if os.path.exists(cand) else None


def process(path, write=True):
    rel = path.replace(os.sep, '/')[len(DOCS.replace(os.sep, '/')):]
    rel = rel.rsplit('index.html', 1)[0] or '/'
    if rel.startswith('/zh/') or rel == '/zh/':
        return 'is-zh'

    with io.open(path, encoding='utf-8') as fh:
        html = fh.read()
    if '<link rel="alternate" hreflang="zh-Hans-MY"' in html:
        return 'already'

    twin = zh_twin_path(rel)
    if not twin:
        return 'no-twin'

    # insert the zh alternate directly after the en-MY one so the cluster
    # stays grouped and readable
    m = re.search(r'<link rel="alternate" hreflang="en-MY" href="[^"]*">', html)
    if not m:
        return 'no-en-alt'

    tag = '\n<link rel="alternate" hreflang="zh-Hans-MY" href="%s%s">' % (SITE, twin)
    html = html[:m.end()] + tag + html[m.end():]
    if write:
        with io.open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(html)
    return 'added'


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    counts = {}
    for f in sorted(glob.glob(os.path.join(DOCS, '**', '*.html'), recursive=True)):
        r = process(f, write=not dry)
        counts[r] = counts.get(r, 0) + 1
    print('%sresults:' % ('[dry] ' if dry else ''))
    for k in sorted(counts):
        print('   %-12s %d' % (k, counts[k]))
