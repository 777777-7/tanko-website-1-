# -*- coding: utf-8 -*-
"""
Tanko.tw Product Scraper
Scrapes product family pages, extracts SKUs, specs, features, images.
"""
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import os
from urllib.parse import urljoin

BASE_URL = 'https://www.tanko.com.tw/en'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Category mapping from tanko.tw to website category_slug
CATEGORY_MAP = {
    'Workstation': 'workstation',
    'Workbench': 'workbench',
    'Tool Cabinet': 'tool-cabinet',
    'CNC Tool Cabinet': 'cnc-tool',
    'Rack': 'rack',
    'Hanger Rack': 'hanger-rack',
    'Locker': 'locker',
    'Parts Cabinet': 'parts-cabinet',
    'Documents Cabinet': 'documents-cabinet',
    'Perforated Board': 'perforated-board',
    'For Home': 'household-items',
}


def get_page(url):
    """Fetch a page and return BeautifulSoup object."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def get_product_families():
    """Get all product family URLs from the products page."""
    families = {}  # slug -> {name, url, category}
    
    # First get the main products page
    print("Fetching products page...")
    soup = get_page(f'{BASE_URL}/products/')
    if not soup:
        return families
    
    # Get category links from navigation (deduplicate)
    cat_links = []
    seen_cats = set()
    for a in soup.find_all('a', href=re.compile(r'/en/products/[^/]+/$')):
        href = a.get('href', '')
        name = a.get_text(strip=True)
        if name and name not in ['Products', 'Download', 'Contact Us'] and name not in seen_cats:
            seen_cats.add(name)
            cat_links.append((name, href))
    
    print(f"Found {len(cat_links)} categories")
    
    # For each category, get product families
    for cat_name, cat_url in cat_links:
        print(f"  Fetching category: {cat_name}")
        cat_soup = get_page(cat_url)
        if not cat_soup:
            continue
        
        # Find product detail links
        for a in cat_soup.find_all('a', href=re.compile(r'products-detail/([^/]+)/')):
            href = a.get('href', '')
            match = re.search(r'products-detail/([^/]+)/', href)
            if match:
                slug = match.group(1)
                name = a.get_text(strip=True)
                if slug not in families and name and len(name) > 2:
                    families[slug] = {
                        'slug': slug,
                        'name': name,
                        'url': href if href.startswith('http') else urljoin(BASE_URL, href),
                        'category': cat_name,
                    }
    
    print(f"Total product families found: {len(families)}")
    return families


def scrape_family(url, slug):
    """Scrape a single product family page."""
    soup = get_page(url)
    if not soup:
        return None
    
    result = {
        'slug': slug,
        'url': url,
        'family_name': '',
        'category': '',
        'subcategory': '',
        'model_no': '',
        'spec_options': {},
        'features': [],
        'images': [],
        'description': '',
        'related_families': [],
    }
    
    # Family name from title
    title = soup.find('title')
    if title:
        result['family_name'] = title.get_text(strip=True).replace('-tanko', '').strip()
    
    # Breadcrumb for category - use the 3rd item (category name like Workstation)
    breadcrumb = soup.find('script', type='application/ld+json')
    if breadcrumb:
        try:
            data = json.loads(breadcrumb.string)
            if isinstance(data, dict) and data.get('@type') == 'BreadcrumbList':
                items = data.get('itemListElement', [])
                # items: [HOME, Products, Category, Subcategory(optional)]
                if len(items) >= 3:
                    result['category'] = items[2]['item']['name']
                if len(items) >= 4:
                    result['subcategory'] = items[3]['item']['name']
        except:
            pass
    
    # Model No.
    model_el = soup.find(string=re.compile(r'Model\s*No', re.I))
    if model_el:
        parent = model_el.find_parent()
        if parent:
            strong = parent.find('strong')
            if strong:
                result['model_no'] = strong.get_text(strip=True)
    
    # Specification options (level1, level2)
    spec_list = soup.find(class_='specList')
    if spec_list:
        for level in spec_list.find_all('li', class_=re.compile(r'level')):
            label_el = level.find('label')
            level_name = label_el.get_text(strip=True).rstrip('：').rstrip(':') if label_el else 'unknown'
            options = []
            for item in level.find_all(class_='item'):
                inp = item.find('input')
                opt_label = item.find('label')
                if inp and opt_label:
                    options.append({
                        'id': inp.get('data-id', ''),
                        'name': opt_label.get_text(strip=True),
                    })
            if options:
                result['spec_options'][level_name] = options
    
    # Features
    features_section = soup.find(string=re.compile(r'^Features$', re.I))
    if features_section:
        parent = features_section.find_parent()
        if parent:
            # Find feature items - look for the next section
            next_sibling = parent.find_next_sibling()
            while next_sibling:
                for item in next_sibling.find_all(['h3', 'h4', 'strong', 'dt']):
                    text = item.get_text(strip=True)
                    if text and len(text) < 100:
                        result['features'].append(text)
                next_sibling = next_sibling.find_next_sibling()
    
    # If no features found, try alternative extraction
    if not result['features']:
        for h3 in soup.find_all('h3'):
            text = h3.get_text(strip=True)
            if text and len(text) < 80 and text not in ['Features', 'Products', 'Contact Us']:
                result['features'].append(text)
    
    # Images (product images only, not logos/icons)
    for img in soup.find_all('img'):
        src = img.get('src', '') or img.get('data-src', '')
        if src and 'upload/catalog_products' in src:
            if src not in result['images']:
                result['images'].append(src)
    
    # Description
    desc_el = soup.find(class_='paragraph')
    if desc_el:
        result['description'] = desc_el.get_text(strip=True)[:500]
    
    # Related families
    related = soup.find(class_='relatedProducts')
    if related:
        for a in related.find_all('a', href=re.compile(r'products-detail/')):
            href = a.get('href', '')
            match = re.search(r'products-detail/([^/]+)/', href)
            if match:
                rel_slug = match.group(1)
                if rel_slug != slug and rel_slug not in result['related_families']:
                    result['related_families'].append(rel_slug)
    
    return result


def scrape_all(delay=1.0):
    """Scrape all product families."""
    families = get_product_families()
    results = {}
    
    for i, (slug, info) in enumerate(families.items()):
        print(f"[{i+1}/{len(families)}] Scraping: {slug} - {info['name']}")
        data = scrape_family(info['url'], slug)
        if data:
            data['category'] = data['category'] or info['category']
            results[slug] = data
        time.sleep(delay)
    
    return results


if __name__ == '__main__':
    # Test with one family first
    print("Testing single family scrape...")
    data = scrape_family(f'{BASE_URL}/products-detail/ry/', 'ry')
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
