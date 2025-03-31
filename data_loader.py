# data_loader.py
import pandas as pd

def load_data():
    try:
        df = pd.read_csv("data_train.csv")
        danh_sach_nganh = {}
        for _, row in df.iterrows():
            ky_nang = row["ky_nang"]
            danh_sach_nganh[ky_nang] = {
                "ngành": row["nganh"],
                "trường": row["truong"],
                "mô_ta": row["mo_ta"]
            }
        return danh_sach_nganh
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return {}