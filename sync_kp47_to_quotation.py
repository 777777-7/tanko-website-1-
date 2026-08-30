# -*- coding: utf-8 -*-
"""Sync KP-4701 product to tanko-quotation data."""
import json
import os
import shutil

WEBSITE_PRODUCTS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\products.json'
QUOTATION_PRODUCTS = r'C:\Users\User\Documents\GitHub\tanko-quotation\data\products.json'
QUOTATION_ASSETS = r'C:\Users\User\Documents\GitHub\tanko-quotation\assets\product'

# Load website products
with open(WEBSITE_PRODUCTS, 'r', encoding='utf-8') as f:
    website_products = json.load(f)

# Find KP-4701
kp47 = next((p for p in website_products if p.get('sku') == 'KP-4701'), None)
if not kp47:
    print("KP-4701 not found in website products!")
    exit(1)

print("Found KP-4701 in website products:")
print(f"  SKU: {kp47['sku']}")
print(f"  Family: {kp47['product_family']}")
print(f"  Category: {kp47['category']}")
print(f"  Images: {kp47.get('image_paths', [])}")

# Load quotation products
with open(QUOTATION_PRODUCTS, 'r', encoding='utf-8') as f:
    quotation_products = json.load(f)

print(f"\nQuotation products before: {len(quotation_products)}")

# Check if already exists
existing = next((p for p in quotation_products if p.get('sku', '').upper() == 'KP-4701'), None)
if existing:
    print("KP-4701 already exists in quotation, updating...")
    quotation_products = [p for p in quotation_products if p.get('sku', '').upper() != 'KP-4701']

# Add KP-4701
quotation_products.append(kp47)

# Save
with open(QUOTATION_PRODUCTS, 'w', encoding='utf-8') as f:
    json.dump(quotation_products, f, indent=2, ensure_ascii=False)

print(f"Quotation products after: {len(quotation_products)}")

# Copy product image if exists
if kp47.get('image_paths'):
    for img_path in kp47['image_paths']:
        src = os.path.join(r'C:\Users\User\Documents\GitHub\tanko-website-1-\docs', img_path)
        if os.path.exists(src):
            dst = os.path.join(QUOTATION_ASSETS, 'KP-4701.webp')
            shutil.copy2(src, dst)
            print(f"Copied image: {dst}")

print("\nDone! KP-4701 synced to tanko-quotation.")
