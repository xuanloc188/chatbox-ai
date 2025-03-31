# chatbot.py
import tkinter as tk
from tkinter import scrolledtext
from data_loader import load_data
from chatbot_logic import tu_van_nganh, lay_thong_tin_truong

# Đọc dữ liệu từ CSV
danh_sach_nganh = load_data()



def xu_ly_cau_hoi(cau_hoi, chat_area):
    chat_area.tag_configure("user", foreground="green")
    chat_area.insert(tk.END, f"🧑 You: {cau_hoi}\n", "user")

    nganh, truong, mo_ta = tu_van_nganh(cau_hoi, danh_sach_nganh)
    thong_tin_truong = lay_thong_tin_truong(truong)

    chat_area.tag_configure("bot", foreground="black")
    chat_area.insert(tk.END, f"🤖 AI: Ngành '{nganh}' tại {truong}. {mo_ta}\n{thong_tin_truong}\n", "bot")

def giao_dien_chatbot():
    window = tk.Tk()
    window.title("Chatbot Hỗ Trợ Ngành Học")
    window.geometry("600x700")
    window.configure(bg="#2E2E2E")

    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=0)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=0)

    chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12), bg="#FFFFFF", fg="black", bd=1, relief="solid")
    chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    chat_area.insert(tk.END, "🤖 AI: Chào bạn! Tớ có thể giúp gì cho bạn hôm nay?\n")
    chat_area.config(state="disabled")

    input_field = tk.Entry(window, width=50, font=("Arial", 12), bg="#FFFFFF", fg="black", bd=1, relief="solid")
    input_field.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def gui_cau_hoi():
        cau_hoi = input_field.get().strip().lower()
        if cau_hoi:
            chat_area.config(state="normal")
            xu_ly_cau_hoi(cau_hoi, chat_area)
            chat_area.see(tk.END)
            chat_area.config(state="disabled")
            input_field.delete(0, tk.END)

    send_button = tk.Button(window, text="Gửi", command=gui_cau_hoi, font=("Arial", 12), bg="#4CAF50", fg="white", bd=1, relief="solid")
    send_button.grid(row=1, column=1, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    giao_dien_chatbot()