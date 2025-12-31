"""
此文件用于调取饰品名称，并保存在本地，以便其他模块使用


"""
import json
import os
import requests
import streamlit as st

#读取位于其他文件夹的json数据
CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE_PATH)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CACHE_FILE = os.path.join(PROJECT_ROOT, "local_data", "skins_data.json")

def get_skin_name(force_update=False):
    """
    从 SteamDT API 获取所有饰品名称，并生成一个字典,中文名:哈希名,优先使用本地存储的数据
    默认情况(force_update=False)：只读本地文件
    只有当本地文件不存在，或者当你手动指定 force_update=True 时，才调用API更新数据
    """
    if not force_update and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE,'r',encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f'读取缓存文件出错,重新下载:{e}')

    #每日只能调用一次API
    st.info("正在从服务器获取最新饰品列表（消耗每日额度）...")
    try:
        Steamdt_API_KEY = "af3eaaddc6474f86a54eaa10096a766b"
        Steamdt_LIST_URL = "https://open.steamdt.com/open/cs2/v1/base"
        headers = {"Authorization": "Bearer " + Steamdt_API_KEY} #搭载key的头请求
        response = requests.get(Steamdt_LIST_URL, headers=headers,timeout=10)
        if response.status_code == 200:#成功状态码200
            data = response.json()
            #打印一下keys或者第一条数据看看结构，看到了是在data里面
            #keys_list = list(data.keys())
            #st.write("API 返回数据的键列表：", keys_list)
            item_list = data.get('data',[])
            print("这是物品的列表内容:",item_list)
            if item_list is None:
                # 获取错误信息，如果没有就显示“未知错误”
                error_msg = data.get('errorMsg') or data.get('msg') or "API未返回具体错误原因"
                st.error(f"数据获取失败！服务器回复: {error_msg}")
                # 打印完整数据在控制台
                print("【调试信息】完整返回数据:", data)
                return {}
            #获得了饰品信息之后，把名字提取为字典
            skin_map = {}
            for item in item_list:
                Chinese_Name = item.get('name')#用于展示给用户中文名
                English_Hash_Name = item.get('marketHashName')#仅用于后面查询饰品数据
                if Chinese_Name and English_Hash_Name:
                    skin_map[Chinese_Name] = English_Hash_Name

            #保存到本地
            with open(CACHE_FILE,'w',encoding='utf-8') as f:
                json.dump(skin_map, f, ensure_ascii=False)
            print('数据更新完毕')
            return skin_map

        else:
            st.error(f"数据获取失败，状态码: {response.status_code}")
            return{}

    except Exception as e:
        st.error(f"API请求失败:{e}")
        return{}