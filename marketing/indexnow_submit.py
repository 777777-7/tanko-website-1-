# -*- coding: utf-8 -*-
"""Push changed URLs to Bing, Yandex, Seznam and Naver in one call (IndexNow).

Why this is worth having, honestly: Bing's own share of Malaysian search is
small, and this will not move Google at all. Two other things make it pay:

  1. Bing's index is what ChatGPT search, Copilot, DuckDuckGo, Yahoo and Ecosia
     read. For a B2B supplier, buyers increasingly research through those.
  2. 1,591 product pages were rewritten on 10 Sep 2026 and 1,228 pages sit in
     "Discovered -- currently not indexed". IndexNow is a push, not a crawl
     request: the URLs are accepted immediately rather than waiting to be
     rediscovered.

Usage:
    python marketing/indexnow_submit.py --what products   # the 1,591 SKU pages
    python marketing/indexnow_submit.py --what changed    # touched in last commit
    python marketing/indexnow_submit.py --what all        # everything in the sitemaps
    (add --apply to actually send; default is a dry run)

The key must be live at https://www.storagesystem.com.my/<key>.txt before any
submission is accepted, so push before running this.
"""
import re, os, sys, json, glob, subprocess
import urllib.request

HOST = 'www.storagesystem.com.my'
BASE = 'https://' + HOST
ENDPOINT = 'https://api.indexnow.org/IndexNow'
KEY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'indexnow-key.txt'), encoding='utf-8').read().strip()
BATCH = 10000          # IndexNow accepts up to 10,000 URLs per request


def urls_from(paths):
    out = []
    for f in paths:
        s = open(f, encoding='utf-8').read()
        out += re.findall(r'<loc>(.*?)</loc>', s)
    return out


def pick(what):
    if what == 'products':
        return urls_from(['docs/sitemap-products.xml'])
    if what == 'all':
        return urls_from(sorted(glob.glob('docs/sitemap-*.xml')))
    if what == 'changed':
        files = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
                               capture_output=True, text=True).stdout.split()
        out = []
        for f in files:
            if f.startswith('docs/') and f.endswith('index.html'):
                out.append(BASE + '/' + f[len('docs/'):-len('index.html')])
        return out
    raise SystemExit('--what must be products, changed or all')


def main():
    what = 'changed'
    for a in sys.argv[1:]:
        if a.startswith('--what='):
            what = a.split('=', 1)[1]
        elif a == '--what':
            what = sys.argv[sys.argv.index(a) + 1]
    apply = '--apply' in sys.argv

    urls = sorted(set(pick(what)))
    print('key      :', KEY)
    print('selection:', what)
    print('urls     :', len(urls))
    for u in urls[:5]:
        print('   ', u)
    if len(urls) > 5:
        print('    ... and %d more' % (len(urls) - 5))
    if not urls:
        return
    if not apply:
        print('\nDRY RUN — nothing sent. Add --apply to submit.')
        return

    sent = 0
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        payload = json.dumps({
            "host": HOST,
            "key": KEY,
            "keyLocation": "%s/%s.txt" % (BASE, KEY),
            "urlList": chunk,
        }).encode()
        req = urllib.request.Request(
            ENDPOINT, data=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print('batch %d: HTTP %s (%d urls)' % (i // BATCH + 1, r.status, len(chunk)))
                sent += len(chunk)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')[:300]
            print('batch %d: HTTP %s — %s' % (i // BATCH + 1, e.code, body))
            if e.code == 403:
                print('  403 means the key file is not reachable yet. Check '
                      '%s/%s.txt is live, then retry.' % (BASE, KEY))
            return
    print('\nsubmitted %d URLs' % sent)
    print('HTTP 200 or 202 means accepted. It is a push, not a promise to index.')


if __name__ == '__main__':
    main()
