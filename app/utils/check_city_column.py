import mysql.connector
from mysql.connector import Error

def check_column_exists():
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
            cursor.execute("SHOW COLUMNS FROM scenic_spots LIKE 'city';")
            result = cursor.fetchone()
            if result:
                print("city列存在")
            else:
                print("city列不存在")
    except Error as e:
        print(f"连接数据库时发生错误: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

check_column_exists()
