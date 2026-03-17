import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Market Analyser", page_icon="📈", layout="wide")
st.title("📈 Nifty50 Market Analyser")

# Symbols
SYMBOLS = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
    "LT", "AXISBANK", "ASIANPAINT", "MARUTI", "SUNPHARMA",
    "TITAN", "ULTRACEMCO", "BAJFINANCE", "WIPRO", "NESTLEIND"
]

# Sidebar
st.sidebar.header("Settings")
selected = st.sidebar.selectbox("Select Stock", SYMBOLS)
days = st.sidebar.slider("Days of History", 30, 365, 180)

# Fetch data
@st.cache_data
def load_data(symbol, days):
    end = datetime.now()
    start = end - timedelta(days=days)
    df = yf.download(symbol + ".NS", start=start, end=end)
    return df

with st.spinner("Fetching data..."):
    df = load_data(selected, days)

if df.empty:
    st.error("No data found. Try another stock.")
else:
    # Metrics row
    latest = df["Close"].iloc[-1]
    prev = df["Close"].iloc[-2]
    change = ((latest - prev) / prev * 100)

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Close", f"₹{float(latest):.2f}")
    col2.metric("Day Change", f"{float(change):.2f}%")
    col3.metric("Volume", f"{int(df['Volume'].iloc[-1]):,}")

    # Price chart
    st.subheader(f"{selected} Price Chart")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"].squeeze(),
        high=df["High"].squeeze(),
        low=df["Low"].squeeze(),
        close=df["Close"].squeeze(),
        name=selected
    ))
    fig.update_layout(xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Raw data
    if st.checkbox("Show raw data"):
        st.dataframe(df.tail(20))
