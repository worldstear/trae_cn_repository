from spiders.base_spider import BaseSpider
from utils.helpers import extract_price, extract_sales, extract_rating, clean_text, generate_unique_id
from bs4 import BeautifulSoup
import random

class PinduoduoSpider(BaseSpider):
    def __init__(self):
        super().__init__('pinduoduo')
    
    def search(self, keyword, max_pages=1):
        return self._get_mock_data(keyword)
    
    def _get_mock_data(self, keyword):
        mock_items = [
            {'name': f'{keyword} Pro Max 256GB 百亿补贴', 'price': 8499.0, 'sales': 25600, 'rating': 4.6, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123456', 'shop': '品牌官方店'},
            {'name': f'{keyword} Pro 128GB 官方正品', 'price': 6499.0, 'sales': 38900, 'rating': 4.5, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123457', 'shop': '数码专卖店'},
            {'name': f'{keyword} 标准版 256GB 国行版', 'price': 5499.0, 'sales': 52300, 'rating': 4.4, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123458', 'shop': '手机专营店'},
            {'name': f'{keyword} Pro Max 512GB 全网通', 'price': 10499.0, 'sales': 12800, 'rating': 4.6, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123459', 'shop': '品牌官方店'},
            {'name': f'{keyword} SE 128GB 特价版', 'price': 3999.0, 'sales': 68900, 'rating': 4.3, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123460', 'shop': '折扣手机店'},
        ]
        
        items = []
        for item in mock_items:
            items.append({
                'unique_id': generate_unique_id({'platform': 'pinduoduo', 'name': item['name'], 'price': item['price']}),
                'platform': '拼多多',
                'name': item['name'],
                'price': item['price'] * (0.90 + random.random() * 0.15),
                'sales': item['sales'] + random.randint(-10000, 10000),
                'rating': max(3.5, min(5.0, item['rating'] + (random.random() - 0.5) * 0.6)),
                'url': item['url'],
                'shop': item['shop']
            })
        
        return items
    
    def extract_items(self, html):
        return []