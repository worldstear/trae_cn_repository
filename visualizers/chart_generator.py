import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import OUTPUT_DIR
from utils.logging import get_logger

class ChartGenerator:
    def __init__(self):
        self.logger = get_logger('visualizer')
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_price_chart(self, items, keyword):
        if not items:
            return None
        
        import pandas as pd
        df = pd.DataFrame(items)
        df = df.sort_values('price').head(20)
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(df['name'], df['price'], color='skyblue')
        
        plt.title(f'{keyword} - 商品价格对比', fontsize=14)
        plt.xlabel('价格 (元)', fontsize=12)
        plt.ylabel('商品名称', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, f'¥{width:.2f}', va='center')
        
        plt.tight_layout()
        
        filename = f'{keyword}_price_chart_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f'Price chart saved to {filepath}')
        return filepath
    
    def generate_platform_distribution(self, items, keyword):
        if not items:
            return None
        
        import pandas as pd
        df = pd.DataFrame(items)
        
        platform_counts = df['platform'].value_counts()
        
        plt.figure(figsize=(8, 8))
        plt.pie(platform_counts.values, labels=platform_counts.index, 
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'))
        
        plt.title(f'{keyword} - 平台分布', fontsize=14)
        plt.tight_layout()
        
        filename = f'{keyword}_platform_dist_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f'Platform distribution chart saved to {filepath}')
        return filepath
    
    def generate_value_score_chart(self, items, keyword):
        if not items:
            return None
        
        import pandas as pd
        df = pd.DataFrame(items)
        df = df.sort_values('value_score', ascending=False).head(10)
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(df['name'], df['value_score'], color='green')
        
        plt.title(f'{keyword} - 性价比评分 Top 10', fontsize=14)
        plt.xlabel('商品名称', fontsize=12)
        plt.ylabel('性价比评分', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        filename = f'{keyword}_value_score_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f'Value score chart saved to {filepath}')
        return filepath
    
    def generate_price_sales_scatter(self, items, keyword):
        if not items:
            return None
        
        import pandas as pd
        df = pd.DataFrame(items)
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='price', y='sales', hue='platform', s=100, alpha=0.7)
        
        plt.title(f'{keyword} - 价格与销量关系', fontsize=14)
        plt.xlabel('价格 (元)', fontsize=12)
        plt.ylabel('销量', fontsize=12)
        plt.legend(title='平台')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        filename = f'{keyword}_price_sales_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f'Price-sales scatter chart saved to {filepath}')
        return filepath