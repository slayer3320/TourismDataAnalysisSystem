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


def get_city_reviews(city_name):
    """获取城市所有景点的评论
    Args:
        city_name: 城市名称
    Returns:
        列表，每个元素包含景点信息和评论
    """
    connection = connect_to_database()
    if not connection:
        return []  # 如果连接失败，直接返回空列表
    
    cursor = connection.cursor(dictionary=True)  # 使用字典游标方便获取列名
    
    try:
        # 1. 先从city表获取city_id
        cursor.execute("SELECT id FROM city WHERE city_name = %s", (city_name,))
        city_result = cursor.fetchone()
        
        if not city_result:
            return []  # 如果城市不存在，返回空列表
        
        city_id = city_result['id']
        
        # 2. 查询该城市所有景点的评论
        query = """
            SELECT 
                s.id as spot_id, 
                s.name as spot_name,
                r.review_id,
                r.content
            FROM scenic_spots s
            JOIN reviews r ON s.id = r.scenic_id
            WHERE s.city_id = %s
            ORDER BY s.id, r.time DESC
        """
        cursor.execute(query, (city_id,))
        result = cursor.fetchall()
        
        # 按景点分组评论
        reviews_by_spot = {}
        for row in result:
            spot_id = row['spot_id']
            if spot_id not in reviews_by_spot:
                reviews_by_spot[spot_id] = {
                    'spot_id': spot_id,
                    'spot_name': row['spot_name'],
                    'reviews': []
                }
            reviews_by_spot[spot_id]['reviews'].append({
                'review_id': row['review_id'],
                'content': row['content'],
            })
        
        return list(reviews_by_spot.values())
    
    finally:
        # 确保无论如何都会关闭连接
        cursor.close()
        connection.close()

def get_scenic_spots_list_by_id(spot_id):
    connection = connect_to_database()
    if not connection:
        return []  # 如果连接失败，直接返回空列表
    
    cursor = connection.cursor()
    
    try:
        # 查询指定ID的景点信息
        query = """
            SELECT s.id, s.name, s.grade, s.score, s.ticket_price,
                   i.url as image_url, s.address, s.type, s.intro, s.heat, s.comments
            FROM scenic_spots s
            LEFT JOIN scenic_images i ON s.id = i.id
            WHERE s.id = %s
        """
        cursor.execute(query, (spot_id,))
        result = cursor.fetchone()
        
        return result if result else []
    
    finally:
        # 确保无论如何都会关闭连接
        cursor.close()
        connection.close()

def check_scenic_images():
    """临时函数：检查scenic_images表数据"""
    connection = connect_to_database()
    if not connection:
        return "数据库连接失败"
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM scenic_images LIMIT 5")
        result = cursor.fetchall()
        return result
    
    finally:
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
        
        # 2. 查询景点列表及图片URL
        # id,city_id,name,grade,address,type,intro,ticket_price,score,heat,comments,url
        query = """
            SELECT s.id, s.name, s.grade, s.score, s.ticket_price,
                   i.url as image_url, cs.url as detail_url,
                   s.address, s.type, s.intro, s.heat, s.comments
            FROM scenic_spots s
            LEFT JOIN scenic_images i ON s.id = i.id
            LEFT JOIN city_scenic cs ON s.id = cs.scenic_id
            WHERE s.city_id = %s
        """
        cursor.execute(query, (city_id,))
        result = cursor.fetchall()
        
        return result
    
    finally:
        # 确保无论如何都会关闭连接
        cursor.close()
        connection.close()
