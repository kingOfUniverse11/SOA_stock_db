import yfinance as yf
import pandas as pd

# Get the list of S&P 500 tickers
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sp500_df = table[0]
tickers = sp500_df['Symbol'].tolist()

# Define the date range
start_date = '2010-01-01'
end_date = '2015-12-31'

# Download historical data for each ticker in the date range
for ticker in tickers:
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            data.to_csv(f'{ticker}.csv')
            print(f"Downloaded {ticker} data")
        else:
            print(f"No data found for {ticker}")
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")