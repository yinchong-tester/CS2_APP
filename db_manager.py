"""
此文件用来创建连接数据库的函数，写入价格的函数和供AI读取数据库进行分析的函数


"""
import pymysql
from config import DB_CONFIG

#定义函数
#写入价格函数
def store_history_price(market_hash_name,price):
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            #print('数据库连接成功')
            try:
                with conn.cursor() as cursor:
                    sql = 'INSERT INTO skins_history_price (market_hash_name,price) VALUES(%s,%s)'  # 占位符%s防止sql注入
                    data = (market_hash_name, price)
                    # 执行SQL语句
                    cursor.execute(sql, data)
                conn.commit()
                #print('数据插入成功')
            except Exception as e:
                conn.rollback()#回滚
                print(f'数据插入失败{e}')
    except Exception as e:
        print(f'数据库连接失败,无法写入数据{e}')

#抓取MySQL中数据给AI
def fetch_data_for_ai(market_hash_name):
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            #print('数据库连接成功')
            try:
                with conn.cursor() as cursor:
                    #增加了按时间正序排序，只取最近两个月的数据
                    fetch_sql = '''SELECT price,created_at
                                   FROM skins_history_price 
                                   WHERE market_hash_name = %s
                                   AND created_at >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
                                   ORDER BY created_at ASC'''
                    params = (market_hash_name,)
                    #execute执行语句
                    cursor.execute(fetch_sql, params)
                    results = cursor.fetchall()
                    return results

            except Exception as e:
                    print(f"查询失败: {e}")

    except Exception as e:
        print(f'数据库连接失败,无法读取数据{e}')
        return []