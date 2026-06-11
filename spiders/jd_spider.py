from spiders.base_spider import BaseSpider
from utils.helpers import extract_price, extract_sales, extract_rating, clean_text, generate_unique_id
from bs4 import BeautifulSoup
import random

class JDSPider(BaseSpider):
    def __init__(self):
        super().__init__('jd')
    
    def search(self, keyword, max_pages=1):
        return self._get_mock_data(keyword)
    
    def _get_mock_data(self, keyword):
        mock_items = [
            {'name': f'{keyword} Pro Max 256GB 黑色', 'price': 8999.0, 'sales': 15680, 'rating': 4.9, 'url': 'https://item.jd.com/100123456789.html', 'shop': '京东自营旗舰店'},
            {'name': f'{keyword} Pro 128GB 白色', 'price': 6999.0, 'sales': 28900, 'rating': 4.8, 'url': 'https://item.jd.com/100123456790.html', 'shop': '京东自营旗舰店'},
            {'name': f'{keyword} 标准版 256GB 蓝色', 'price': 5999.0, 'sales': 42500, 'rating': 4.7, 'url': 'https://item.jd.com/100123456791.html', 'shop': '京东自营旗舰店'},
            {'name': f'{keyword} Pro Max 512GB 原色钛金属', 'price': 10999.0, 'sales': 8900, 'rating': 4.9, 'url': 'https://item.jd.com/100123456792.html', 'shop': '京东自营旗舰店'},
            {'name': f'{keyword} SE 128GB 红色', 'price': 4499.0, 'sales': 56200, 'rating': 4.6, 'url': 'https://item.jd.com/100123456793.html', 'shop': '京东自营旗舰店'},
        ]
        
        items = []
        for item in mock_items:
            items.append({
                'unique_id': generate_unique_id({'platform': 'jd', 'name': item['name'], 'price': item['price']}),
                'platform': '京东',
                'name': item['name'],
                'price': item['price'] * (0.95 + random.random() * 0.1),
                'sales': item['sales'] + random.randint(-5000, 5000),
                'rating': max(4.0, min(5.0, item['rating'] + (random.random() - 0.5) * 0.4)),
                'url': item['url'],
                'shop': item['shop']
            })
        
        return items
    
    def extract_items(self, html):
        return []