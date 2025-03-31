# train_tfidf.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from nltk.tokenize import word_tokenize
import nltk

# Tải tài nguyên punkt_tab (chỉ cần chạy một lần)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    if isinstance(text, str):  # Kiểm tra xem text có phải là chuỗi không
        text = text.lower()
        tokens = word_tokenize(text)
        return ' '.join(tokens)
    return ''  # Trả về chuỗi rỗng nếu text không phải là chuỗi

# Hàm huấn luyện và lưu mô hình TF-IDF
def train_and_save_tfidf():
    # Đọc dữ liệu từ file CSV
    try:
        data = pd.read_csv("C:/ChatBotTuVanNganhHoc/data_train.csv")
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return

    # Tiền xử lý cột 'mo_ta'
    data['mo_ta'] = data['mo_ta'].apply(preprocess_text)

    # Lấy danh sách các mô tả và kỹ năng
    mo_tas = data['mo_ta'].tolist()
    ky_nangs = data['ky_nang'].tolist()

    # Khởi tạo và huấn luyện TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(mo_tas)
    except ValueError as e:
        print(f"Lỗi khi huấn luyện TF-IDF: {e}")
        return

    # Lưu mô hình và dữ liệu
    joblib.dump(vectorizer, "tfidf_vectorizer.joblib")
    joblib.dump(tfidf_matrix, "tfidf_matrix.joblib")
    joblib.dump(ky_nangs, "ky_nangs.joblib")

    print("Đã lưu mô hình TF-IDF thành công!")

# Gọi hàm để huấn luyện và lưu
if __name__ == "__main__":
    train_and_save_tfidf()