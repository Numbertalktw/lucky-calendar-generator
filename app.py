import streamlit as st
import datetime
import pandas as pd
from io import BytesIO
import calendar

# ===== 主日數與幸運物件資料 =====
day_meaning = {
    1: {"名稱": "創造日", "指引": "展現創意，展現自我魅力。", "星": "⭐⭐⭐⭐"},
    2: {"名稱": "連結日", "指引": "適合合作，溝通與等待機會。", "星": "⭐⭐"},
    3: {"名稱": "表達日", "指引": "表達想法，展現自我魅力。", "星": "⭐⭐⭐"},
    4: {"名稱": "實作日", "指引": "建立基礎，適合細節與規劃。", "星": "⭐⭐⭐"},
    5: {"名稱": "行動日", "指引": "啟動新的計畫，做出主動選擇。", "星": "⭐⭐⭐⭐"},
    6: {"名稱": "關係日", "指引": "接觸愛情，適當調整。", "星": "⭐⭐⭐"},
    7: {"名稱": "內省日", "指引": "適合學習、休息與自我對話。", "星": "⭐"},
    8: {"名稱": "成果日", "指引": "聚焦目標與務成就。", "星": "⭐⭐⭐⭐"},
    9: {"名稱": "釋放日", "指引": "放手，療癒與完成階段。", "星": "⭐⭐"},
}

lucky_map = {
    1: {"色": "紅色", "水晶": "紅瑪瑙", "小物": "原子筆"},
    2: {"色": "粉紅色", "水晶": "粉晶", "小物": "情書"},
    3: {"色": "橙色", "水晶": "太陽石", "小物": "麥克風"},
    4: {"色": "棕色", "水晶": "茶晶", "小物": "紙箱"},
    5: {"色": "黃色", "水晶": "黃水晶", "小物": "指南針"},
    6: {"色": "綠色", "水晶": "綠幽靈", "小物": "愛心"},
    7: {"色": "藍色", "水晶": "青金石", "小物": "書本"},
    8: {"色": "紫色", "水晶": "紫水晶", "小物": "獎盃"},
    9: {"色": "白色", "水晶": "白水晶", "小物": "白鴿"},
}

# ===== 工具函式 =====
def reduce_to_digit(n):
    while n > 9:
        n = sum(int(x) for x in str(n))
    return n

def format_layers(total):
    mid = sum(int(x) for x in str(total))
    return f"{total}/{mid}/{reduce_to_digit(mid)}" if mid > 9 else f"{total}/{mid}"

def get_flowing_year_ref(query_date, bday):
    query_date = query_date.date() if hasattr(query_date, "date") else query_date
    cutoff = datetime.date(query_date.year, bday.month, bday.day)
    return query_date.year - 1 if query_date < cutoff else query_date.year

def get_flowing_month_ref(query_date, birthday):
    query_date = query_date.date() if hasattr(query_date, "date") else query_date
    if query_date.day < birthday.day:
        return query_date.month - 1 if query_date.month > 1 else 12
    return query_date.month

# ===== Streamlit UI =====
st.set_page_config(page_title="樂覺製所生命靈數", layout="centered")
st.title("🧭 樂覺製所生命靈數")
st.markdown("在數字之中，  \n我們與自己不期而遇。  \n**Be true, be you — 讓靈魂，自在呼吸。**")

# ===== 使用者輸入 =====
birthday = st.date_input("請輸入生日", value=datetime.date(1990, 1, 1), min_value=datetime.date(1900, 1, 1))
target_year = st.number_input("請選擇年份", min_value=1900, max_value=2100, value=datetime.datetime.now().year)
target_month = st.selectbox("請選擇月份", list(range(1, 13)), index=datetime.datet_
