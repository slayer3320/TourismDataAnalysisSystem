import subprocess
import logging
from typing import Dict, List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScenicSpotFetcher:
    def __init__(self):
        # MySQL连接配置
        self.host = '47.109.193.153'
        self.port = '8673'
        self.user = 'root'
        self.password = 'tqkzT4olfaRImhlwgDiQZSiqwVNQDfZSOuyKwsGOvQc'
        self.database = 'data'
        self.table = 'scenic_spots'

    def fetch_spots(self, page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        从MySQL分页获取景点数据
        :param page: 页码
        :param page_size: 每页数量
        :return: 景点数据列表
        """
        offset = (page - 1) * page_size
        query = f"""
            SELECT id, name, province, city, description, rating, price 
            FROM {self.table}
            LIMIT {page_size} OFFSET {offset}
        """
        
        try:
            cmd = (
                f'mysql -h {self.host} -P {self.port} -u {self.user} '
                f'-p{self.password} {self.database} --ssl-mode=DISABLED '
                f'-e "{query}"'
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return self._parse_mysql_result(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"MySQL查询失败: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"处理数据失败: {str(e)}")
            raise

    def fetch_by_city(self, city_name: str) -> List[Dict]:
        """
        根据城市名获取景点数据
        :param city_name: 城市名称
        :return: 景点数据列表
        """
        query = f"""
            SELECT id, name, province, city, description, rating, price 
            FROM {self.table}
            WHERE city = '{city_name}'
            LIMIT 50
        """
        
        try:
            cmd = (
                f'mysql -h {self.host} -P {self.port} -u {self.user} '
                f'-p{self.password} {self.database} --ssl-mode=DISABLED '
                f'-e "{query}"'
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return self._parse_mysql_result(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"MySQL查询失败: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"处理数据失败: {str(e)}")
            raise

    def get_grade_distribution(self, city_name: str = None) -> Dict[str, int]:
        """
        获取景点星级分布数据
        :param city_name: 城市名称(可选)
        :return: 各星级数量统计字典
        """
        where_clause = f"WHERE city = '{city_name}'" if city_name else ""
        query = f"""
            SELECT IFNULL(grade, '无评级') as grade, COUNT(*) as count 
            FROM {self.table}
            {where_clause}
            GROUP BY grade
            ORDER BY grade
        """
        try:
            cmd = (
                f'mysql -h {self.host} -P {self.port} -u {self.user} '
                f'-p{self.password} {self.database} --ssl-mode=DISABLED '
                f'-e "{query}"'
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) < 2:
                return {}
            
            distribution = {}
            for line in lines[1:]:
                if line.strip():
                    grade, count = line.split('\t')
                    distribution[grade] = int(count)
            return distribution
        except subprocess.CalledProcessError as e:
            logger.error(f"获取表结构失败: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"处理数据失败: {str(e)}")
            raise

    def _parse_mysql_result(self, result: str) -> List[Dict]:
        """解析MySQL查询结果"""
        lines = result.strip().split('\n')
        if len(lines) < 2:
            return []

        headers = [h.strip() for h in lines[0].split('\t')]
        spots = []
        
        for line in lines[1:]:
            if line.strip():
                values = [v.strip() for v in line.split('\t')]
                spot = dict(zip(headers, values))
                spots.append(spot)
        
        return spots

# 使用示例
if __name__ == '__main__':
    fetcher = ScenicSpotFetcher()
    # 获取第一页数据
    print(fetcher.fetch_spots(page=1, page_size=10))
    # 获取北京景点
    print(fetcher.fetch_by_city('北京'))
