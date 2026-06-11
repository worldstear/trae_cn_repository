from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
import time
import os

app = Flask(__name__)
CORS(app)

current_results = {}
is_running = False

def run_crawler(keyword, max_pages=1):
    global current_results, is_running
    is_running = True
    
    try:
        from spiders.jd_spider import JDSPider
        from spiders.taobao_spider import TaobaoSpider
        from spiders.pinduoduo_spider import PinduoduoSpider
        from analyzers.data_analyzer import DataAnalyzer
        
        all_items = []
        
        platforms = [
            ('京东', JDSPider()),
            ('淘宝', TaobaoSpider()),
            ('拼多多', PinduoduoSpider())
        ]
        
        for platform_name, spider in platforms:
            try:
                items = spider.search(keyword, max_pages=max_pages)
                all_items.extend(items)
            except Exception as e:
                print(f'{platform_name} 抓取失败: {e}')
            time.sleep(2)
        
        analyzer = DataAnalyzer()
        cleaned_items = analyzer.clean_and_deduplicate(all_items)
        cleaned_items = analyzer.add_value_score(cleaned_items)
        sorted_items = analyzer.sort_by_price(cleaned_items)
        stats = analyzer.analyze_prices(sorted_items)
        
        value_items = sorted(sorted_items, key=lambda x: x['value_score'], reverse=True)[:5]
        
        current_results[keyword] = {
            'items': sorted_items[:20],
            'stats': stats,
            'recommendations': value_items,
            'total_count': len(sorted_items),
            'timestamp': time.time()
        }
        
    except Exception as e:
        current_results[keyword] = {
            'error': str(e),
            'timestamp': time.time()
        }
    
    is_running = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    global is_running
    
    if is_running:
        return jsonify({'status': 'running', 'message': '正在抓取数据，请稍候...'})
    
    data = request.get_json()
    keyword = data.get('keyword', '')
    
    if not keyword:
        return jsonify({'status': 'error', 'message': '请输入搜索关键词'})
    
    if keyword in current_results and time.time() - current_results[keyword].get('timestamp', 0) < 300:
        return jsonify({
            'status': 'success',
            'data': current_results[keyword]
        })
    
    thread = threading.Thread(target=run_crawler, args=(keyword,))
    thread.start()
    
    return jsonify({'status': 'started', 'message': '开始抓取数据，请等待结果...'})

@app.route('/api/status')
def api_status():
    return jsonify({'is_running': is_running})

@app.route('/api/sample')
def api_sample():
    sample_data = {
        'items': [
            {'platform': '京东', 'name': 'Apple iPhone 15 Pro 256GB 原色钛金属', 'price': 7999.0, 'sales': 12580, 'rating': 4.9, 'url': 'https://item.jd.com/100123456789.html', 'value_score': 85.5},
            {'platform': '淘宝', 'name': 'Apple iPhone 15 Pro 256GB 国行正品', 'price': 7899.0, 'sales': 8920, 'rating': 4.8, 'url': 'https://item.taobao.com/item.htm?id=1234567890', 'value_score': 82.3},
            {'platform': '拼多多', 'name': 'Apple iPhone 15 Pro 256GB 全网通', 'price': 7599.0, 'sales': 25600, 'rating': 4.7, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123456', 'value_score': 88.7},
            {'platform': '京东', 'name': 'Apple iPhone 15 Pro 128GB 原色钛金属', 'price': 6999.0, 'sales': 18900, 'rating': 4.9, 'url': 'https://item.jd.com/100123456790.html', 'value_score': 86.2},
            {'platform': '淘宝', 'name': 'Apple iPhone 15 Pro 128GB 全新未拆封', 'price': 6899.0, 'sales': 12300, 'rating': 4.8, 'url': 'https://item.taobao.com/item.htm?id=1234567891', 'value_score': 84.1},
            {'platform': '拼多多', 'name': 'Apple iPhone 15 Pro 128GB 官方正品', 'price': 6599.0, 'sales': 35200, 'rating': 4.6, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123457', 'value_score': 90.5},
            {'platform': '京东', 'name': 'Apple iPhone 15 256GB 黑色', 'price': 6499.0, 'sales': 22100, 'rating': 4.8, 'url': 'https://item.jd.com/100123456791.html', 'value_score': 87.3},
            {'platform': '淘宝', 'name': 'Apple iPhone 15 256GB 双卡双待', 'price': 6399.0, 'sales': 15600, 'rating': 4.7, 'url': 'https://item.taobao.com/item.htm?id=1234567892', 'value_score': 85.2},
            {'platform': '拼多多', 'name': 'Apple iPhone 15 256GB 国行版', 'price': 6199.0, 'sales': 42800, 'rating': 4.5, 'url': 'https://mobile.pinduoduo.com/goods.html?goods_id=123458', 'value_score': 91.2},
            {'platform': '京东', 'name': 'Apple iPhone 15 128GB 蓝色', 'price': 5999.0, 'sales': 28900, 'rating': 4.8, 'url': 'https://item.jd.com/100123456792.html', 'value_score': 88.1}
        ],
        'stats': {
            'total_items': 10,
            'avg_price': 6918.1,
            'min_price': 5999.0,
            'max_price': 7999.0,
            'median_price': 6699.0,
            'price_range': 2000.0
        },
        'recommendations': [
            {'platform': '拼多多', 'name': 'Apple iPhone 15 256GB 国行版', 'price': 6199.0, 'sales': 42800, 'rating': 4.5, 'value_score': 91.2},
            {'platform': '拼多多', 'name': 'Apple iPhone 15 Pro 128GB 官方正品', 'price': 6599.0, 'sales': 35200, 'rating': 4.6, 'value_score': 90.5},
            {'platform': '京东', 'name': 'Apple iPhone 15 Pro 128GB 原色钛金属', 'price': 6999.0, 'sales': 18900, 'rating': 4.9, 'value_score': 86.2}
        ],
        'total_count': 10
    }
    return jsonify({'status': 'success', 'data': sample_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)