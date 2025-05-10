import streamlit as st
import datetime
import pandas as pd
from io import BytesIO

# ========== 設定 ==========
st.set_page_config(page_title="LuckyCalendar - 樂覺製所", layout="centered")

# 品牌標題與標語
st.title("🌟 樂覺製所生命靈數")
st.markdown("""
在數字之中，我們與自己不期而遇。  
Be true, be you — 讓靈魂自在呼吸。
""")


# 使用者輸入
birthday = st.date_input(
    "請輸入你的生日",
    value=datetime.date(1990, 1, 1),
    min_value=datetime.date(1900, 1, 1),  # ✅ 加上這一行
    max_value=datetime.date.today()
)
target_year = st.number_input("請輸入年份", min_value=1900, max_value=2100, value=datetime.datetime.now().year)
target_month = st.selectbox("請選擇月份", list(range(1, 13)), index=datetime.datetime.now().month - 1)

# ===== 資料對應表 =====
day_meaning = {
    1: {"名稱": "創造日", "指引": "展現創意，展現自我魅力。"},
    2: {"名稱": "連結日", "指引": "適合合作、溝通與等待機會。"},
    3: {"名稱": "表達日", "指引": "表達想法，展現自我魅力。"},
    4: {"名稱": "實作日", "指引": "建立基礎，適合細節與規劃。"},
    5: {"名稱": "行動日", "指引": "啟動新的計畫，做出主動選擇。"},
    6: {"名稱": "關係日", "指引": "接觸愛情，適當調整。"},
    7: {"名稱": "內省日", "指引": "適合學習、休息與自我對話。"},
    8: {"名稱": "成果日", "指引": "聚焦目標與務成就。"},
    9: {"名稱": "釋放日", "指引": "放手，療癒與完成階段。"},
}

lucky_map = {
    1: {"色": "紅色", "水晶": "紅瑪瑙", "小物": "鋼筆"},
    2: {"色": "粉紅色", "水晶": "粉晶", "小物": "情書"},
    3: {"色": "橙色", "水晶": "太陽石", "小物": "麥克風"},
    4: {"色": "棕色", "水晶": "茶晶", "小物": "紙箱"},
    5: {"色": "黃色", "水晶": "黃水晶", "小物": "指南針"},
    6: {"色": "綠色", "水晶": "綠幽靈", "小物": "心型石"},
    7: {"色": "藍色", "水晶": "青金石", "小物": "書本"},
    8: {"色": "紫色", "水晶": "紫水晶", "小物": "獎盃"},
    9: {"色": "白色", "水晶": "白水晶", "小物": "羽毛"},
}

# ===== 工具函式 =====
def reduce_to_digit(n):
    while n > 9:
        n = sum(int(x) for x in str(n))
    return n

def format_layers(total):
    mid = sum(int(x) for x in str(total))
    return f"{total}/{mid}/{reduce_to_digit(mid)}" if mid > 9 else f"{total}/{mid}"

def get_flowing_year_ref(query_date, birthday):
    bday = datetime.date(query_date.year, birthday.month, birthday.day)
    return query_date.year - 1 if query_date < bday else query_date.year

def get_flowing_month_ref(query_date, birthday):
    return query_date.month - 1 if query_date.day < birthday.day else query_date.month

# ===== 主運算區塊 =====
if st.button("🎉 產生日曆建議表"):

    # 日期範圍
    last_day = (datetime.date(target_year, target_month % 12 + 1, 1) - datetime.timedelta(days=1)).day
    days = pd.date_range(start=datetime.date(target_year, target_month, 1),
                         end=datetime.date(target_year, target_month, last_day))

    data = []
    for d in days:
        main_number = d.day % 9 or 9
        meaning = day_meaning.get(main_number, {})
        lucky = lucky_map.get(main_number, {})

        # 流年邏輯
        year_ref = get_flowing_year_ref(d, birthday)
        fy_total = sum(int(x) for x in f"{year_ref}{birthday.month:02}{birthday.day:02}")
        flowing_year = format_layers(fy_total)

        # 流日邏輯（包含主日數作為流日主數）
        fd_total = sum(int(x) for x in f"{birthday.year}{birthday.month:02}{d.day:02}")
        fd_mid = sum(int(x) for x in str(fd_total))
        fd_final = reduce_to_digit(fd_mid) if fd_mid > 9 else fd_mid
        flowing_day = f"{fd_total}/{fd_mid}/{fd_final}" if fd_mid > 9 else f"{fd_total}/{fd_mid}"

        # 改為使用流日的主數作為主日數
        main_number = fd_final


        # 流日邏輯
        fd_total = sum(int(x) for x in f"{birthday.year}{birthday.month:02}{d.day:02}")
        flowing_day = format_layers(fd_total)

        data.append({
            "日期": d.strftime("%Y-%m-%d"),
            "流年": flowing_year,
            "流月": flowing_month,
            "流日": flowing_day,
            "主日數": main_number,
            "主日名稱": meaning.get("名稱", ""),
            "指引": meaning.get("指引", ""),
            "幸運色": lucky.get("色", ""),
            "水晶": lucky.get("水晶", ""),
            "幸運小物": lucky.get("小物", "")
        })

    df = pd.DataFrame(data)
    st.dataframe(df)

    # 下載區塊
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="LuckyCalendar")
    output.seek(0)

    filename = f"LuckyCalendar_{target_year}_{target_month:02}.xlsx"
    label = f"📥 點此下載 {target_year} 年 {target_month} 月靈數流日建議表（三層加總斜線版）"
    st.download_button(label, data=output.read(), file_name=filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

