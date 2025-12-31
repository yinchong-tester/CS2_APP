"""
此文件为主模块,调用了其他模块的函数,并且用streamlit完成了对用户的分析展示


"""
import streamlit as st
import pandas as pd
from data_manager import get_skin_name
from api_service import  get_skin_price,get_ava_price
from ai_analyst import  analyze_skin_market,generate_history_prompt
from db_manager import  fetch_data_for_ai

#读取饰品名字字典
Skin_Dict = get_skin_name(force_update=False)
#制作头部搜索框
col1, col2 = st.columns([3, 2])
with col1:
    st.title('CS饰品分析助手(搭载 DeepSeek 版)')
    st.caption('基于steamDT数据')
with col2:
    st.write('')  #空行美观
    selected_skin_cn = st.selectbox(
        '搜索饰品名称',
        options=list(Skin_Dict.keys()),
        index=None,
        placeholder='请输入饰品名称',
        label_visibility='collapsed'
    )
selected_skin_hash_name = None
if selected_skin_cn:
    st.success(f"你选择了:{selected_skin_cn}")
    #把选择的中文名对应到其哈希名
    selected_skin_hash_name = Skin_Dict[selected_skin_cn]

# 网页交互
if st.button('点击开始分析饰品数据'):
    st.write('准备开始分析')
    if selected_skin_hash_name:
        selected_skin_price = get_skin_price(selected_skin_hash_name)
        selected_skin_avg = get_ava_price(selected_skin_hash_name)
        st.write(f'{selected_skin_cn}的价格是:{selected_skin_price}元')
        st.write(f'{selected_skin_cn}的七天均价是:{selected_skin_avg}元')
        #调用历史数据投喂给AI
        history_data = fetch_data_for_ai(selected_skin_hash_name)
        generate_history_prompt(history_data)
        #生成可视化图表
        df = pd.DataFrame(history_data,columns=['Price','Time'])
        df['Time'] = pd.to_datetime(df['Time'])
        df['Price'] = df['Price'].astype(float)
        df.set_index('Time', inplace=True)
        st.subheader('历史价格走势图')
        st.line_chart(df)

        #调用AI进行数据分析
        analyze_skin_market(selected_skin_cn,selected_skin_price,selected_skin_avg,history_data=history_data)
    else:
        st.warning('请选择一个饰品')