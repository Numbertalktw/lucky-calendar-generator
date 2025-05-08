import streamlit as st
import datetime
import pandas as pd
from io import BytesIO
import calendar

# 主日數對應資料
day_meaning = {
    1: {"名稱": "創造日", "指引": "展現創意，展現自我魅力。", "星": "⭐⭐⭐⭐"},
    2: {"名稱": "連結日", "指引": "適合合作、溝通與等待機會。", "星": "⭐⭐"},
    3: {"名稱": "表達日", "指引": "表達想法，展現自我魅力。", "星": "⭐⭐⭐"},
    4: {"名稱": "實作日", "指引": "建立基礎，適合細節與規劃。", "星": "⭐⭐⭐"},
    5: {"名稱": "行動日", "指引": "啟動新的計畫，做出主動選擇。", "星": "⭐⭐⭐⭐"},
    6: {"名稱": "關係日", "指引": "接觸愛情，適當調整。", "星": "⭐⭐⭐"},
    7: {"名稱": "內省日", "指引": "適合學習、休息與自我對話。", "星": "⭐"},
    8: {"名稱": "成果日", "指引": "聚焦目標與務成就。", "星": "⭐⭐⭐⭐"},
    9: {"名稱": "釋放日", "指引": "放手，療癒與完成階段。", "星": "⭐⭐"},
}

# 對應的顏色、水晶、小物
lucky_map = {
    1: {"色": "紅色", "水晶": "紅瑪瑙", "小物": "🖊️"},
    2: {"色": "粉紅色", "水晶": "粉晶", "小物": "💌"},
    3: {"色": "橙色", "水晶": "太陽石", "小物": "🎤"},
    4: {"色": "棕色", "水晶": "茶晶", "小物": "📦"},
    5: {"色": "黃色", "水晶": "黃水晶", "小物": "🧭"},
    6: {"色": "綠色", "水晶": "綠幽靈", "小物": "💗"},
    7: {"色": "藍色", "水晶": "青金石", "小物": "📖"},
    8: {"色": "紫色", "水晶": "紫水晶", "小物": "🏆"},
    9: {"色": "白色", "水晶": "白水晶", "小物": "🕊️"},
}

# 數字加總遞減到個位數（reduce_to_digit）
def reduce_to_digit(n):
    while n > 9:
        n = sum(int(x) for x in str(n))
    return n

# UI 設定
st.set_page_config(page_title="流年月曆生成器", layout="centered")
st.title("🗓️ 流年月曆生成器")
st.markdown("請輸入你的生日與要查看的月份，系統將產出整月的流日對照表")

# 使用者輸入
birthday = st.date_input("請輸入你的生日", value=datetime.date(1990, 1, 1),
                         min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
target_year = st.number_input("請輸入年份", min_value=1900, max_value=2100, value=2025)
target_month = st.selectbox("請選擇月份", list(range(1, 13)))

# 點擊生成
if st.button("🎉 生成日曆"):
    st.success(f"生日：{birthday}｜目標月份：{target_year} 年 {target_month} 月")

    # 計算該月最後一天
    _, last_day = calendar.monthrange(target_year, target_month)
    days = pd.date_range(start=datetime.date(target_year, target_month, 1),
                         end=datetime.date(target_year, target_month, last_day))

    data = []
    for d in days:
        main_number = d.day % 9 if d.day % 9 != 0 else 9
        meaning = day_meaning.get(main_number, {})
        lucky = lucky_map.get(main_number, {})

        # 流年（查詢年＋出生月日）
        flowing_year_sum = sum(int(x) for x in f"{d.year}{birthday.month:02}{birthday.day:02}")
        flowing_year_mid = sum(int(x) for x in str(flowing_year_sum))
        flowing_year_final = reduce_to_digit(flowing_year_mid) if flowing_year_mid > 9 else flowing_year_mid

        # 流月（出生年＋查詢月＋出生日）
        flowing_month_sum = sum(int(x) for x in f"{birthday.year}{d.month:02}{birthday.day:02}")
        flowing_month_mid = sum(int(x) for x in str(flowing_month_sum))
        flowing_month_final = reduce_to_digit(flowing_month_mid) if flowing_month_mid > 9 else flowing_month_mid

        # 流日（出生年＋出生月＋查詢日）
        flowing_day_sum = sum(int(x) for x in f"{birthday.year}{birthday.month:02}{d.day:02}")
        flowing_day_mid = sum(int(x) for x in str(flowing_day_sum))
        flowing_day_final = reduce_to_digit(flowing_day_mid) if flowing_day_mid > 9 else flowing_day_mid

        data.append({
            "日期": d.strftime("%Y-%m-%d"),
            "主日數": main_number,
            "主日名稱": meaning.get("名稱", ""),
            "指引": meaning.get("指引", ""),
            "運勢指數": meaning.get("星", ""),
            "流年": f"{flowing_year_sum}/{flowing_year_mid}/{flowing_year_final}" if flowing_year_mid > 9 else f"{flowing_year_sum}/{flowing_year_mid}",
            "流月": f"{flowing_month_sum}/{flowing_month_mid}/{flowing_month_final}" if flowing_month_mid > 9 else f"{flowing_month_sum}/{flowing_month_mid}",
            "流日": f"{flowing_day_sum}/{flowing_day_mid}/{flowing_day_final}" if flowing_day_mid > 9 else f"{flowing_day_sum}/{flowing_day_mid}",
            "幸運色": lucky.get("色", ""),
            "水晶": lucky.get("水晶", ""),
            "幸運小物": lucky.get("小物", "")
        })

    df = pd.DataFrame(data)
    st.dataframe(df)

    # 匯出 Excel（含空檢查）
    if isinstance(df, pd.DataFrame) and not df.empty and df.dropna(how='all').shape[0] > 0:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="流年月曆")
        st.download_button("📥 下載 Excel", data=output.getvalue(),
                           file_name="流年月曆.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("⚠️ 無法匯出 Excel：目前資料為空，請先產生日曆資料")
