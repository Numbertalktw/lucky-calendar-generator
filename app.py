
import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="流年月曆生成器", layout="centered")

st.title("🗓️ 流年月曆生成器")
st.markdown("請輸入你的生日與要查看的月份，系統將產出整月的流日對照表")

# 生日輸入
birthday = st.date_input("請輸入你的生日", value=datetime.date(1990, 1, 1))
  min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()

# 年月選擇
target_year = st.number_input("請輸入年份", min_value=1900, max_value=2100, value=2025)
target_month = st.selectbox("請選擇月份", list(range(1, 13)))

if st.button("🎉 生成日曆"):
    st.success(f"生日：{birthday}｜目標月份：{target_year} 年 {target_month} 月")

    # 以下為示範資料
    days = pd.date_range(start=datetime.date(target_year, target_month, 1),
                         end=datetime.date(target_year, target_month, 28))
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
