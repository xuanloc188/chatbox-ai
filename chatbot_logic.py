# chatbot_logic.py
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
from nltk.tokenize import word_tokenize
import nltk
import requests
import random
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Tải tài nguyên punkt_tab (chỉ cần chạy một lần)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# API Keys (Thay bằng API key thật của bạn)
GOOGLE_API_KEY = "AIzaSyCwN16UhmZsKYazVd2CQrjDE3kj6XrAJbY"
GOOGLE_CSE_ID = "519d867d7db1f49df"
OPENWEATHER_API_KEY = "2a39ac296197c2f8ad13922c8bf17686"
NEWSAPI_KEY = "e9dffaa1921e4f43ac0a738a5fcc76b9"

# Load mô hình BlenderBot
model_name = "facebook/blenderbot-3B"
try:
    tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
except Exception as e:
    print(f"Lỗi khi tải mô hình BlenderBot: {e}")
    tokenizer = None
    model = None

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return ' '.join(tokens)

# Hàm lấy tóm tắt từ Wikipedia
def get_wikipedia_summary(topic):
    headers = {
        "User-Agent": "MyChatBot (your_email@example.com)"
    }
    topic = topic.replace(" ", "_")
    url = f"https://vi.wikipedia.org/api/rest_v1/page/summary/{topic}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if "extract" in data:
            return data["extract"]
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Hàm lấy thông tin thời tiết từ OpenWeatherMap
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=vi"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("cod") == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"Hôm nay ở {city} trời {weather}, nhiệt độ khoảng {temp}°C. Hy vọng bạn có một ngày tuyệt vời nhé!"
        else:
            return f"Xin lỗi, mình không tìm được thông tin ở {city}. Bạn thử với địa điểm khác được không?"
    except requests.exceptions.RequestException:
        return "Mình gặp chút trục trặc khi lấy thông tin, bạn thử lại sau nhé!"

# Tích hợp phản hồi tự nhiên vào hàm xử lý câu hỏi
def tu_van_nganh(cau_hoi, danh_sach_nganh):
    cau_hoi_processed = preprocess_text(cau_hoi)

    # Kiểm tra câu hỏi liên quan đến thời tiết
    if "hôm nay" in cau_hoi_processed:
        words = cau_hoi_processed.split()
        city = None
        for word in words:
            if word not in ["hôm", "nay", "ở", "tại"]:
                city = word
                break
        if city:
            weather_info = get_weather(city)
            return "", "", weather_info
        else:
            return "", "", "Bạn muốn biết thời tiết ở đâu, hãy cho mình biết nhé!"

    # Hàm tùy chỉnh phản hồi
def custom_response(source, content):
    if source == "Wikipedia":
        return f"Dưới đây là thông tin mình tìm được từ Wikipedia: {content}"
    elif source == "NewsAPI":
        return f"Dưới đây là một số tin tức mới nhất mình tìm được: {content}"
    elif source == "OpenWeather":
        return f"Dưới đây là thông tin thời tiết hiện tại: {content}"
    elif source == "Google CSE":
        return f"Dưới đây là kết quả tìm kiếm từ Google: {content}"
    else:
        return "Mình không tìm thấy thông tin phù hợp, bạn thử lại nhé!"

# Tích hợp vào hàm xử lý câu hỏi
def tu_van_nganh(cau_hoi, danh_sach_nganh):
    cau_hoi_processed = preprocess_text(cau_hoi)

    # Kiểm tra câu hỏi liên quan đến Wikipedia
    if "wiki" in cau_hoi_processed:
        wiki_summary = get_wikipedia_summary(cau_hoi)
        if wiki_summary:
            return "", "", custom_response("Wikipedia", wiki_summary)
        else:
            return "", "", "Mình không tìm thấy thông tin từ Wikipedia, bạn thử hỏi lại nhé!"

    # Kiểm tra câu hỏi liên quan đến tin tức
    if "tin tức" in cau_hoi_processed:
        news_info = get_news(cau_hoi)
        if news_info:
            return "", "", custom_response("NewsAPI", news_info)
        else:
            return "", "", "Mình không tìm thấy tin tức liên quan, bạn thử cung cấp từ khóa khác nhé!"

    # Kiểm tra câu hỏi liên quan đến thời tiết
    if "hôm nay" in cau_hoi_processed:
        words = cau_hoi_processed.split()
        city = None
        for word in words:
            if word not in ["hôm", "nay", "ở", "tại"]:
                city = word
                break
        if city:
            weather_info = get_weather(city)
            return "", "", custom_response("OpenWeather", weather_info)
        else:
            return "", "", "Bạn muốn biết thời tiết ở đâu, hãy cho mình biết nhé!"

    # Kiểm tra câu hỏi liên quan đến Google CSE
    if "google" in cau_hoi_processed:
        google_result = search_google(cau_hoi)
        if google_result:
            return "", "", custom_response("Google CSE", google_result)
        else:
            return "", "", "Mình không tìm thấy kết quả từ Google, bạn thử lại nhé!"

# Hàm lấy tin tức từ NewsAPI
def get_news(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWSAPI_KEY}&language=vi&pageSize=3"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok" and data.get("articles"):
            news = "Dưới đây là một số tin tức liên quan:\n"
            for i, article in enumerate(data["articles"], 1):
                title = article["title"]
                url = article["url"]
                news += f"{i}. {title}\n   Link: {url}\n"
            return news
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Hàm tìm kiếm thông tin từ Google Custom Search
def search_google(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    try:
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=3).execute()
        if "items" in res and len(res["items"]) > 0:
            thong_tin = "Dưới đây là thông tin tìm kiếm từ Google:\n"
            for i, item in enumerate(res["items"], 1):
                title = item.get("title", "Không có tiêu đề")
                snippet = item.get("snippet", "Không có mô tả")
                link = item.get("link", "Không có liên kết")
                thong_tin += f"{i}. {title}\n   - Mô tả: {snippet}\n   - Link: {link}\n"
            return thong_tin
        else:
            return None
    except Exception:
        return None

# Hàm trò chuyện với BlenderBot
def chat_with_blenderbot(message):
    if tokenizer is None or model is None:
        return "Mình không thể trò chuyện vì mô hình BlenderBot chưa được tải. Hãy kiểm tra lại!"
    try:
        inputs = tokenizer([message], return_tensors="pt")
        reply_ids = model.generate(**inputs)
        reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        return reply
    except Exception as e:
        return f"Lỗi khi trò chuyện với BlenderBot: {str(e)}"

# Load mô hình TF-IDF đã lưu
try:
    vectorizer = joblib.load("tfidf_vectorizer.joblib")
    tfidf_matrix = joblib.load("tfidf_matrix.joblib")
    ky_nangs = joblib.load("ky_nangs.joblib")
except Exception as e:
    print(f"Lỗi khi load mô hình TF-IDF: {e}. Vui lòng chạy file train_tfidf.py trước!")
    vectorizer = None
    tfidf_matrix = None
    ky_nangs = []

# Danh sách các câu trả lời chào hỏi
greeting_responses = [
    "Chào bạn! Mình là chatbot hỗ trợ ngành học, hôm nay mình có thể giúp gì cho bạn?",
    "Xin chào! Mình ở đây để giúp bạn tìm hiểu về các ngành học hoặc bất kỳ thông tin nào bạn cần. Bạn muốn hỏi gì nào?",
    "Chào bạn! Rất vui được trò chuyện với bạn. Hôm nay bạn muốn tìm hiểu về ngành học hay chỉ muốn trò chuyện thôi? 😊",
    "Hello! Mình là chatbot siêu thân thiện đây, bạn khỏe không? Hôm nay mình có thể giúp gì cho bạn?",
    "Chào bạn! Hôm nay bạn thế nào? Mình sẵn sàng giúp bạn tìm hiểu về ngành học hoặc trò chuyện vui vẻ! 😄"
]

casual_responses = [
    "Ồ, câu hỏi này thú vị đấy! Nhưng mình chưa biết câu trả lời chính xác, bạn có thể nói thêm chi tiết không?",
    "Hmmm, mình không chắc lắm, nhưng mình có thể giúp bạn tìm hiểu thêm nếu bạn muốn!",
    "Câu hỏi này hơi ngoài chuyên môn của mình, nhưng mình nghĩ chúng ta có thể cùng tìm hiểu nhé!",
    "Mình không có thông tin chính xác, nhưng mình có thể kể bạn nghe một câu chuyện vui nếu bạn muốn! 😄",
    "Chà, mình chưa được train để trả lời câu này, nhưng mình có thể tìm kiếm giúp bạn! Bạn muốn mình tìm gì?",
    "Mình là chatbot nên không có ý kiến cá nhân, nhưng nếu mình là con người, mình sẽ rất tò mò về câu hỏi này! Bạn nghĩ sao?",
    "Câu hỏi này làm mình nhớ đến một lần mình tìm hiểu về một chủ đề hoàn toàn khác... À mà thôi, bạn muốn mình tìm thông tin gì thêm không? 😄",
    "Hôm nay bạn thế nào? Mình thì đang rất vui vì được trò chuyện với bạn! 😊",
    "Mình không chắc lắm, nhưng nếu bạn muốn, mình có thể kể cho bạn một vài điều thú vị mà mình biết! Bạn muốn nghe về chủ đề gì?"
]
# Hàm kiểm tra câu chào hỏi
def is_greeting(cau_hoi_processed):
    greetings = ["chào", "xin chào", "hi", "hello", "hallo", "chao", "tổ", "tô"]
    return any(greeting in cau_hoi_processed for greeting in greetings)

# Hàm kiểm tra câu hỏi mang tính trò chuyện
def is_conversational(cau_hoi_processed):
    conversational_phrases = [
        "hôm nay thế nào", "có thể giúp gì", "bạn khỏe không", "tình hình thế nào", 
        "hôm nay ra sao", "bạn đang làm gì", "có gì vui không", "hôm nay bạn thế nào",
        "nghi thức", "tổ", "khang", "bạn có khỏe không", "hôm nay có gì mới"
    ]
    return any(phrase in cau_hoi_processed for phrase in conversational_phrases)

def tu_van_nganh(cau_hoi, danh_sach_nganh):
    cau_hoi_processed = preprocess_text(cau_hoi)

    # Kiểm tra câu chào hỏi
    if is_greeting(cau_hoi_processed):
        return "Chào hỏi", "", random.choice(greeting_responses)

    # Kiểm tra câu hỏi mang tính trò chuyện
    if is_conversational(cau_hoi_processed):
        blender_response = chat_with_blenderbot(cau_hoi)
        return "Trò chuyện", "", f"Mình đang rất ổn, cảm ơn bạn đã hỏi! 😊 {blender_response}"

    # Kiểm tra nếu câu hỏi liên quan đến thời tiết
    if "thời tiết" in cau_hoi_processed:
        words = cau_hoi_processed.split()
        city = None
        for word in words:
            if word not in ["thời", "tiết", "ở", "tại"]:
                city = word
                break
        if city:
            weather_info = get_weather(city)
            if weather_info:
                return "Thông tin thời tiết", "", weather_info
            else:
                return "Không rõ", "", "Không tìm thấy thông tin thời tiết cho thành phố này."
        else:
            return "Không rõ", "", "Vui lòng cung cấp tên thành phố để tra cứu thời tiết."

    # Kiểm tra nếu câu hỏi liên quan đến tin tức
    if "tin tức" in cau_hoi_processed or "mới nhất" in cau_hoi_processed:
        words = cau_hoi_processed.split()
        keyword = None
        for word in words:
            if word not in ["tin", "tức", "mới", "nhất", "về"]:
                keyword = word
                break
        if keyword:
            news_info = get_news(keyword)
            if news_info:
                return "Tin tức", "", news_info
            else:
                return "Không rõ", "", "Không tìm thấy tin tức liên quan."
        else:
            return "Không rõ", "", "Vui lòng cung cấp từ khóa để tìm tin tức."

    # Kiểm tra từ khóa trước (nếu khớp chính xác thì ưu tiên)
    for ky_nang, info in danh_sach_nganh.items():
        if ky_nang in cau_hoi_processed or f"giỏi {ky_nang}" in cau_hoi_processed or f"thích {ky_nang}" in cau_hoi_processed:
            return info["ngành"], info["trường"], info["mô_ta"]

    # Nếu không khớp từ khóa, dùng TF-IDF để tìm ngành phù hợp
    if vectorizer is not None and tfidf_matrix is not None:
        cau_hoi_tfidf = vectorizer.transform([cau_hoi_processed])
        cosine_similarities = cosine_similarity(cau_hoi_tfidf, tfidf_matrix)
        best_match_idx = np.argmax(cosine_similarities)
        best_score = cosine_similarities[0][best_match_idx]

        if best_score > 0.1:
            ky_nang = ky_nangs[best_match_idx]
            info = danh_sach_nganh[ky_nang]
            return info["ngành"], info["trường"], info["mô_ta"]

    # Nếu không tìm thấy trong dữ liệu ngành học, thử tìm trên Wikipedia
    wiki_summary = get_wikipedia_summary(cau_hoi)
    if wiki_summary:
        return "Không rõ", "Chưa xác định", wiki_summary

    # Nếu không tìm thấy trên Wikipedia, thử tìm trên Google
    google_result = search_google(cau_hoi)
    if google_result:
        return "Không rõ", "Chưa xác định", google_result

    # Nếu không tìm thấy gì, dùng BlenderBot để trả lời
    blender_response = chat_with_blenderbot(cau_hoi)
    return "Không rõ", "Chưa xác định", blender_response

def lay_thong_tin_truong(truong):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    query = f"Thông tin về {truong} ngành học Việt Nam"
    try:
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=3).execute()
        if "items" in res and len(res["items"]) > 0:
            thong_tin = "Dưới đây là thông tin chi tiết từ Google:\n"
            for i, item in enumerate(res["items"], 1):
                title = item.get("title", "Không có tiêu đề")
                snippet = item.get("snippet", "Không có mô tả")
                link = item.get("link", "Không có liên kết")
                thong_tin += f"{i}. {title}\n   - Mô tả: {snippet}\n   - Link: {link}\n"
            return thong_tin
        else:
            return f"Không tìm thấy thông tin chi tiết về {truong} trên web."
    except Exception as e:
        return f"Lỗi khi tìm thông tin: {str(e)}. Vui lòng thử lại sau."