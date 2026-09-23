# -*- coding: utf-8 -*-
"""Generate a translated language layer from the English pages.

Reads docs/<path>/index.html, writes docs/<prefix>/<path>/index.html with:
  - lang / hreflang / canonical / og:locale rewritten
  - <title>, meta description and the og/twitter twins translated
  - internal links repointed into the language layer where a twin exists
  - JSON-LD url, @id and inLanguage rewritten (scoped to ld+json blocks)
  - every text node inside <main> replaced from the glossary

A page is only written when glossary coverage reaches MIN_COVERAGE. A partly
translated page is worse than none, so short pages are reported and skipped.

Usage:
    python tools/build_lang.py zh            # build
    python tools/build_lang.py zh --dry      # report coverage only
    python tools/build_lang.py zh workbench  # limit to matching paths
"""
import re, io, os, json, glob, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.storagesystem.com.my"
MIN_COVERAGE = 1.0

LANGS = {
    "zh": dict(prefix="zh", html_lang="zh-Hans-MY", hreflang="zh-Hans-MY",
               og_locale="zh_MY",
               switch_en="阅读本页英文版 →",
               switch_to="阅读本页中文版 →"),
    "ms": dict(prefix="ms", html_lang="ms-MY", hreflang="ms-MY",
               og_locale="ms_MY",
               switch_en="Baca halaman ini dalam Bahasa Inggeris →",
               switch_to="Baca halaman ini dalam Bahasa Malaysia →"),
}

SKIP = re.compile(r'^[\s\W\d]*$|^[WDH]\d|^\d+(\.\d+)?$|^RM\s?[\d,]|^[A-Z]{1,4}[\-A-Z0-9]*\d[\-A-Z0-9]*$')

HEAD_PATTERNS = [
    (re.compile(r'(<title>)(.*?)(</title>)', re.S), 2),
    (re.compile(r'(<meta name="description" content=")([^"]*)(")'), 2),
    (re.compile(r'(<meta property="og:title" content=")([^"]*)(")'), 2),
    (re.compile(r'(<meta property="og:description" content=")([^"]*)(")'), 2),
    (re.compile(r'(<meta property="og:image:alt" content=")([^"]*)(")'), 2),
    (re.compile(r'(<meta name="twitter:image:alt" content=")([^"]*)(")'), 2),
]


def _blank(mm):
    return ' ' * (mm.end() - mm.start())


def text_nodes(html):
    """(start, end, raw, normalised) for translatable text nodes inside <main>."""
    m = re.search(r'<main\b[^>]*>.*?</main>', html, re.S | re.I)
    if not m:
        return []
    lo = m.start()
    body = re.sub(r'<(script|style)\b.*?</\1>', _blank, html[lo:m.end()],
                  flags=re.S | re.I)
    out = []
    for tm in re.finditer(r'>([^<>]+)<', body):
        raw = tm.group(1)
        s = re.sub(r'\s+', ' ', raw).strip()
        if not s or SKIP.match(s):
            continue
        if re.fullmatch(r'[\w\s]*[×xX]\s*\d+\s*(mm|cm|kg)?', s):
            continue
        out.append((lo + tm.start(1), lo + tm.end(1), raw, s))
    return out


def head_strings(html):
    """Translatable strings in <head>, deduplicated."""
    head = html[:html.find('</head>')] if '</head>' in html else html
    seen = []
    for rx, gi in HEAD_PATTERNS:
        for m in rx.finditer(head):
            s = re.sub(r'\s+', ' ', m.group(gi)).strip()
            if s and s not in seen:
                seen.append(s)
    return seen


def all_strings(html):
    return [n[3] for n in text_nodes(html)] + head_strings(html)


def load_glossary(lang):
    p = os.path.join(ROOT, 'tools', 'i18n', 'glossary_%s.json' % lang)
    return json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else {}


def rel_path(f):
    return f.replace(os.sep, '/')[len('docs'):].rsplit('index.html', 1)[0]


def build(lang, pages, write=True, verbose=True):
    cfg = LANGS[lang]
    gl = load_glossary(lang)
    twins = {rel_path(f) for f in pages}
    written, skipped = [], []
    missing = collections.Counter()

    for f in pages:
        html = io.open(f, encoding='utf-8').read()
        path = rel_path(f)
        strings = all_strings(html)
        absent = [s for s in strings if s not in gl]
        cov = 1.0 - (len(absent) / float(len(strings))) if strings else 1.0
        if cov < MIN_COVERAGE:
            for s in absent:
                missing[s] += 1
            skipped.append((path, cov, len(absent)))
            continue

        new = '/%s%s' % (cfg['prefix'], path)

        # capture the ORIGINAL alternates before anything rewrites them.
        # Malay lives at root with its own slug (/papan-berlubang/), not /ms/,
        # so its real URL has to be carried across rather than derived.
        orig_alts = dict(re.findall(
            r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)">', html))

        # ---- body text (right to left so offsets stay valid)
        for start, end, raw, s in reversed(text_nodes(html)):
            if s in gl:
                lead = raw[:len(raw) - len(raw.lstrip())]
                tail = raw[len(raw.rstrip()):]
                html = html[:start] + lead + gl[s] + tail + html[end:]

        # ---- head fields
        cut = html.find('</head>')
        head, rest = html[:cut], html[cut:]
        for rx, gi in HEAD_PATTERNS:
            def sub(m):
                s = re.sub(r'\s+', ' ', m.group(gi)).strip()
                if s in gl:
                    return m.group(1) + gl[s] + m.group(3)
                return m.group(0)
            head = rx.sub(sub, head)
        html = head + rest

        # ---- JSON-LD, scoped so it cannot touch <link> hrefs
        def fix_ld(m):
            blob = m.group(0)
            blob = blob.replace('"%s%s"' % (SITE, path), '"%s%s"' % (SITE, new))
            blob = re.sub(r'("inLanguage"\s*:\s*")[^"]*(")',
                          lambda mm: mm.group(1) + cfg['html_lang'] + mm.group(2), blob)
            return blob
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', fix_ld,
                      html, flags=re.S)

        # ---- canonical / og:url / og:locale
        html = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % cfg['html_lang'], html, count=1)
        html = html.replace('<link rel="canonical" href="%s%s">' % (SITE, path),
                            '<link rel="canonical" href="%s%s">' % (SITE, new))
        html = re.sub(r'<meta property="og:locale" content="[^"]*">',
                      '<meta property="og:locale" content="%s">' % cfg['og_locale'], html, count=1)
        html = html.replace('<meta property="og:url" content="%s%s">' % (SITE, path),
                            '<meta property="og:url" content="%s%s">' % (SITE, new))

        # ---- internal links into this language layer (before the switcher,
        #      so the switcher's own href is not caught by it)
        def fixhref(m):
            h = m.group(1)
            return 'href="/%s%s"' % (cfg['prefix'], h) if h in twins else m.group(0)
        html = re.sub(r'href="(/[^"#?]*/)"', fixhref, html)

        # ---- language switcher in the body: point back to English
        html = re.sub(
            r'<a href="[^"]*" hreflang="ms-MY" rel="alternate">[^<]*</a>',
            '<a href="%s" hreflang="en-MY" rel="alternate">%s</a>' % (path, cfg['switch_en']),
            html)

        # ---- hreflang cluster, rebuilt last so nothing else can rewrite it
        alts = re.findall(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', html)
        if alts:
            block = ['<link rel="alternate" hreflang="en-MY" href="%s%s">' % (SITE, path)]
            for L, c in LANGS.items():
                if L == lang:
                    href = '%s%s' % (SITE, new)
                elif c['hreflang'] in orig_alts:
                    href = orig_alts[c['hreflang']]      # real Malay slug at root
                else:
                    continue                             # no twin, so no claim
                block.append('<link rel="alternate" hreflang="%s" href="%s">'
                             % (c['hreflang'], href))
            block.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, path))
            html = html.replace(alts[0], '\n'.join(block), 1)
            for a in alts[1:]:
                html = html.replace(a, '', 1)

        if write:
            out = os.path.join(ROOT, 'docs', cfg['prefix'], path.strip('/'), 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            io.open(out, 'w', encoding='utf-8', newline='').write(html)
        written.append(path)

    if verbose:
        print('[%s] written: %d   skipped: %d' % (lang, len(written), len(skipped)))
        for p, c, n in sorted(skipped, key=lambda r: r[1])[:8]:
            print('    %5.1f%%  %-42s %4d missing' % (c * 100, p, n))
        if missing:
            print('    untranslated: %d distinct / %d occurrences'
                  % (len(missing), sum(missing.values())))
    return written, skipped, missing


def target_pages():
    CATS = ("workbench tool-cabinet perforated-board workstation cnc-tool parts-cabinet "
            "hanger-rack documents-cabinet locker rack household-items").split()
    pages = []
    for c in CATS:
        pages.append('docs/%s/index.html' % c)
        pages += sorted(glob.glob('docs/%s/*/index.html' % c))
    return pages


if __name__ == '__main__':
    os.chdir(ROOT)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    lang = args[0] if args else 'zh'
    only = args[1] if len(args) > 1 else None
    pages = target_pages()
    if only:
        pages = [p for p in pages if only in p]
    # full inventory of every translatable string across the target pages
    inv = collections.Counter()
    for f in pages:
        for s in all_strings(io.open(f, encoding='utf-8').read()):
            inv[s] += 1
    # only a full (unfiltered) run may rewrite the inventory, otherwise a
    # filtered run would shrink it and the glossary would lose entries
    if not only:
        inv_path = os.path.join(ROOT, 'tools', 'i18n', 'strings_%s.json' % lang)
        json.dump(inv.most_common(), io.open(inv_path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=0)
        print('    inventory: %d distinct -> %s' % (len(inv), inv_path))

    w, s, miss = build(lang, pages, write='--dry' not in sys.argv)
    if miss:
        out = os.path.join(ROOT, 'tools', 'i18n', 'missing_%s.json' % lang)
        json.dump(miss.most_common(), io.open(out, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=0)
        print('    -> %s' % out)
