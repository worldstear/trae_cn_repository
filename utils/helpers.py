import random
from config import USER_AGENTS, HEADERS

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_random_headers():
    headers = HEADERS.copy()
    headers['User-Agent'] = get_random_user_agent()
    return headers

def extract_price(text):
    import re
    match = re.search(r'(\d+(?:\.\d+)?)', str(text))
    return float(match.group(1)) if match else 0.0

def extract_sales(text):
    import re
    text = str(text)
    match = re.search(r'(\d+(?:\.\d+)?)\s*(万|千|百)?', text)
    if match:
        num = float(match.group(1))
        unit = match.group(2)
        if unit == '万':
            return int(num * 10000)
        elif unit == '千':
            return int(num * 1000)
        elif unit == '百':
            return int(num * 100)
        return int(num)
    return 0

def extract_rating(text):
    import re
    match = re.search(r'(\d+(?:\.\d+)?)', str(text))
    return float(match.group(1)) if match else 0.0

def clean_text(text):
    if text:
        return ' '.join(str(text).strip().split())
    return ''

def format_price(price):
    return f'¥{price:.2f}'

def generate_unique_id(item):
    import hashlib
    key = f"{item.get('platform', '')}_{item.get('name', '')}_{item.get('price', 0)}"
    return hashlib.md5(key.encode()).hexdigest()