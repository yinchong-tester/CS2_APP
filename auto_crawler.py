import time
from api_service import get_skin_price
from data_manager import get_skin_name

#获取哈希名的列表
def get_hash_name_list():
    hash_name_list = list(get_skin_name().values())
    return hash_name_list

def run_crawler_job(L):
    '''
    输入名称列表，每一小时自动抓取所有饰品的价格数据，并存储到数据库
    '''
    for name in L:
        try:
            get_skin_price(name)
            print(f'抓取{name}成功')

        except Exception as e:
            print(f"抓取{name}失败:{e}")
        time.sleep(1.01)

hash_name_list = get_hash_name_list()
while True:
    run_crawler_job(hash_name_list)
    print('休息时间')
    time.sleep(43200)