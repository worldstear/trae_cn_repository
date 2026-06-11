import requests
import time
import random
from utils.logging import get_logger
from config import DEFAULT_TIMEOUT, MAX_RETRIES

class BaseSpider:
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.logger = get_logger(f'spider.{platform_name}')
    
    def get(self, url, params=None, headers=None, timeout=DEFAULT_TIMEOUT):
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                self.logger.warning(f'Request failed (attempt {attempt+1}/{MAX_RETRIES}): {e}')
                time.sleep(random.uniform(1, 3))
        return None
    
    def search(self, keyword, max_pages=1):
        raise NotImplementedError('Subclasses must implement search method')
    
    def extract_items(self, html):
        raise NotImplementedError('Subclasses must implement extract_items method')