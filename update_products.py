# -*- coding: utf-8 -*-
"""
Tanko Product Update Tool
- Scrapes tanko.tw for new/updated products
- Compares with existing products.json
- Generates update report
- Optionally merges new products into products.json

Usage:
  python update_products.py          # Scan and report only
  python update_products.py --apply  # Apply updates to products.json
"""
import json
import os
import sys
import time
from datetime import datetime

# Import scraper from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanko_scraper import scrape_all, scrape_family, get_product_families, CATEGORY_MAP, BASE_URL

PRODUCTS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.json')
REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tanko_update_report.json')


def load_existing_products():
    """Load existing products.json."""
    with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_existing_skus(products):
    """Get set of existing SKUs and family slugs."""
    skus = set()
    families = set()
    for p in products:
        if p.get('sku'):
            skus.add(p['sku'].upper())
        if p.get('family_slug'):
            families.add(p['family_slug'].lower())
    return skus, families


def map_category(tanko_category):
    """Map tanko.tw category to website category_slug."""
    # Direct match
    if tanko_category in CATEGORY_MAP:
        return CATEGORY_MAP[tanko_category]
    # Fuzzy match
    for key, val in CATEGORY_MAP.items():
        if key.lower() in tanko_category.lower() or tanko_category.lower() in key.lower():
            return val
    return 'unknown'


def generate_product_entries(family_data, existing_skus):
    """Generate product entries from scraped family data.
    For now, creates a mother product entry. Variants need SKU resolution.
    """
    entries = []
    slug = family_data['slug']
    model_no = family_data.get('model_no', '')
    
    # Create mother product entry
    mother = {
        'sku': model_no or slug.upper(),
        'product_family': family_data.get('family_name', slug.title()),
        'family_slug': slug,
        'category': family_data.get('category', ''),
        'category_slug': map_category(family_data.get('category', '')),
        'subcategory': family_data.get('subcategory', ''),
        'color': None,
        'dimensions': '',
        'material': '',
        'load_capacity': None,
        'attributes': {},
        'image_paths': [],
        'tanko_url': family_data.get('url', ''),
        'evidence': {'tanko': True, 'pdf': False, 'image': bool(family_data.get('images'))},
        'distinct_title': '',
        'product_type': 'mother_product',
        'specification': '',
    }
    
    # Build specification from features
    if family_data.get('features'):
        mother['specification'] = 'Features:\n' + '\n'.join(f'- {f}' for f in family_data['features'][:15])
    
    # Add spec options to attributes
    if family_data.get('spec_options'):
        for opt_name, options in family_data['spec_options'].items():
            mother['attributes'][opt_name] = ', '.join(o['name'] for o in options)
    
    entries.append(mother)
    
    # TODO: Generate variant entries from spec combinations
    # This requires AJAX calls to get exact SKUs for each combination
    
    return entries


def main():
    apply_mode = '--apply' in sys.argv
    
    print("=" * 60)
    print("TANKO PRODUCT UPDATE TOOL")
    print(f"Mode: {'APPLY' if apply_mode else 'REPORT ONLY'}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load existing products
    print("\n[1/4] Loading existing products...")
    existing = load_existing_products()
    existing_skus, existing_families = get_existing_skus(existing)
    print(f"  Existing products: {len(existing)}")
    print(f"  Existing SKUs: {len(existing_skus)}")
    print(f"  Existing families: {len(existing_families)}")
    
    # Scrape tanko.tw
    print("\n[2/4] Scraping tanko.tw...")
    families = get_product_families()
    print(f"  Found {len(families)} product families on tanko.tw")
    
    scraped = {}
    new_families = []
    for i, (slug, info) in enumerate(families.items()):
        print(f"  [{i+1}/{len(families)}] {slug}: {info['name']}")
        data = scrape_family(info['url'], slug)
        if data:
            data['category'] = data['category'] or info['category']
            scraped[slug] = data
            if slug.lower() not in existing_families:
                new_families.append(slug)
        time.sleep(0.2)
    
    # Compare
    print("\n[3/4] Comparing...")
    scraped_families = set(scraped.keys())
    missing_families = existing_families - scraped_families
    new_family_set = scraped_families - existing_families
    
    print(f"\n  Families on tanko.tw: {len(scraped_families)}")
    print(f"  New families (not on website): {len(new_family_set)}")
    print(f"  Families on website but not tanko.tw: {len(missing_families)}")
    
    if new_family_set:
        print("\n  NEW FAMILIES:")
        for slug in sorted(new_family_set):
            data = scraped.get(slug, {})
            print(f"    - {slug}: {data.get('family_name', '?')} (Model: {data.get('model_no', '?')})")
    
    if missing_families:
        print("\n  MISSING FROM TANKO.TW (may be discontinued):")
        for slug in sorted(missing_families):
            print(f"    - {slug}")
    
    # Generate new product entries
    new_products = []
    for slug in new_family_set:
        if slug in scraped:
            entries = generate_product_entries(scraped[slug], existing_skus)
            new_products.extend(entries)
    
    print(f"\n  New product entries to add: {len(new_products)}")
    
    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'mode': 'apply' if apply_mode else 'report',
        'summary': {
            'existing_products': len(existing),
            'existing_families': len(existing_families),
            'scraped_families': len(scraped_families),
            'new_families': len(new_family_set),
            'missing_families': len(missing_families),
            'new_product_entries': len(new_products),
        },
        'new_families': [
            {
                'slug': slug,
                'name': scraped[slug].get('family_name', ''),
                'model_no': scraped[slug].get('model_no', ''),
                'category': scraped[slug].get('category', ''),
                'url': scraped[slug].get('url', ''),
                'features': scraped[slug].get('features', [])[:10],
                'image_count': len(scraped[slug].get('images', [])),
            }
            for slug in sorted(new_family_set) if slug in scraped
        ],
        'missing_families': sorted(missing_families),
        'new_products': new_products,
    }
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  Report saved: {REPORT_FILE}")
    
    # Apply if requested
    if apply_mode and new_products:
        print("\n[4/4] Applying updates...")
        updated = existing + new_products
        with open(PRODUCTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(updated, f, indent=2, ensure_ascii=False)
        print(f"  products.json updated: {len(existing)} -> {len(updated)} products")
        print("  NOTE: Run 'python site/build.py' to rebuild the website.")
    else:
        print("\n[4/4] Report mode - no changes applied.")
        print("  Run with --apply to add new products to products.json")
    
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == '__main__':
    main()
