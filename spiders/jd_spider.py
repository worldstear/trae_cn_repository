from spiders.base_spider import BaseSpider
from utils.helpers import get_random_headers, extract_price, extract_sales, extract_rating, clean_text, generate_unique_id
from bs4 import BeautifulSoup

class JDSPider(BaseSpider):
    def __init__(self):
        super().__init__('jd')
    
    def search(self, keyword, max_pages=1):
        items = []
        for page in range(1, max_pages + 1):
            url = f'https://search.jd.com/Search?keyword={keyword}&page={page}'
            headers = get_random_headers()
            response = self.get(url, headers=headers)
            if response:
                items.extend(self.extract_items(response.text))
        return items
    
    def extract_items(self, html):
        items = []
        soup = BeautifulSoup(html, 'lxml')
        product_list = soup.find_all('div', class_='gl-i-wrap')
        
        for item in product_list:
            try:
                name_tag = item.find('div', class_='p-name')
                price_tag = item.find('div', class_='p-price')
                sales_tag = item.find('div', class_='p-commit')
                shop_tag = item.find('div', class_='p-shop')
                url_tag = item.find('a', class_='J_ClickStat')
                
                name = clean_text(name_tag.get_text() if name_tag else '')
                price = extract_price(price_tag.get_text() if price_tag else '')
                sales = extract_sales(sales_tag.get_text() if sales_tag else '')
                rating = extract_rating(shop_tag.get_text() if shop_tag else '')
                url = 'https:' + url_tag['href'] if url_tag and 'href' in url_tag.attrs else ''
                
                if name and price > 0:
                    items.append({
                        'unique_id': generate_unique_id({'platform': 'jd', 'name': name, 'price': price}),
                        'platform': '京东',
                        'name': name,
                        'price': price,
                        'sales': sales,
                        'rating': rating,
                        'url': url,
                        'shop': clean_text(shop_tag.get_text() if shop_tag else '')
                    })
            except Exception as e:
                self.logger.error(f'Error extracting item: {e}')
        
        return items