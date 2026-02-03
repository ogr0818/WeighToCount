import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


# 讀取外部 CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
st.title("藥包機四級管藥盤點")
machine = st.selectbox("藥包機編號：", ['1 號機', '2 號機'], index=1)
diff = timedelta(days=5)
min = datetime.today() - diff
max = datetime.today() + diff
note = st.date_input(
            "目前日期： ",
            value="today",
            min_value=min, max_value=max,
            format="YYYY-MM-DD",
                )
st.divider()
ctr_4 = ['384', '385', '386', '387', '388', '389',
         '390', '391', '392', '393', '394', '395',
         '396', '398', '399', '400']
# 藥品資訊
df = pd.read_excel("machine_meta.xlsx")
regression = pd.read_excel("deming.xlsx")
# columns = ['編號', '品項代碼', '藥名', '日期', '數量', '秤重']
def base(id):
    drug = df.query('編號 == @id')
    return drug.values.tolist()

with st.form("main_form", clear_on_submit=True):
    box_id = st.text_input("請輸入藥盒編號：", key="box_id", max_chars=3, value=3)
    weight = st.text_input("重量：", key="weight")

    submitted = st.form_submit_button("確定")
    try:
        float(weight)
    except:
        st.write("重量未輸或有非數字")

if submitted:
    if box_id in ctr_4:
        num = int(box_id)
        base = base(num)
        st.write(f'藥名：{base[0][2]}')
        # st.success("顆數: ")
        para = regression.query('編號 == @num')
        b0 = float(para.values.tolist()[0][1])
        b1 = float(para.values.tolist()[0][2])
        tab = np.round((float(weight) - b0)/ b1)
        st.markdown(
                    f"""
                    <p style="
                        font-size:34px; 
                        color:red; 
                        font-family: 'BiauKai','KaiTi','STKaiti','DFKai-SB', serif;
                    ">
                    估計顆數約：<strong>{int(tab)} 顆</strong>
                    </p>
                    """,
                    unsafe_allow_html=True
                    )
    else:
        if box_id.isdigit() == False:
            box_id = '0'
            st.markdown(f'<h5 style="color:red;">無藥盒編號 或 不是數字</h5>', unsafe_allow_html=True)
        elif int(box_id) > 400 or (int(box_id) not in df['編號'].to_list()):
            st.markdown(f'<h3 style="color:blue;">藥盒編號不存在</h3>', unsafe_allow_html=True)
        else:
            base = base(int(box_id))
            st.markdown(f'<h3 style="color:blue;">{base[0][2]}</h3>', unsafe_allow_html=True)
            st.markdown('🛑 :red[非藥包機四級管藥]')