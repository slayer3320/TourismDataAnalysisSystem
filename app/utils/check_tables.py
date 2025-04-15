import mysql.connector

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'tqkzT4olfaRImhlwgDiQZSiqwVNQDfZSOuyKwsGOvQc',
    'host': '47.109.193.153',
    'port': '8673',
    'database': 'data'
}

def connect_to_database():
    connection = None
    try:
        # 连接到数据库
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        return None


def get_star_ratio(city_name):
    connection = connect_to_database()
    if not connection:
        return []  # 如果连接失败，直接返回空列表
    
    cursor = connection.cursor()
    
    try:
        # 1. 先从city表获取city_id
        cursor.execute("SELECT id FROM city WHERE city_name = %s", (city_name,))
        city_result = cursor.fetchone()
        
        if not city_result:
            return []  # 如果城市不存在，返回空列表
        
        city_id = city_result[0]
        
        # 2. 查询景点星级分布
        query = """
            SELECT grade, COUNT(*) as count 
            FROM scenic_spots 
            WHERE city_id = %s 
            GROUP BY grade
        """
        cursor.execute(query, (city_id,))  # 关键修复：这里必须传递参数
        result = cursor.fetchall()
        
        return result
    
    finally:
        # 确保无论如何都会关闭连接
        cursor.close()
        connection.close()
    

def get_price_analysis(city_name):
    connection = connect_to_database()
    if not connection:
        return []  # 如果连接失败，直接返回空列表
    
    cursor = connection.cursor()
    
    try:
        # 1. 先从city表获取city_id
        cursor.execute("SELECT id FROM city WHERE city_name = %s", (city_name,))
        city_result = cursor.fetchone()
        
        if not city_result:
            return []  # 如果城市不存在，返回空列表
        
        city_id = city_result[0]
        
        # 2. 查询景点价格分布
        query = """
            SELECT ticket_price, COUNT(*) as count 
            FROM scenic_spots 
            WHERE city_id = %s 
            GROUP BY ticket_price
        """
        cursor.execute(query, (city_id,))  # 注意这里传递参数 (city_id,)
        result = cursor.fetchall()
        
        return result
    
    finally:
        # 确保无论如何都会关闭连接
        cursor.close()
        connection.close()
        
# 获取景点列表
def get_scenic_spots_list(city_name):
    connection = connect_to_database()
    if not connection:
        return []  # 如果连接失败，直接返回空列表
    
    cursor = connection.cursor()
    
    try:
        # 1. 先从city表获取city_id
        cursor.execute("SELECT id FROM city WHERE city_name = %s", (city_name,))
        city_result = cursor.fetchone()
        
        if not city_result:
            return []  # 如果城市不存在，返回空列表
        
        city_id = city_result[0]
        
        # 2. 查询景点列表
        query = """
            SELECT id, name, grade, score, ticket_price, comments, url 
            FROM scenic_spots 
            WHERE city_id = %s
        """
        cursor.execute(query, (city_id,))
        result = cursor.fetchall()
        
        return result
    
    finally:
        # 确保无论如何都会关闭连接
        cursor.close()
        connection.close()
