
import streamlit as st
import datetime
import pandas as pd

# 主日數對應的名稱、指引、星星數
day_meaning = {
    1: {"名稱": "創造日", "指引": "發揮行動力，啟動新的計畫與方向", "星": "⭐️⭐️⭐️⭐️"},
    2: {"名稱": "連結日", "指引": "傾聽與合作，建立支持與情感連結", "星": "⭐️⭐️⭐️"},
    3: {"名稱": "表達日", "指引": "敞開心扉，用創意傳達你的想法", "星": "⭐️⭐️⭐️⭐️"},
    4: {"名稱": "建構日", "指引": "紮實前行，適合組織與落實任務", "星": "⭐️⭐️⭐️"},
    5: {"名稱": "流動日", "指引": "擁抱改變，為生活注入新鮮與冒險", "星": "⭐️⭐️⭐️⭐️⭐️"},
    6: {"名稱": "關懷日", "指引": "照顧他人也別忘了照顧自己", "星": "⭐️⭐️⭐️⭐️"},
    7: {"名稱": "覺察日", "指引": "適合靜心內觀，釐清內在的方向與焦點", "星": "⭐️⭐️"},
    8: {"名稱": "成就日", "指引": "專注在資源與目標，放膽展現實力", "星": "⭐️⭐️⭐️⭐️"},
    9: {"名稱": "圓滿日", "指引": "放下執著，為下一個階段做準備", "星": "⭐️⭐️⭐️"},
}


st.set_page_config(page_title="流年月曆生成器", layout="centered")

st.title("🗓️ 流年月曆生成器")
st.markdown("請輸入你的生日與要查看的月份，系統將產出整月的流日對照表")

# 生日輸入
birthday = st.date_input(
    "請輸入你的生日",
    value=datetime.date(1990, 1, 1),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)


# 年月選擇
target_year = st.number_input("請輸入年份", min_value=1900, max_value=2100, value=2025)
target_month = st.selectbox("請選擇月份", list(range(1, 13)))

if st.button("🎉 生成日曆"):
    st.success(f"生日：{birthday}｜目標月份：{target_year} 年 {target_month} 月")

    # 以下為示範資料
    days = pd.date_range(start=datetime.date(target_year, target_month, 1),
                     end=datetime.date(target_year, target_month, 28))

data = []
for d in days:
    main_number = d.day % 9 if d.day % 9 != 0 else 9
    meaning = day_meaning.get(main_number, {})
    data.append({
        "日期": d.strftime("%Y-%m-%d"),
        "主日數": main_number,
        "主日名稱": meaning.get("名稱", ""),
        "指引": meaning.get("指引", ""),
        "運勢指數": meaning.get("星", ""),
        "幸運色": "紅色",  # 可替換為動態邏輯
        "水晶": "石榴石",
        "幸運小物": "💎",
    })

df = pd.DataFrame(data)
st.dataframe(df)


    data = pd.DataFrame({
        "日期": days,
        "主日數": [i.day % 9 + 1 for i in days],
        "主日名稱": ["創造" if i.day % 9 + 1 == 1 else "其他" for i in days],
        "運勢指數": ["⭐️⭐️⭐️" for _ in days],
        "指引": ["相信自己" for _ in days],
        "幸運色": ["紅色" for _ in days],
        "水晶": ["石榴石" for _ in days],
        "幸運小物": ["💎" for _ in days],
    })

    st.dataframe(data)

    

    # 下載 Excel
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name="流年月曆")
    st.download_button("📥 下載 Excel", data=output.getvalue(), file_name="流年月曆.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
