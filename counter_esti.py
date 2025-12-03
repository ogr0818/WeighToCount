import numpy as np
import pandas as pd
import streamlit as st


st.title("藥包機顆數估算")
id = st.text_input("請輸入藥盒編號： ", value='')

df = pd.read_excel("machine_meta.xlsx")
if id == "":
    st.write("不存在")
elif int(id) > 400 or (int(id) not in df['編號'].to_list()):
    st.write("不存在")
else:
    num = int(id)
    x = df.query('編號 == @num').values.tolist()
    st.write(f'品項代碼: {x[0][1]}')
    st.write(f'藥名: {x[0][2]}')
    st.divider()
    regression = pd.read_excel("deming.xlsx")
    para = regression.query('編號 == @num')

    wt = st.text_input("重量： ", value=0)
    tab_real = st.text_input("實際顆數： ", value='')
    b0 = float(para.values.tolist()[0][1])
    b1 = float(para.values.tolist()[0][2])
    tab = np.round((float(wt) - b0)/ b1)
    st.write(f'估計顆數： {int(tab)}')
    st.divider()
if st.button("確定記錄本筆資料", type='primary'):
    st.write(f"{x[0][2]} 存入一筆資料")
    st.write(f"總重：{wt} 共{tab_real}顆")

# with st.sidebar:
#     st.markdown('<h2 style="color:blue;font-size:24px">存檔輸出(.xlsx)： </h2>', unsafe_allow_html=True)
#     if st.button("Saved", type="primary"):
#         st.write("finished")