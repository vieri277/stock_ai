import streamlit as st
import akshare as ak
import pandas as pd
import requests

# --- 1. 智谱配置区 (已根据你的截图填好) ---
ZHIPU_KEY = "b4ff7563b113457ea2f2e32fc3701f2d.gipphsslxToT7nyG"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# --- 2. AI 题材分析逻辑 ---
def get_ai_sector(news_content):
    headers = {"Authorization": f"Bearer {ZHIPU_KEY}"}
    payload = {
        "model": "glm-4",
        "messages": [
            {"role": "system", "content": "提取利好A股的具体板块名（如：零食、航天、影视）："},
            {"role": "user", "content": news_content}
        ]
    }
    try:
        res = requests.post(API_URL, json=payload, headers=headers).json()
        return res['choices'][0]['message']['content'].strip()
    except: return None

# --- 3. 低位筛选逻辑 ---
def scan_low_stocks(sector_name):
    try:
        stocks = ak.stock_board_concept_cons_em(symbol=sector_name)
        spot = ak.stock_zh_a_spot_em()
        df = pd.merge(stocks, spot, on="代码")
        # 你的硬指标：市值30-120亿，换手1.5-5.5
        filtered = df[(df['总市值'] > 3e9) & (df['总市值'] < 1.2e10) & (df['换手率'] > 1.5) & (df['换手率'] < 5.5)]
        return filtered[['代码', '名称_x', '最新价', '换手率']]
    except: return pd.DataFrame()

# --- 4. 网页界面 ---
st.title("🚀 沈阳老哥潜伏选股器")
st.write("逻辑：新浪快讯 -> 智谱AI提取题材 -> 匹配【低位+缩量】个股")

if st.button("🔄 点击刷新实时快讯并选股"):
    with st.spinner('正在分析中...'):
        news_df = ak.js_news(src="sina").head(10)
        for _, row in news_df.iterrows():
            with st.expander(f"📌 {row['content'][:30]}..."):
                st.write(row['content'])
                sector = get_ai_sector(row['content'])
                if sector:
                    st.warning(f"AI识别板块：{sector}")
                    res = scan_low_stocks(sector)
                    if not res.empty: st.table(res)
                    else: st.write("暂无符合形态个股")
