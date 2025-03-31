import mysql.connector
from mysql.connector import Error

# Hàm kết nối tới cơ sở dữ liệu
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',              # Thay bằng host của bạn (vd: localhost, hoặc IP của hosting)
            user='root',          # Tên đăng nhập MySQL (vd: root)
            password='',      # Mật khẩu MySQL
            database='chatbot_db'          # Tên cơ sở dữ liệu bạn tạo trong phpMyAdmin
        )
        if connection.is_connected():
            print("Kết nối thành công tới cơ sở dữ liệu MySQL!")
            return connection
    except Error as e:
        print(f"Lỗi khi kết nối: {e}")
        return None

# Hàm thực thi truy vấn SQL
def execute_query(query, values=None):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            connection.commit()
            print("Thực thi truy vấn thành công!")
            return cursor.fetchall()
        except Error as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")
        finally:
            cursor.close()
            connection.close()
