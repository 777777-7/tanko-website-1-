import sys, json, requests, re
sys.path.insert(0, '.')
from tanko_variant_scraper import scrape_product, BASE

cats = ['workstation','workbench','tool-cabinet','cnc-tool','rack','hanger-rack','locker','parts-cabinet','documents-cabinet','perforated-board','household-items']
all_urls = set()
for cat in cats:
    for page in range(1, 15):
        u = f'{BASE}/en/products/{cat}/' + (f'?page={page}' if page>1 else '')
        try:
            r = requests.get(u, headers={'User-Agent':'Mozilla/5.0'}, timeout=10).text
        except Exception: break
        hits = set(re.findall(r'/en/products-detail/([a-z0-9\-]+)/', r))
        if not hits and page > 1: break
        before = len(all_urls); all_urls.update(hits)
        if page > 1 and len(all_urls) == before: break

existing = json.load(open('tanko_variants.json',encoding='utf-8'))
have = {p['slug'] for p in existing}
missing = sorted(all_urls - have)
print(f'Missing count: {len(missing)}', flush=True)
for i, slug in enumerate(missing, 1):
    print(f'[{i}/{len(missing)}] {slug}', flush=True)
    d = scrape_product(f'{BASE}/en/products-detail/{slug}/')
    if d:
        existing.append(d)
    if i % 5 == 0:
        json.dump(existing, open('tanko_variants.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(existing, open('tanko_variants.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'DONE. products={len(existing)} variants={sum(len(p["variants"]) for p in existing)}', flush=True)
