import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import date
import re

# 讀取外部 CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 初始化 session_state 用來存所有輸入資料
if "records" not in st.session_state:
    st.session_state["records"] = []

st.title("藥包機秤重轉顆數")

id = st.text_input("請輸入藥盒編號： ", value='')

df = pd.read_excel("machine_meta.xlsx")
columns = ['編號', '品項代碼', '藥名', '日期', '數量', '秤重']
try:
    if id == "":
        pass
    elif re.findall(r'\D', id):
        st.write(f"{id} 藥盒編號不對")
    elif int(id) > 400 or (int(id) not in df['編號'].to_list()):
        st.write("不存在")
    elif int(id):
        num = int(id)
        x = df.query('編號 == @num').values.tolist()
        st.markdown(f"<h5>品項代碼: {x[0][1]}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5>藥名: {x[0][2]}</h5>", unsafe_allow_html=True)
        note = st.text_input("日期： ", value='')
        # st.divider()
        regression = pd.read_excel("deming.xlsx")
        para = regression.query('編號 == @num')

        try:
            tab_real = st.text_input("數量： ", value='')
            if tab_real == '':
                tab_real = 0
            elif int(tab_real):
                tab_real = int(tab_real)

            wt = st.text_input("秤重： ", value='')
            if wt == '':
                wt = 0
                wt_float = float(wt)

            if float(wt):
                # Deming regression
                b0 = float(para.values.tolist()[0][1])
                b1 = float(para.values.tolist()[0][2])
                tab = np.round((float(wt) - b0)/ b1)
                # st.markdown(f'<p style="font-size:24px;">估計顆數：<strong> {int(tab)} 顆</strong> (資料累積中...)</p>', unsafe_allow_html=True)
                # st.markdown(f'<h5 style="color:mediumblue;font-size:1.2rem;font-weight:normal;">一筆新資料：{x[0][2]} 共：{tab_real}顆 重量：{wt}</h5>', unsafe_allow_html=True)
                if st.button("確定記錄此筆資料", type='primary'):
                    data_ls = [num, x[0][1], x[0][2], note, tab_real, wt]
                    st.session_state["records"].append(data_ls)
                
                st.markdown(f'<p style="font-size:24px;">估計顆數：<strong> {int(tab)} 顆</strong> (資料累積中...)</p>', unsafe_allow_html=True)
                st.markdown(f'<h5 style="color:mediumblue;font-size:1.2rem;font-weight:normal;">一筆新資料：{x[0][2]} 共：{tab_real}顆 重量：{wt}</h5>', unsafe_allow_html=True)
        except:
            st.write("資料格式不對！")
except:
    st.write('請確認藥盒編號')
    
st.subheader("目前累積紀錄")

if len(st.session_state["records"]) > 0:
    df_records = pd.DataFrame(st.session_state["records"],
                              columns=columns)
    st.dataframe(df_records, width="stretch")

    # 提供下載
    buffer = BytesIO()
    df_records.to_excel(buffer, index=False)
    st.download_button(
        label="下載 Excel",
        data=buffer.getvalue(),
        file_name=f"{date.today()}記錄.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.markdown(f'<h5 style="font-size:1.2rem;color:mediumblue;font-weight:normal;">尚無資料</h5>', unsafe_allow_html=True)
    