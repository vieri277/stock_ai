import streamlit as st
import akshare as ak
import pandas as pd
import requests

# --- 1. 智谱配置区 ---
ZHIPU_KEY = "b4ff7563b113457ea2f2e32fc3701f2d.S9vG0H7P9F9A9B9C"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

st.set_page_config(page_title="沈阳老哥潜伏助手", layout="wide")
st.title("🚀 沈阳老哥潜伏选股助手")

# --- 2. 极速测试逻辑 ---
st.subheader("📊 实时行情简报 (测试)")
try:
    with st.spinner('正在调取行情数据...'):
        # 抓取 A 股实时行情
        df = ak.stock_zh_a_spot_em()
        st.success("行情对接成功！")
        # 只显示前 5 行，防止手机端内存溢出卡死
        st.table(df.head(5)) 
except Exception as e:
    st.error(f"行情连接失败: {e}")

st.info("如果看到上面的表格，说明系统已经全线打通！")
