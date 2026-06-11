from spiders.base_spider import BaseSpider
from utils.helpers import extract_price, extract_sales, extract_rating, clean_text, generate_unique_id
from bs4 import BeautifulSoup
import random

class TaobaoSpider(BaseSpider):
    def __init__(self):
        super().__init__('taobao')
    
    def search(self, keyword, max_pages=1):
        return self._get_mock_data(keyword)
    
    def _get_mock_data(self, keyword):
        mock_items = [
            {'name': f'{keyword} Pro Max 256GB 国行正品', 'price': 8799.0, 'sales': 12300, 'rating': 4.8, 'url': 'https://item.taobao.com/item.htm?id=1234567890', 'shop': '天猫官方旗舰店'},
            {'name': f'{keyword} Pro 128GB 全新未拆封', 'price': 6799.0, 'sales': 18900, 'rating': 4.7, 'url': 'https://item.taobao.com/item.htm?id=1234567891', 'shop': '数码专营店'},
            {'name': f'{keyword} 标准版 256GB 双卡双待', 'price': 5799.0, 'sales': 28500, 'rating': 4.6, 'url': 'https://item.taobao.com/item.htm?id=1234567892', 'shop': '手机专卖店铺'},
            {'name': f'{keyword} Pro Max 512GB 全网通', 'price': 10799.0, 'sales': 6700, 'rating': 4.8, 'url': 'https://item.taobao.com/item.htm?id=1234567893', 'shop': '天猫官方旗舰店'},
            {'name': f'{keyword} SE 128GB 特惠版', 'price': 4299.0, 'sales': 38900, 'rating': 4.5, 'url': 'https://item.taobao.com/item.htm?id=1234567894', 'shop': '手机折扣店'},
        ]
        
        items = []
        for item in mock_items:
            items.append({
                'unique_id': generate_unique_id({'platform': 'taobao', 'name': item['name'], 'price': item['price']}),
                'platform': '淘宝',
                'name': item['name'],
                'price': item['price'] * (0.93 + random.random() * 0.14),
                'sales': item['sales'] + random.randint(-5000, 5000),
                'rating': max(4.0, min(5.0, item['rating'] + (random.random() - 0.5) * 0.4)),
                'url': item['url'],
                'shop': item['shop']
            })
        
        return items
    
    def extract_items(self, html):
        return []