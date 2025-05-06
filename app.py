
import streamlit as st
import datetime
import pandas as pd

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
        "幸運色": "紅色",
        "水晶": "石榴石",
        "幸運小物": "💎"
    })

df = pd.DataFrame(data)



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
    # 主日數：流日
    main_number = d.day % 9 if d.day % 9 != 0 else 9
    meaning = day_meaning.get(main_number, {})

        # 流年計算（以生日為主；若當年生日尚未到，使用前一年）
    birth_md = (birthday.month, birthday.day)
    target_md = (d.month, d.day)
    ref_year = d.year - 1 if target_md < birth_md else d.year
    lifepath = sum(int(x) for x in f"{birthday.year}{birthday.month:02}{birthday.day:02}")
    lifepath = lifepath % 9 or 9

    flowing_year = (ref_year - birthday.year + lifepath) % 9 or 9
    flowing_month = ((d.month - birthday.month + 9) % 9) or 9
    flowing_day = ((d.day - birthday.day + 9) % 9) or 9



    data.append({
        "日期": d.strftime("%Y-%m-%d"),
        "主日數": main_number,
        "主日名稱": meaning.get("名稱", ""),
        "指引": meaning.get("指引", ""),
        "運勢指數": meaning.get("星", ""),
      "流年": f"{flowing_year} / {lifepath}",
"流月": f"{flowing_month} / {(birthday.month % 9 or 9)}",
"流日": f"{flowing_day} / {(birthday.day % 9 or 9)}",
      "幸運色": "紅色",
        "水晶": "石榴石",
        "幸運小物": "💎"
    })

df = pd.DataFrame(data)



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
