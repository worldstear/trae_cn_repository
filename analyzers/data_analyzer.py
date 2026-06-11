import pandas as pd
import numpy as np
from utils.logging import get_logger
from config import DATA_DIR, OUTPUT_DIR
import os

class DataAnalyzer:
    def __init__(self):
        self.logger = get_logger('analyzer')
    
    def clean_and_deduplicate(self, items):
        if not items:
            return []
        
        df = pd.DataFrame(items)
        
        df = df.drop_duplicates(subset=['unique_id'], keep='first')
        
        df = df.dropna(subset=['name', 'price'])
        
        df = df[df['price'] > 0]
        
        df = df.drop_duplicates(subset=['name', 'price'], keep='first')
        
        return df.to_dict('records')
    
    def sort_by_price(self, items, ascending=True):
        return sorted(items, key=lambda x: x['price'], reverse=not ascending)
    
    def add_value_score(self, items):
        if not items:
            return items
        
        df = pd.DataFrame(items)
        
        if 'sales' in df.columns and 'rating' in df.columns:
            df['sales_norm'] = (df['sales'] - df['sales'].min()) / (df['sales'].max() - df['sales'].min() + 1e-10)
            df['rating_norm'] = df['rating'] / 5.0 if df['rating'].max() > 0 else 0
            df['price_norm'] = 1 - (df['price'] - df['price'].min()) / (df['price'].max() - df['price'].min() + 1e-10)
            
            df['value_score'] = 0.3 * df['sales_norm'] + 0.3 * df['rating_norm'] + 0.4 * df['price_norm']
            df['value_score'] = (df['value_score'] * 100).round(2)
        else:
            df['value_score'] = 0.0
        
        return df.to_dict('records')
    
    def analyze_prices(self, items):
        if not items:
            return {}
        
        df = pd.DataFrame(items)
        
        stats = {
            'total_items': len(df),
            'avg_price': float(df['price'].mean().round(2)),
            'min_price': float(df['price'].min()),
            'max_price': float(df['price'].max()),
            'median_price': float(df['price'].median()),
            'price_range': float((df['price'].max() - df['price'].min()).round(2))
        }
        
        platform_stats = df.groupby('platform')['price'].agg(['count', 'mean', 'min', 'max']).to_dict()
        stats['platform_stats'] = platform_stats
        
        return stats
    
    def compare_products(self, items):
        if not items:
            return []
        
        df = pd.DataFrame(items)
        df = df.sort_values('price')
        
        comparison = []
        for _, row in df.iterrows():
            comparison.append({
                'platform': row['platform'],
                'name': row['name'],
                'price': float(row['price']),
                'sales': int(row['sales']) if 'sales' in row else 0,
                'rating': float(row['rating']) if 'rating' in row else 0.0,
                'url': row['url'],
                'shop': row['shop'] if 'shop' in row else '',
                'value_score': float(row['value_score']) if 'value_score' in row else 0.0
            })
        
        return comparison
    
    def save_to_excel(self, items, keyword):
        if not items:
            return None
        
        df = pd.DataFrame(items)
        filename = f'{keyword}_comparison_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        df.to_excel(filepath, index=False, encoding='utf-8')
        self.logger.info(f'Data saved to {filepath}')
        
        return filepath