"""
此文件用于把数据投喂给AI，并令其生成分析文本


"""
import streamlit as st
from openai import OpenAI
from config import  DEEPSEEK_API_KEY
#初始化客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def generate_history_prompt(history_data):
    if not history_data:
        return "暂无历史价格记录。"

    # 简单的拼接逻辑：把时间和价格拼成一行行的文本
    lines = []
    # 限制一下条数，防止token爆炸，比如只取最近15条
    recent_data = history_data[-15:]
    for price, created_at in recent_data:
        # 格式化一下时间，精确到分即可
        time_str = created_at.strftime("%m-%d %H:%M")
        lines.append(f"- {time_str}: ¥{price}")

    return "\n".join(lines)

def analyze_skin_market(skin_name,price,avg_price,volume='暂无数据',history_data=None):
    """
    调用 DeepSeek AI 对饰品数据进行分析
    """
    history_text = "暂无数据"
    if history_data:
        history_text = generate_history_prompt(history_data)

    system_prompt = """
        你是一名专业的金融分析师，同时也是一位经验丰富的 CS2 饰品市场交易员。你的分析风格客观、专业，擅长技术面和市场情绪分析。
        请根据用户提供的饰品数据，输出一份专业的、置于100字和200字之间的分析报告。
        报告必须包括以下关键点：
        1. 当前价格的简短点评。
        2. 对流动性（如销量）和稳定性（如趋势）的推测和分析。
        3. 给出明确的投资建议：【买入】、【卖出】或【观望】。
        """
    user_prompt = f"""
    分析对象：{skin_name}
    当前价格：{price} CNY
    七日均价：{avg_price} CNY
    近期销量：{volume}
    【历史价格记录（近两个月部分数据）】：
    {history_text}
    
    请根据以上数据进行分析，并给出最终建议。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        if response.choices:
            analysis_text = response.choices[0].message.content
            st.markdown(analysis_text)
        else:
            st.warning("AI未能生成分析结果。")
    except Exception as e:
        st.error(f"AI分析失败:{e}")