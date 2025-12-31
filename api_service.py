"""
此文件用于调取饰品的实时数据，并且将每次的价格都写入MySQL，每次运行app.py都需要重新调用一次新数据


"""
import requests
import streamlit as st
from db_manager import store_history_price

def get_skin_price(market_hash_name):
    """
    从SteamDT获取到搜索饰品的数据,并存储到数据库,返回价格
    """
    if not market_hash_name:
        return None

    try:
        Steamdt_API_KEY = "af3eaaddc6474f86a54eaa10096a766b"
        URL_data='https://open.steamdt.com/open/cs2/v1/price/single'
        headers = {"Authorization": "Bearer " + Steamdt_API_KEY}
        query_params = {
            'marketHashName':market_hash_name
        }
        response = requests.get(URL_data,params=query_params,headers=headers,timeout=5)
        if response.status_code == 200:  # 成功状态码200
            response_data = response.json()
            #处理数据
            skindata_list = response_data.get('data',[])
            if not skindata_list:
                st.warning(f"未找到饰品数据: {market_hash_name}")
                return None
            UU_platform_data = skindata_list[0]
            #获取价格
            sellPrice = UU_platform_data.get('sellPrice')
            #存储价格
            store_history_price(market_hash_name,float(sellPrice))
            try:
                return float(sellPrice)
            except (ValueError,TypeError):
                return None

        else:
            st.error(f'价格数据获取失败,状态码:{response.status_code}')
            return None

    except Exception as e:
        st.error(f"数据API请求失败:{e}")
        return None

def get_ava_price(market_hash_name):
    """
    获取饰品的七日均价
    """
    if not market_hash_name:
        return None

    try:
        Steamdt_API_KEY = "af3eaaddc6474f86a54eaa10096a766b"
        URL_avg = 'https://open.steamdt.com/open/cs2/v1/price/avg'
        headers = {"Authorization": "Bearer " + Steamdt_API_KEY}
        query_params = {
            'marketHashName': market_hash_name
        }
        response = requests.get(URL_avg, params=query_params, headers=headers, timeout=5)
        avg_price = None
        if response.status_code == 200:
            response_data = response.json()
            #处理数据
            avg_dict = response_data.get('data',{})
            #获取价格
            avg_price = avg_dict.get('avgPrice',None)

            try:
                return float(avg_price)

            except (ValueError, TypeError):
                return None

        else:
            st.error(f'均价数据获取失败,状态码:{response.status_code}')
            return None

    except Exception as e:
        st.error(f"均价API请求失败:{e}")
        return None