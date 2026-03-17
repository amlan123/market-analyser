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
selected = st.sidebar.multiselect(
    "Select Stocks to Compare",
    SYMBOLS,
    default=["RELIANCE", "TCS", "INFY"]
)
days = st.sidebar.slider("Days of History", 30, 365, 180)
normalize = st.sidebar.checkbox("Normalize to 100 (compare % growth)", value=True)

if not selected:
    st.warning("Please select at least one stock.")
    st.stop()

# Fetch data
@st.cache_data
def load_data(symbol, days):
    end = datetime.now()
    start = end - timedelta(days=days)
    df = yf.download(symbol + ".NS", start=start, end=end)
    return df["Close"]

# Metrics row
st.subheader("Latest Snapshot")
cols = st.columns(len(selected))
for i, symbol in enumerate(selected):
    df = load_data(symbol, days)
    if not df.empty:
        latest = float(df.iloc[-1])
        prev = float(df.iloc[-2])
        change = (latest - prev) / prev * 100
        cols[i].metric(symbol, f"₹{latest:.2f}", f"{change:.2f}%")

# Comparison chart
st.subheader("Price Comparison Chart")
fig = go.Figure()

for symbol in selected:
    df = load_data(symbol, days)
    if not df.empty:
        if normalize:
            series = (df / df.iloc[0]) * 100
        else:
            series = df
        fig.add_trace(go.Scatter(
            x=series.index,
            y=series.values.flatten(),
            name=symbol,
            mode="lines"
        ))

fig.update_layout(
    height=500,
    xaxis_title="Date",
    yaxis_title="Normalized Price (base 100)" if normalize else "Price (₹)",
    legend_title="Stocks",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)