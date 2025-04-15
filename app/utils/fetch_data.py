import mysql.connector

# 数据库连接配置
config = {
    'host': '47.109.193.153',
    'port': 8673,
    'user': 'root',
    'password': 'tqkzT4olfaRImhlwgDiQZSiqwVNQDfZSOuyKwsGOvQc',
    'database': 'data'
}

# 连接到数据库
connection = mysql.connector.connect(**config)

# 创建游标
cursor = connection.cursor()

def fetch_scenic_spots_by_city(city_name):
    # 连接到数据库
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # 首先查询city表获取city_id
    cursor.execute("SELECT id FROM city WHERE city_name = %s", (city_name,))
    city_result = cursor.fetchone()
    
    if not city_result:
        # 如果没有找到对应的城市，返回空结果
        cursor.close()
        connection.close()
        return []
    
    city_id = city_result[0]
    
    # 然后查询scenic_spots表
    cursor.execute("SELECT * FROM scenic_spots WHERE city_id = %s", (city_id,))
    results = cursor.fetchall()
    
    # 关闭游标和连接
    cursor.close()
    connection.close()
    
    return results

# 示例调用
# scenic_spots = fetch_scenic_spots_by_city('当前城市名称')

# 关闭游标和连接
cursor.close()
connection.close()

# 示例调用
# scenic_spots = fetch_scenic_spots_by_city('当前城市名称')
