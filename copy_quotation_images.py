# -*- coding: utf-8 -*-
"""Copy product images from website to quotation assets."""
import json
import os
import re
import shutil

WEBSITE_PRODUCTS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\products.json'
WEBSITE_ROOT = r'C:\Users\User\Documents\GitHub\tanko-website-1-'
QUOTATION_ASSETS = r'C:\Users\User\Documents\GitHub\tanko-quotation\assets\product'

def get_image_filename(sku, image_paths):
    if not image_paths:
        return None
    first = image_paths[0]
    basename = os.path.basename(first)
    ext = os.path.splitext(basename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        ext = '.jpg'
    clean_sku = re.sub(r'[^\w\-+]', '_', sku)
    return f"{clean_sku}{ext}"

def main():
    with open(WEBSITE_PRODUCTS, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    seen = set()
    copied = 0
    skipped = 0
    errors = 0
    
    for p in products:
        sku = p.get('sku', '')
        if not sku or sku in seen:
            continue
        seen.add(sku)
        
        img_paths = p.get('image_paths', [])
        if not img_paths:
            continue
        
        img_filename = get_image_filename(sku, img_paths)
        if not img_filename:
            continue
        
        src = os.path.join(WEBSITE_ROOT, img_paths[0].replace('/', os.sep))
        dst = os.path.join(QUOTATION_ASSETS, img_filename)
        
        if os.path.exists(dst):
            skipped += 1
            continue
        
        if os.path.exists(src):
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
            except Exception as e:
                print(f"  ERROR {sku}: {e}")
                errors += 1
        else:
            errors += 1
            if errors <= 10:
                print(f"  NOT FOUND: {src}")
    
    print(f"\n=== DONE ===")
    print(f"  Copied: {copied}")
    print(f"  Already existed: {skipped}")
    print(f"  Errors/not found: {errors}")
    print(f"  Total products: {len(seen)}")
    
    # Verify specific products
    for sku in ['ME-321', 'WKT-5102F', 'KP-4701']:
        dst = os.path.join(QUOTATION_ASSETS, f"{sku}.jpg")
        dst_webp = os.path.join(QUOTATION_ASSETS, f"{sku}.webp")
        exists = os.path.exists(dst) or os.path.exists(dst_webp)
        print(f"  {sku} image exists: {exists}")

if __name__ == '__main__':
    main()
