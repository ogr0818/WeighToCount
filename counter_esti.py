import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import date
import re
from datetime import datetime, timedelta

tab1, tab2 = st.tabs(["藥包機四級管藥盤點", "藥包機秤重轉顆數"])
with tab1:
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

with tab2:
    # 讀取外部 CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # 初始化 session_state 用來存所有輸入資料
    if "records" not in st.session_state:
        st.session_state["records"] = []

    st.title("藥包機秤重轉顆數")

    # machine = st.selectbox("藥包機編號：", ['1 號機', '2 號機'], index=1)   # 加入藥包機編號
    # # 外插日期
    # note = st.date_input(
    #             "目前日期： ",
    #             value="today",
    #             format="YYYY-MM-DD",
    #                 )
    # st.divider()
    # id = st.text_input("請輸入藥盒編號： ", value='385', key="box_id")    # 預設 4 級管藥

    # df = pd.read_excel("machine_meta.xlsx")
    # columns = ['編號', '品項代碼', '藥名', '日期', '數量', '秤重']

    # try:
    #     if id == "":
    #         pass
    #     elif re.findall(r'\D', id):
    #         st.write(f"{id} 藥盒編號不對")
    #     elif int(id) > 400 or (int(id) not in df['編號'].to_list()):
    #         st.markdown(f'<h2 style="color:blue;">藥盒編號不存在</h2>', unsafe_allow_html=True)
    #     elif int(id):
    #         num = int(id)
    #         x = df.query('編號 == @num').values.tolist()
    #         st.markdown(f"<h5>品項代碼: {x[0][1]}</h5>", unsafe_allow_html=True)
    #         st.markdown(f"<h5>藥名: {x[0][2]}</h5>", unsafe_allow_html=True)
    #         # st.divider()
    #         # note = st.text_input("日期： ", value='')

    #         regression = pd.read_excel("deming.xlsx")
    #         para = regression.query('編號 == @num')
            
    #         try:
    #             # tab_real = st.text_input("數量： ", value='')   # closed the show
    #             tab_real = 0 # 外插預設值
    #             if tab_real == '':
    #                 tab_real = 0
    #             elif int(tab_real):
    #                 tab_real = int(tab_real)

    #             wt = st.text_input("藥品重量： ", value='') # 秤重
    #             if wt == '':
    #                 wt = 0
    #                 wt_float = float(wt)

    #             if float(wt):
    #                 if para.empty:
    #                     st.markdown(f'<p style="font-size:24px;">暫時無法估計顆數</p>', unsafe_allow_html=True)
    #                     # if st.button("確定記錄此筆資料", type='primary'):
    #                     #     data_ls = [num, x[0][1], x[0][2], note, tab_real, wt]
    #                     #     st.session_state["records"].append(data_ls)

    #                 # Deming regression
    #                 else:
    #                     b0 = float(para.values.tolist()[0][1])
    #                     b1 = float(para.values.tolist()[0][2])
    #                     tab = np.round((float(wt) - b0)/ b1)
    #                     # st.markdown(f'<p style="font-size:24px;">估計顆數：<strong> {int(tab)} 顆</strong> (資料累積中...)</p>', unsafe_allow_html=True)
    #                     # st.markdown(f'<h5 style="color:mediumblue;font-size:1.2rem;font-weight:normal;">一筆新資料：{x[0][2]} 共：{tab_real}顆 重量：{wt}</h5>', unsafe_allow_html=True)
    #                     # if st.button("確定記錄此筆資料", type='primary'):
    #                     #     data_ls = [num, x[0][1], x[0][2], note, tab_real, wt]
    #                     #     st.session_state["records"].append(data_ls)
                        
    #                     # st.markdown(f'<p style="font-size:34px; color:red">估計顆數：<strong> {int(tab)} 顆</strong></p>', unsafe_allow_html=True) #  (資料累積中...)
    #                     # st.markdown(f'<h5 style="color:mediumblue;font-size:1.2rem;font-weight:normal;">一筆新資料：{x[0][2]} 共：{tab_real}顆 重量：{wt}</h5>', unsafe_allow_html=True)

    #                     st.markdown(
    #                                 f"""
    #                                 <p style="
    #                                     font-size:34px; 
    #                                     color:red; 
    #                                     font-family: 'BiauKai','KaiTi','STKaiti','DFKai-SB', serif;
    #                                 ">
    #                                 估計顆數約：<strong>{int(tab)} 顆</strong>
    #                                 </p>
    #                                 """,
    #                                 unsafe_allow_html=True
    #                                 )
                        
    #                     # st.write(f"{((float(wt) - b0)/ b1):.3f}") # 觀察小數後2位
    #         except:
    #             st.write(f"資料格式不對！")
    # except:
    #     st.write('請確認藥盒編號')
        
    # # st.subheader("目前累積紀錄")

    # # if len(st.session_state["records"]) > 0:
    # #     df_records = pd.DataFrame(st.session_state["records"],
    # #                               columns=columns)
    # #     st.dataframe(df_records, width="stretch")

    # #     # 提供下載
    # #     buffer = BytesIO()
    # #     df_records.to_excel(buffer, index=False)
    # #     st.download_button(
    # #         label="下載 Excel",
    # #         data=buffer.getvalue(),
    # #         file_name=f"{date.today()}記錄.xlsx",
    # #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # #     )
    # # else:
    # #     st.markdown(f'<h5 style="font-size:1.2rem;color:mediumblue;font-weight:normal;">尚無資料</h5>', unsafe_allow_html=True)
        
    # if st.button("清除藥盒編號"):
    #     # st.session_state["box_id"] = ""
    #     st.rerun()