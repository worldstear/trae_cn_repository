import argparse
import time
from spiders.jd_spider import JDSPider
from spiders.taobao_spider import TaobaoSpider
from spiders.pinduoduo_spider import PinduoduoSpider
from analyzers.data_analyzer import DataAnalyzer
from visualizers.chart_generator import ChartGenerator
from utils.logging import get_logger

logger = get_logger('main')

def crawl_all_platforms(keyword, max_pages=1):
    all_items = []
    
    platforms = [
        ('京东', JDSPider()),
        ('淘宝', TaobaoSpider()),
        ('拼多多', PinduoduoSpider())
    ]
    
    for platform_name, spider in platforms:
        logger.info(f'开始抓取 {platform_name} 数据...')
        try:
            items = spider.search(keyword, max_pages=max_pages)
            logger.info(f'{platform_name} 抓取完成，共 {len(items)} 条数据')
            all_items.extend(items)
        except Exception as e:
            logger.error(f'{platform_name} 抓取失败: {e}')
        time.sleep(2)
    
    return all_items

def main():
    parser = argparse.ArgumentParser(description='电商商品价格自动化采集与对比工具')
    parser.add_argument('keyword', type=str, help='搜索关键词')
    parser.add_argument('--pages', type=int, default=1, help='每个平台抓取的页数')
    parser.add_argument('--output', action='store_true', help='是否输出到Excel文件')
    parser.add_argument('--charts', action='store_true', help='是否生成图表')
    
    args = parser.parse_args()
    
    logger.info(f'开始采集关键词 "{args.keyword}" 的商品数据...')
    
    raw_items = crawl_all_platforms(args.keyword, max_pages=args.pages)
    
    if not raw_items:
        logger.warning('未采集到任何数据')
        return
    
    analyzer = DataAnalyzer()
    
    cleaned_items = analyzer.clean_and_deduplicate(raw_items)
    logger.info(f'数据清洗完成，去重后剩余 {len(cleaned_items)} 条数据')
    
    cleaned_items = analyzer.add_value_score(cleaned_items)
    
    sorted_items = analyzer.sort_by_price(cleaned_items)
    
    stats = analyzer.analyze_prices(sorted_items)
    logger.info(f'价格分析完成: 共 {stats["total_items"]} 件商品, 均价 ¥{stats["avg_price"]}, 最低价 ¥{stats["min_price"]}, 最高价 ¥{stats["max_price"]}')
    
    if args.output:
        excel_path = analyzer.save_to_excel(sorted_items, args.keyword)
        if excel_path:
            logger.info(f'数据已保存到: {excel_path}')
    
    if args.charts:
        chart_gen = ChartGenerator()
        chart_gen.generate_price_chart(sorted_items, args.keyword)
        chart_gen.generate_platform_distribution(sorted_items, args.keyword)
        chart_gen.generate_value_score_chart(sorted_items, args.keyword)
        chart_gen.generate_price_sales_scatter(sorted_items, args.keyword)
        logger.info('图表生成完成')
    
    print('\n=== 商品价格对比结果 (按价格从低到高排序) ===')
    for i, item in enumerate(sorted_items[:10], 1):
        print(f'{i}. [{item["platform"]}] {item["name"]}')
        print(f'    价格: ¥{item["price"]:.2f}')
        print(f'    销量: {item["sales"]}')
        print(f'    评分: {item["rating"]}')
        print(f'    性价比: {item["value_score"]:.2f}')
        print(f'    链接: {item["url"]}')
        print()
    
    print('=== 高性价比推荐 ===')
    value_items = sorted(sorted_items, key=lambda x: x['value_score'], reverse=True)[:5]
    for i, item in enumerate(value_items, 1):
        print(f'{i}. [{item["platform"]}] {item["name"]}')
        print(f'    价格: ¥{item["price"]:.2f} | 销量: {item["sales"]} | 评分: {item["rating"]} | 性价比: {item["value_score"]:.2f}')
        print()

if __name__ == '__main__':
    main()