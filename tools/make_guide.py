# -*- coding: utf-8 -*-
"""Create a new English guide page from the site's existing guide shell.

Copies head, nav, footer and scripts from TEMPLATE, then swaps in the new
page's title, description, canonical, Open Graph, JSON-LD and <main> body. The
hreflang block is reduced to en-MY + x-default, because a new guide has no
Malay or Chinese twin yet. The inherited language picker is stripped;
tools/add_lang_picker.py adds the right one afterwards.

Content lives in tools/guides_src/<module>.py as a GUIDE dict.

Run:  python tools/make_guide.py <module> [<module> ...]
"""
import html, importlib, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.storagesystem.com.my'
TEMPLATE = os.path.join(ROOT, 'docs', 'guides',
                        'perforated-board-shadow-board-tool-control-malaysia', 'index.html')

AUTHOR = {"@type": "Person", "name": "Wong Wei Ming", "jobTitle": "Business Development Manager",
          "worksFor": {"@type": "Organization", "name": "Primaxs Marketing (M) Sdn Bhd",
                       "url": SITE + "/", "sameAs": ["https://www.facebook.com/primaxsmarketing"]}}
PUBLISHER = {"@type": "Organization", "name": "Primaxs Marketing (M) Sdn Bhd",
             "sameAs": ["https://www.facebook.com/primaxsmarketing"]}


def plain(s):
    """HTML fragment -> plain text for JSON-LD."""
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s))).strip()


def esc(s):
    return html.escape(s, quote=True)


def long_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return '%d %s %d' % (d.day, d.strftime('%B'), d.year)


def jsonld(g, url):
    graph = [
        {"@type": "Article", "headline": g['h1'], "author": AUTHOR, "publisher": PUBLISHER,
         "about": g.get('about', 'Industrial storage in Malaysia'), "mainEntityOfPage": url,
         "inLanguage": "en-MY", "datePublished": g['published'],
         "dateModified": g.get('modified', g['published']), "image": SITE + g['og_image']},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": g['crumb'], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in g['faqs']]},
    ]
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False))


def main_html(g):
    img = g['image']
    stem = img.rsplit('.', 1)[0]
    q = lambda p: p.replace(' ', '%20')
    faqs = '\n'.join('        <details><summary>%s</summary><p>%s</p></details>' % (qq, a)
                     for qq, a in g['faqs'])
    ranges = '\n'.join('          <li><a href="%s">%s</a> &mdash; %s</li>' % r for r in g['ranges'])
    sources = '\n'.join('          <li>%s</li>' % s for s in g['sources'])
    updated = ''
    if g.get('modified') and g['modified'] != g['published']:
        updated = ' &middot; Updated <time datetime="%s">%s</time>' % (g['modified'], long_date(g['modified']))
    # wide comparison tables must scroll inside the article on a phone,
    # not push the whole page sideways
    body = re.sub(r'(<table>.*?</table>)',
                  r'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">\1</div>',
                  g['body'].strip(), flags=re.S)
    tpl = io.open(TEMPLATE, encoding='utf-8').read()
    # reuse the template's compliance aside and author box verbatim
    compliance = re.search(r'<aside class="article-compliance".*?</aside>', tpl, re.S).group(0)
    author = re.search(r'<aside class="author-box">.*?</aside>', tpl, re.S).group(0)
    return '''<main id="main-content">
<div class="container">
  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="/">Home</a><span class="sep">/</span>
    <a href="/guides/">Guides</a><span class="sep">/</span>
    <span class="current">%(crumb)s</span>
  </nav>
</div>
<section class="section">
  <div class="container">
    <article class="article">
      <div class="tag" style="color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:.72rem;">%(tag)s</div>
      <h1>%(h1)s</h1>
      <div class="article-meta">By <span class="author-name">Wong Wei Ming</span>, Business Development Manager &middot; <a href="/about/">Primaxs Marketing (M) Sdn Bhd</a> &middot; Published <time datetime="%(pub)s">%(publong)s</time>%(updated)s</div>

<p class="lead">%(lead)s</p>
<figure class="guide-figure">
  <picture>
    <source srcset="%(w800)s 800w, %(full)s 1200w"
            sizes="(max-width: 780px) 100vw, 720px" type="image/webp">
    <img src="%(full)s" alt="%(alt)s" width="1200" height="1200"
         loading="lazy" decoding="async" class="guide-img">
  </picture>
  <figcaption>%(caption)s</figcaption>
</figure>

%(body)s

      <div class="faq">
        <h2>Frequently asked questions</h2>
%(faqs)s
      </div>

      <div class="callout" style="margin-top:2.5rem;">
        <p><strong>Sourcing in Malaysia?</strong> Primaxs is the exclusive Malaysia distributor for Tanko industrial storage. Browse the <a href="/products/">product range</a> or <a href="/enquiry/">request a quote</a> for your workshop or factory.</p>
      </div>

      %(compliance)s

      <aside class="guide-ranges" style="margin-top:1.75rem;padding:1.25rem 1.5rem;border:1px solid var(--line,#26303f);border-radius:6px;font-size:.9rem;">
        <h3 style="margin:0 0 .6rem;font-size:1rem;">The ranges this guide covers</h3>
        <ul style="margin:0;padding-left:1.25rem;line-height:1.7;">
%(ranges)s
        </ul>
      </aside>

      <aside class="article-sources" style="margin-top:1.25rem;padding:1.25rem 1.5rem;border:1px solid var(--line,#26303f);border-radius:6px;font-size:.9rem;">
        <h3 style="margin:0 0 .6rem;font-size:1rem;">References &amp; further reading</h3>
        <ul style="margin:0;padding-left:1.25rem;line-height:1.7;">
%(sources)s
        </ul>
      </aside>
    %(author)s</article>
  </div>
</section>
</main>''' % dict(crumb=g['crumb'], tag=g['tag'], h1=g['h1'], pub=g['published'],
                  publong=long_date(g['published']), updated=updated, lead=g['lead'],
                  w800=q(stem + '-w800.webp'), full=q(img), alt=esc(g['image_alt']),
                  caption=g['caption'], body=body, faqs=faqs,
                  compliance=compliance, ranges=ranges, sources=sources, author=author)


def build(g):
    url = '%s/guides/%s/' % (SITE, g['slug'])
    h = io.open(TEMPLATE, encoding='utf-8').read()

    def sub1(pattern, repl, s):
        new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('template pattern not found: %s' % pattern)
        return new

    h = sub1(r'<title>.*?</title>', '<title>%s</title>' % esc(g['title']), h)
    h = sub1(r'<meta name="description" content="[^"]*">',
             '<meta name="description" content="%s">' % esc(g['description']), h)
    h = sub1(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, h)
    # hreflang: English only until a translation exists
    alts = re.findall(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', h)
    block = ('<link rel="alternate" hreflang="en-MY" href="%s">\n'
             '<link rel="alternate" hreflang="x-default" href="%s">' % (url, url))
    h = h.replace(alts[0], block, 1)
    for a in alts[1:]:
        h = h.replace(a, '', 1)
    h = sub1(r'<meta property="og:title" content="[^"]*">',
             '<meta property="og:title" content="%s">' % esc(g['title']), h)
    h = sub1(r'<meta property="og:description" content="[^"]*">',
             '<meta property="og:description" content="%s">' % esc(g['description']), h)
    h = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, h)
    h = sub1(r'<meta property="og:image" content="[^"]*">',
             '<meta property="og:image" content="%s%s">' % (SITE, g['og_image']), h)
    h = sub1(r'<meta property="og:image:alt" content="[^"]*">',
             '<meta property="og:image:alt" content="%s">' % esc(g['image_alt']), h)
    h = sub1(r'<meta name="twitter:image:alt" content="[^"]*">',
             '<meta name="twitter:image:alt" content="%s">' % esc(g['image_alt']), h)
    h = sub1(r'<meta name="twitter:image" content="[^"]*">',
             '<meta name="twitter:image" content="%s%s">' % (SITE, g['og_image']), h)
    h = sub1(r'<script type="application/ld\+json">.*?</script>', jsonld(g, url), h)
    h = re.sub(r'\n\s*<li class="lang-pick">.*?</li>', '', h, flags=re.S)
    h = sub1(r'<main id="main-content">.*?</main>', main_html(g), h)

    out = os.path.join(ROOT, 'docs', 'guides', g['slug'], 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, 'w', encoding='utf-8', newline='') as fh:
        fh.write(h)
    words = len(plain(re.search(r'<article.*?</article>', main_html(g), re.S).group(0)).split())
    print('   wrote %s  (%d words in article)' % (os.path.relpath(out, ROOT), words))


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'guides_src'))
    for name in sys.argv[1:]:
        build(importlib.import_module(name).GUIDE)
