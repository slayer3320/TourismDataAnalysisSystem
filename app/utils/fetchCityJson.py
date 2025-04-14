import os
import csv
import subprocess
import logging
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CITY_CSV_PATH = os.path.join(os.path.dirname(__file__), 'city.csv')
CACHE_EXPIRE_HOURS = 1

def fetch_cities_from_mysql():
    """
    从MySQL数据库获取城市数据并保存到CSV
    """
    # MySQL连接配置
    host = '47.109.193.153'
    port = '8673'
    user = 'root'
    password = 'tqkzT4olfaRImhlwgDiQZSiqwVNQDfZSOuyKwsGOvQc'
    database = 'data'

    try:
        # 执行MySQL查询命令，包含ID字段
        cmd = f'mysql -h {host} -P {port} -u {user} -p{password} {database} --ssl-mode=DISABLED -e "SELECT id, city_name, province FROM city ORDER BY province, city_name"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        
        # 处理查询结果
        lines = result.stdout.strip().split('\n')
        city_data = {}
        
        if len(lines) < 2:  # 至少表头+1行数据
            logger.warning("MySQL查询返回空结果")
            return {}

        # 解析数据
        for line in lines[1:]:
            if line.strip():
                parts = [p.strip() for p in line.split('\t')]
                if len(parts) >= 2:
                    city_data[parts[0]] = parts[1]

        # 保存到CSV，包含ID字段
        with open(CITY_CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'city_name', 'province', 'last_updated'])
            for line in lines[1:]:
                if line.strip():
                    parts = [p.strip() for p in line.split('\t')]
                    if len(parts) >= 3:  # id, city_name, province
                        writer.writerow([parts[0], parts[1], parts[2], datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

        logger.info(f"城市数据已保存到 {CITY_CSV_PATH}")
        return city_data

    except subprocess.CalledProcessError as e:
        logger.error(f"MySQL查询失败: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"处理数据失败: {str(e)}")
        raise

def get_city_data(with_id=False, json_format=False):
    """从CSV文件获取城市数据，如果过期则从MySQL更新
    :param with_id: 是否返回包含ID的完整数据
    :param json_format: 是否返回与city.json相同的格式
    :return: 根据参数返回不同格式的数据
    """
    # 检查文件是否存在
    if not os.path.exists(CITY_CSV_PATH):
        return fetch_cities_from_mysql()

    # 检查缓存是否过期
    last_modified = datetime.fromtimestamp(os.path.getmtime(CITY_CSV_PATH))
    if datetime.now() - last_modified > timedelta(hours=CACHE_EXPIRE_HOURS):
        logger.info("城市数据缓存已过期，重新从MySQL获取")
        return fetch_cities_from_mysql()

    # 从CSV读取数据，根据参数返回不同格式
    city_data = {}
    try:
        with open(CITY_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if json_format:
                    # 返回与city.json相同的格式
                    city_data[row['city_name']] = row['province']
                elif with_id:
                    # 返回包含ID的完整数据
                    city_data[row['city_name']] = {
                        'id': row['id'],
                        'province': row['province']
                    }
                else:
                    # 默认返回城市到省份的映射
                    city_data[row['city_name']] = row['province']
        
        # 如果需要生成json文件
        if json_format:
            import json
            json_path = os.path.join(os.path.dirname(__file__), 'city.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(city_data, f, ensure_ascii=False, indent=2)
        
        return city_data
    except Exception as e:
        logger.error(f"读取CSV文件失败: {str(e)}")
        return fetch_cities_from_mysql()

if __name__ == '__main__':
    get_city_data()
