import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests  # For NSE list

def get_nifty50_symbols():
    """Hardcoded Nifty 50 symbols (yfinance format)."""
    symbols = [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
        "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
        "LT", "AXISBANK", "ASIANPAINT", "MARUTI", "SUNPHARMA",
        "TITAN", "ULTRACEMCO", "BAJFINANCE", "WIPRO", "NESTLEIND"
    ]
    return [s + ".NS" for s in symbols]

def fetch_data(symbols=None, days=365):
    """Download OHLCV data."""
    if symbols is None:
        symbols = get_nifty50_symbols()[:10]  # Start small
    end = datetime.now()
    start = end - timedelta(days=days)
    data = yf.download(symbols, start=start, end=end, group_by='ticker')
    print(f"Fetched {len(data.columns)} tickers")
    return data

# Test
if __name__ == "__main__":
    data = fetch_data()
    data.to_csv('data/nifty_sample.csv')
    print("Saved to data/nifty_sample.csv")
