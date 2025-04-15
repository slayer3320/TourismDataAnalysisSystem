import mysql.connector
from mysql.connector import Error

def check_table_exists():
    config = {
        'host': '47.109.193.153',
        'port': 8673,
        'user': 'root',
        'password': 'tqkzT4olfaRImhlwgDiQZSiqwVNQDfZSOuyKwsGOvQc',
        'database': 'data'
    }
    
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES LIKE 'scenic_spots';")
            result = cursor.fetchone()
            if result:
                print("scenic_spots表存在")
            else:
                print("scenic_spots表不存在")
    except Error as e:
        print(f"连接数据库时发生错误: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

check_table_exists()
