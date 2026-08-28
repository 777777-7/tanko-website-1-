# -*- coding: utf-8 -*-
"""
批量爬取 tanko.tw 产品系列页面，提取详细规格，更新 products.json。
添加 specification, description, features 字段。
"""
import requests
from bs4 import BeautifulSoup
import json
import re
import time
import sys
import os

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def scrape_series_page(url):
    """爬取一个系列页面，返回系列信息和各型号规格。"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        for s in soup(['script', 'style']):
            s.decompose()
        
        # 获取页面完整文本
        full_text = soup.get_text(separator='\n', strip=True)
        lines = [l.strip() for l in full_text.split('\n') if l.strip()]
        
        # 提取系列描述（Features 部分）
        features = []
        in_features = False
        for i, line in enumerate(lines):
            if line == 'Features' and i > 0:
                in_features = True
                continue
            if in_features:
                if line in ['How to choose', 'Specification', 'Model No.']:
                    break
                if line and not line.startswith('Step.') and line != '▲':
                    features.append(line)
        
        # 提取各型号规格
        models = {}
        current_model = None
        i = 0
        while i < len(lines):
            line = lines[i]
            if line == 'Model No.':
                # 下一行是型号
                if i + 1 < len(lines):
                    current_model = lines[i + 1]
                    models[current_model] = {}
                    i += 2
                    continue
            elif current_model and line in ['Dimensions', 'Dimensions：', 'Dimensions :']:
                # 找尺寸值
                j = i + 1
                dim_parts = []
                while j < len(lines) and lines[j] not in ['Material', 'Model No.', 'Items included', 'Desktop', 'Load capacity', 'Loading']:
                    if lines[j] not in ['：', ':']:
                        dim_parts.append(lines[j])
                    j += 1
                models[current_model]['dimensions'] = ' '.join(dim_parts).strip()
                i = j
                continue
            elif current_model and line == 'Material':
                j = i + 1
                mat_parts = []
                while j < len(lines) and lines[j] not in ['Model No.', 'Items included', 'Desktop', 'Load capacity', 'Loading', 'Dimensions']:
                    if lines[j] not in ['：', ':']:
                        mat_parts.append(lines[j])
                    j += 1
                models[current_model]['material'] = ' '.join(mat_parts).strip()
                i = j
                continue
            elif current_model and line == 'Desktop':
                j = i + 1
                desk_parts = []
                while j < len(lines) and lines[j] not in ['Model No.', 'Items included', 'Material', 'Load capacity', 'Loading', 'Dimensions']:
                    if lines[j] not in ['：', ':']:
                        desk_parts.append(lines[j])
                    j += 1
                models[current_model]['desktop'] = ' '.join(desk_parts).strip()
                i = j
                continue
            elif current_model and line == 'Items included':
                j = i + 1
                items = []
                while j < len(lines) and lines[j] != 'Model No.':
                    if lines[j] not in ['：', ':']:
                        items.append(lines[j])
                    j += 1
                models[current_model]['items_included'] = items
                i = j
                continue
            elif current_model and line in ['Load capacity', 'Loading']:
                j = i + 1
                load_parts = []
                while j < len(lines) and lines[j] not in ['Model No.', 'Items included', 'Material', 'Desktop', 'Dimensions']:
                    if lines[j] not in ['：', ':']:
                        load_parts.append(lines[j])
                    j += 1
                models[current_model]['load_capacity'] = ' '.join(load_parts).strip()
                i = j
                continue
            i += 1
        
        return {
            'url': url,
            'features': features,
            'models': models,
            'raw_text': full_text[:5000]
        }
    except Exception as e:
        print(f"  错误: {e}")
        return None

def match_sku_to_model(sku, models):
    """将 products.json 的 SKU 匹配到页面上的型号。"""
    # 精确匹配
    if sku in models:
        return sku
    
    # 模糊匹配：去掉后缀字母
    sku_base = re.sub(r'[A-Z]+$', '', sku)
    for model in models:
        model_base = re.sub(r'[A-Z]+$', '', model)
        if sku_base == model_base:
            return model
    
    # 前缀匹配
    for model in models:
        if sku.startswith(model) or model.startswith(sku):
            return model
    
    return None

def main():
    # 读取 products.json
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"产品总数: {len(products)}")
    
    # 提取唯一 URL
    urls = {}
    for p in products:
        url = p.get('tanko_url', '')
        if url:
            if url not in urls:
                urls[url] = []
            urls[url].append(p['sku'])
    
    print(f"唯一系列页面数: {len(urls)}")
    
    # 爬取每个页面
    results = {}
    success = 0
    fail = 0
    
    for idx, (url, skus) in enumerate(urls.items()):
        print(f"\n[{idx+1}/{len(urls)}] 爬取: {url} ({len(skus)} 个 SKU)")
        data = scrape_series_page(url)
        if data:
            results[url] = data
            model_count = len(data['models'])
            print(f"  成功: {model_count} 个型号, {len(data['features'])} 条特性")
            success += 1
        else:
            fail += 1
            print(f"  失败")
        
        # 每爬取 10 个页面保存一次
        if (idx + 1) % 10 == 0:
            with open('_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  已保存中间结果 ({len(results)} 个页面)")
        
        time.sleep(0.5)  # 礼貌延迟
    
    # 保存最终结果
    with open('_scraped_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n爬取完成: 成功 {success}, 失败 {fail}")
    
    # 更新 products.json
    updated = 0
    for p in products:
        url = p.get('tanko_url', '')
        if url in results:
            data = results[url]
            
            # 添加 features（系列级别的特性）
            if data['features'] and not p.get('features'):
                p['features'] = data['features']
            
            # 匹配型号，添加规格
            model_key = match_sku_to_model(p['sku'], data['models'])
            if model_key and model_key in data['models']:
                model = data['models'][model_key]
                
                spec_parts = []
                if model.get('dimensions'):
                    spec_parts.append(f"Dimensions: {model['dimensions']}")
                if model.get('material'):
                    spec_parts.append(f"Material: {model['material']}")
                if model.get('desktop'):
                    spec_parts.append(f"Desktop: {model['desktop']}")
                if model.get('load_capacity'):
                    spec_parts.append(f"Load Capacity: {model['load_capacity']}")
                if model.get('items_included'):
                    items_str = ', '.join(model['items_included'][:10])
                    spec_parts.append(f"Items Included: {items_str}")
                
                if spec_parts and not p.get('specification'):
                    p['specification'] = '\n'.join(spec_parts)
                
                # 添加描述
                if not p.get('description') and data['features']:
                    p['description'] = ' '.join(data['features'][:5])
                
                updated += 1
    
    # 保存更新后的 products.json
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"更新产品数: {updated}")
    print(f"有 specification 的产品数: {sum(1 for p in products if p.get('specification'))}")
    print(f"有 description 的产品数: {sum(1 for p in products if p.get('description'))}")
    print(f"有 features 的产品数: {sum(1 for p in products if p.get('features'))}")

if __name__ == '__main__':
    main()
