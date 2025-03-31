from database_connection import execute_query

# Câu truy vấn SQL
query_create_table = """
CREATE TABLE IF NOT EXISTS ds_nganh (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ky_nang VARCHAR(255) NOT NULL,
    nganh VARCHAR(255) NOT NULL,
    truong VARCHAR(255) NOT NULL,
    mo_ta TEXT NOT NULL
);
"""

query_insert_data = """
INSERT INTO ds_nganh (ky_nang, nganh, truong, mo_ta) VALUES (%s, %s, %s, %s)
"""

data = [
    ('vẽ', 'Kiến trúc', 'ĐH Kiến trúc TP.HCM', 'Phù hợp với người giỏi vẽ, sáng tạo, và đam mê thiết kế không gian.'),
    ('toán', 'Kỹ thuật cơ khí', 'ĐH Bách Khoa TP.HCM', 'Dành cho người giỏi toán, tư duy logic, và thích chế tạo máy móc.'),
    ('logic', 'Công nghệ thông tin', 'ĐH Bách Khoa TP.HCM', 'Phù hợp với tư duy lập trình, giải quyết vấn đề kỹ thuật.'),
    ('sáng tạo', 'Thiết kế đồ họa', 'ĐH Mỹ thuật TP.HCM', 'Cho người đam mê sáng tạo, thiết kế hình ảnh và giao diện.')
]

# Tạo bảng
execute_query(query_create_table)

# Chèn dữ liệu
for item in data:
    execute_query(query_insert_data, item)
from flask import Flask # type: ignore

app = Flask(__name__)

@app.route("/")
def home():
    return "Chatbot đang hoạt động!"

if __name__ == "__main__":
    app.run()
