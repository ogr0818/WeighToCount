import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO, StringIO
from datetime import date

# 初始化 session_state 用來存所有輸入資料
if "records" not in st.session_state:
    st.session_state["records"] = []

st.title("藥包機顆數估算")
id = st.text_input("請輸入藥盒編號： ", value='')

df = pd.read_excel("machine_meta.xlsx")
columns = ['編號', '品項代碼', '藥名', '重量', '顆數']
try:
    if id == "":
        pass
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

        try:
            wt = st.text_input("重量： ", value='')
            if wt == '':
                wt = 0
            wt_float = float(wt)
            tab_real = st.text_input("實際顆數： ", value='')
            b0 = float(para.values.tolist()[0][1])
            b1 = float(para.values.tolist()[0][2])
            tab = np.round((float(wt) - b0)/ b1)
            st.write(f'估計顆數： {int(tab)}')
        except:
            st.write("資料格式不對！")
except:
    st.write('請確認藥盒編號')
    st.divider()
if st.button("確定記錄此筆資料", type='primary'):
    data_ls = [num, x[0][1], x[0][2], wt, tab_real]
    st.session_state["records"].append(data_ls)

    st.write(f"{x[0][2]} 存入一筆資料")
    st.write(f"總重：{wt} 共{tab_real}顆")

st.divider()
st.subheader("目前累積紀錄")

if len(st.session_state["records"]) > 0:
    df_records = pd.DataFrame(st.session_state["records"],
                              columns=columns)
    st.dataframe(df_records, use_container_width=True)

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
    st.write("尚無資料")
# with st.sidebar:
#     st.markdown('<h2 style="color:blue;font-size:24px">存檔輸出(.xlsx)： </h2>', unsafe_allow_html=True)
#     if st.button("Saved", type="primary"):
#         st.write("finished")