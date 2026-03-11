import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests  # For NSE list

def get_nifty50_symbols():
    """Fetch live Nifty 50 symbols from NSE CSV (free, no key)."""
    url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    df = pd.read_csv(url)
    symbols = df['Symbol'].tolist()
    return [s + '.NS' for s in symbols]  # yfinance format[web:61][web:65]

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
