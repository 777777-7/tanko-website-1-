# -*- coding: utf-8 -*-
"""
Update tanko-quotation index.html:
1. Regenerate PRODUCT_DATA from website products.json (all 1761 products)
2. Regenerate PRODUCT_IMAGES mapping
3. Add product thumbnail images to search suggestions
4. Copy new product images to assets/product/
"""
import json
import os
import re
import shutil

WEBSITE_PRODUCTS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\products.json'
WEBSITE_ASSETS = r'C:\Users\User\Documents\GitHub\tanko-website-1-'  # root, image_paths are relative to this
QUOTATION_HTML = r'C:\Users\User\Documents\GitHub\tanko-quotation\index.html'
QUOTATION_ASSETS = r'C:\Users\User\Documents\GitHub\tanko-quotation\assets\product'

def build_product_name(p):
    """Build product name string from product data."""
    parts = []
    if p.get('product_family'):
        parts.append(p['product_family'])
    if p.get('subcategory') and p['subcategory'] != p.get('product_family'):
        parts.append(p['subcategory'])
    # Add attributes
    if p.get('attributes'):
        for key, val in p['attributes'].items():
            if val and key.lower() not in ['dimensions', 'color', 'material']:
                parts.append(f"{key}: {val}")
    if p.get('color'):
        parts.append(f"Color: {p['color']}")
    if p.get('material'):
        parts.append(f"Material: {p['material']}")
    if p.get('dimensions'):
        parts.append(f"Size: {p['dimensions']}")
    if p.get('load_capacity'):
        parts.append(f"Weight Hold: {p['load_capacity']}")
    return '\n'.join(parts)

def get_image_filename(sku, image_paths):
    """Get a clean filename for the product image."""
    if not image_paths:
        return None
    # Use first image
    first = image_paths[0]
    # Extract filename
    basename = os.path.basename(first)
    # Convert to clean SKU-based name
    ext = os.path.splitext(basename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        ext = '.jpg'
    # Clean SKU for filename
    clean_sku = re.sub(r'[^\w\-+]', '_', sku)
    return f"{clean_sku}{ext}"

def main():
    # Load website products
    print("Loading website products...")
    with open(WEBSITE_PRODUCTS, 'r', encoding='utf-8') as f:
        products = json.load(f)
    print(f"  Total products: {len(products)}")

    # Deduplicate by SKU
    seen_skus = set()
    unique_products = []
    for p in products:
        sku = p.get('sku', '')
        if sku and sku not in seen_skus:
            seen_skus.add(sku)
            unique_products.append(p)
    print(f"  Unique SKUs: {len(unique_products)}")

    # Generate PRODUCT_DATA entries
    print("\nGenerating PRODUCT_DATA...")
    product_data_lines = []
    product_images = {}
    images_to_copy = []

    for p in unique_products:
        sku = p.get('sku', '')
        name = build_product_name(p)
        # Escape quotes in name
        name_escaped = name.replace('"', '\\"').replace("'", "\\'")
        product_data_lines.append(f'  {{ sku: "{sku}", name: "{name_escaped}", base_price: 0.0 }},')

        # Image mapping
        img_paths = p.get('image_paths', [])
        if img_paths:
            img_filename = get_image_filename(sku, img_paths)
            if img_filename:
                product_images[sku] = img_filename
                # Track images to copy
                src = os.path.join(WEBSITE_ASSETS, img_paths[0].replace('/', os.sep))
                dst = os.path.join(QUOTATION_ASSETS, img_filename)
                images_to_copy.append((src, dst, sku))

    print(f"  PRODUCT_DATA entries: {len(product_data_lines)}")
    print(f"  PRODUCT_IMAGES entries: {len(product_images)}")

    # Copy images
    print(f"\nCopying {len(images_to_copy)} product images...")
    copied = 0
    for src, dst, sku in images_to_copy:
        if os.path.exists(src) and not os.path.exists(dst):
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
            except Exception as e:
                print(f"  ERROR copying {sku}: {e}")
    print(f"  Copied {copied} new images")

    # Read quotation HTML
    print("\nReading quotation HTML...")
    with open(QUOTATION_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace PRODUCT_DATA
    print("Replacing PRODUCT_DATA...")
    new_product_data = 'const PRODUCT_DATA = [\n' + '\n'.join(product_data_lines) + '\n];'
    html = re.sub(
        r'const PRODUCT_DATA = \[.*?\];',
        new_product_data,
        html,
        flags=re.DOTALL
    )

    # Replace PRODUCT_IMAGES
    print("Replacing PRODUCT_IMAGES...")
    img_lines = [f'  "{sku}": "{filename}",' for sku, filename in product_images.items()]
    new_product_images = 'const PRODUCT_IMAGES = {\n' + '\n'.join(img_lines) + '\n};'
    html = re.sub(
        r'const PRODUCT_IMAGES = \{.*?\};',
        new_product_images,
        html,
        flags=re.DOTALL
    )

    # Update renderSuggestions to include product thumbnails
    print("Updating renderSuggestions with thumbnails...")
    old_render = '''function renderSuggestions(results) {
  activeSuggestionIndex = -1;
  el.suggestions.innerHTML = "";
  if (results.length === 0) {
    el.suggestions.classList.remove("open");
    return;
  }
  results.forEach((product) => {
    const item = document.createElement("div");
    item.innerHTML =
      "<span class=\\"sug-sku\\">" + escapeHtml(product.sku) + "</span>" +
      "<span class=\\"sug-name\\"> - " + escapeHtml(product.name.replace(/\\n/g, " / ")) + "</span>";
    item.addEventListener("click", () => selectProduct(product));
    el.suggestions.appendChild(item);
  });
  el.suggestions.classList.add("open");
}'''

    new_render = '''function renderSuggestions(results) {
  activeSuggestionIndex = -1;
  el.suggestions.innerHTML = "";
  if (results.length === 0) {
    el.suggestions.classList.remove("open");
    return;
  }
  results.forEach((product) => {
    const item = document.createElement("div");
    item.className = "sug-item";
    const imgPath = getProductImagePath(product.sku);
    const imgHtml = imgPath
      ? '<img class="sug-thumb" src="' + imgPath + '" onerror="this.style.display=\\'none\\'" alt="">'
      : '<span class="sug-thumb sug-thumb-placeholder"></span>';
    item.innerHTML =
      imgHtml +
      '<div class="sug-text">' +
      "<span class=\\"sug-sku\\">" + escapeHtml(product.sku) + "</span>" +
      "<span class=\\"sug-name\\">" + escapeHtml(product.name.replace(/\\n/g, " / ")) + "</span>" +
      '</div>';
    item.addEventListener("click", () => selectProduct(product));
    el.suggestions.appendChild(item);
  });
  el.suggestions.classList.add("open");
}'''

    if old_render in html:
        html = html.replace(old_render, new_render)
        print("  renderSuggestions updated")
    else:
        print("  WARNING: Could not find exact renderSuggestions match, trying regex...")
        # Try regex replacement
        html = re.sub(
            r'function renderSuggestions\(results\) \{.*?\n\}',
            new_render,
            html,
            flags=re.DOTALL
        )

    # Add CSS for suggestion thumbnails
    print("Adding CSS for thumbnails...")
    thumb_css = '''
/* Search suggestion thumbnails */
.sug-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid var(--border);
}
.sug-item:hover {
  background: var(--surface-alt);
}
.sug-thumb {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 4px;
  background: var(--surface-alt);
  flex-shrink: 0;
}
.sug-thumb-placeholder {
  display: inline-block;
  width: 48px;
  height: 48px;
  background: var(--surface-alt);
  border-radius: 4px;
  flex-shrink: 0;
}
.sug-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.sug-sku {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--ink);
}
.sug-name {
  font-size: 0.8rem;
  color: var(--ink-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
'''
    # Insert before </style>
    if '</style>' in html:
        html = html.replace('</style>', thumb_css + '\n</style>')
        print("  CSS added")

    # Write updated HTML
    print("\nWriting updated HTML...")
    with open(QUOTATION_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n=== DONE ===")
    print(f"  PRODUCT_DATA: {len(product_data_lines)} products")
    print(f"  PRODUCT_IMAGES: {len(product_images)} products with images")
    print(f"  Images copied: {copied}")
    print(f"  Search thumbnails: added")
    print(f"\n  ME-321 in data: {'ME-321' in seen_skus}")
    print(f"  WKT-5102F in data: {'WKT-5102F' in seen_skus}")
    print(f"  KP-4701 in data: {'KP-4701' in seen_skus}")

if __name__ == '__main__':
    main()
