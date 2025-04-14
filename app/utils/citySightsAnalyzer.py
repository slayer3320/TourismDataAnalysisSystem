import csv
import logging
from typing import Dict, List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CitySightsAnalyzer:
    def __init__(self):
        self.file_path = 'app/utils/city_sights_counts_5A_4A.csv'
        self.data = self._load_data()

    def _load_data(self) -> List[Dict]:
        """加载CSV文件数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            logger.error(f"加载CSV文件失败: {str(e)}")
            return []

    def get_all_data(self) -> List[Dict]:
        """获取全部城市景点数据"""
        return self.data

    def get_city_data(self, city_name: str) -> Dict:
        """获取指定城市数据"""
        for city in self.data:
            if city['city'] == city_name:
                return {
                    'city': city['city'],
                    'count': int(city['sights_count_5A_4A'])
                }
        return {}

    def get_top_cities(self, n: int = 10) -> List[Dict]:
        """获取景点数量最多的前N个城市"""
        sorted_data = sorted(
            self.data,
            key=lambda x: int(x['sights_count_5A_4A']),
            reverse=True
        )
        return [
            {
                'city': city['city'],
                'count': int(city['sights_count_5A_4A'])
            }
            for city in sorted_data[:n]
        ]

# 使用示例
if __name__ == '__main__':
    analyzer = CitySightsAnalyzer()
    # 获取全部数据
    print(analyzer.get_all_data())
    # 获取北京数据
    print(analyzer.get_city_data('北京'))
    # 获取前10名城市
    print(analyzer.get_top_cities(10))
