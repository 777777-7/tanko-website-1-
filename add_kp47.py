# -*- coding: utf-8 -*-
"""Add KP-47 product with images to products.json."""
import json
import os
import requests
from PIL import Image
import io

WEBSITE_DIR = r'C:\Users\User\Documents\GitHub\tanko-website-1-'
PRODUCTS_JSON = os.path.join(WEBSITE_DIR, 'products.json')
ASSET_DIR = os.path.join(WEBSITE_DIR, 'docs', 'asset3')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# KP-47 product data from tanko.tw
KP47_DATA = {
    "sku": "KP-4701",
    "product_family": "Tray",
    "family_slug": "kp-47",
    "category": "Perforated Board",
    "category_slug": "perforated-board",
    "subcategory": "Accessories",
    "color": "Black, White",
    "dimensions": "W250 x D100 x H60 mm",
    "material": "Steel",
    "load_capacity": None,
    "attributes": {
        "Dimensions": "W250 x D100 x H60 mm",
        "Color": "Black, White",
        "Material": "Steel",
        "Application": "Perforated Board",
    },
    "image_paths": [],
    "tanko_url": "https://www.tanko.com.tw/en/products-detail/kp-47/",
    "evidence": {"tanko": True, "pdf": False, "image": True},
    "distinct_title": "Tray for Perforated Board - KP-4701",
    "product_type": "mother_product",
    "specification": "Features:\n- Can be applied to perforated boards\n- Ideal for storing small parts and tools\n- Durable steel construction\n- Available in Black and White\n- Dimensions: W250 x D100 x H60 mm",
}

# Product images from tanko.tw (filtered - only product images, not related)
KP47_IMAGES = [
    "https://www.tanko.com.tw/upload/catalog_products_b/ALL_catalog_products_25B10_hiDv3vLY8h.png",
]

def download_and_convert_image(url, output_path):
    """Download image and convert to webp."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        img = Image.open(io.BytesIO(r.content))
        # Convert to RGB if RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(output_path, 'WEBP', quality=85)
        return True
    except Exception as e:
        print(f"  ERROR downloading {url}: {e}")
        return False

def main():
    # Ensure asset directory exists
    os.makedirs(ASSET_DIR, exist_ok=True)
    
    # Download images
    print("Downloading KP-47 images...")
    image_paths = []
    for i, url in enumerate(KP47_IMAGES):
        filename = f"kp-47-{i+1}.webp"
        output_path = os.path.join(ASSET_DIR, filename)
        print(f"  {url} -> {filename}")
        if download_and_convert_image(url, output_path):
            image_paths.append(f"asset3/{filename}")
    
    KP47_DATA["image_paths"] = image_paths
    print(f"Downloaded {len(image_paths)} images")
    
    # Load existing products
    print("\nLoading products.json...")
    with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
        products = json.load(f)
    print(f"Existing products: {len(products)}")
    
    # Check if already exists
    existing = [p for p in products if p.get('sku') == 'KP-4701']
    if existing:
        print("KP-4701 already exists, updating...")
        products = [p for p in products if p.get('sku') != 'KP-4701']
    
    # Add new product
    products.append(KP47_DATA)
    
    # Save
    with open(PRODUCTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Updated products.json: {len(products)} products")
    
    print("\nKP-47 product added successfully!")
    print(f"  SKU: {KP47_DATA['sku']}")
    print(f"  Family: {KP47_DATA['product_family']}")
    print(f"  Category: {KP47_DATA['category']}")
    print(f"  Images: {len(image_paths)}")

if __name__ == '__main__':
    main()
