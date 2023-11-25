import pandas as pd
import yfinance as yf
import psycopg2

connectionToAWS = psycopg2.connect(
    dbname="stock_data",
    user="postgres",
    password="nazim4471",
    host="my-db-instance.cxjzjls8ya5o.us-east-2.rds.amazonaws.com",
    port='5432'
)

table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sp500_df = table[0]
tickers = sp500_df['Symbol'].tolist()

# conn = connectionToMyLocal
conn = connectionToAWS
cursor = conn.cursor()


# def get_ticker_name(ticker_symbol):
#     try:
#         ticker = yf.Ticker(ticker_symbol)
#         tickerName = ticker.info['longName']
#         stockTableQuery = f"UPDATE \"STOCKS\" SET stock_name = \'{tickerName}\' where stock_symbol =\'{ticker}\';"
#         cursor.execute(stockTableQuery)
#         conn.commit()

#         return tickerName
    
#     except Exception as e:
#         return f"Error: {e}"

# Replace 'AAPL' with your ticker symbol
# symbol = 'AAPL'
def get_ticker_name(tickers):
    for ticker in tickers:
        try:
            tickerYahoo = yf.Ticker(ticker)
            tickerName = tickerYahoo.info['longName']
            updateStockTable = f"UPDATE \"STOCKS\" SET stock_name = \'{tickerName}\' where stock_symbol =\'{ticker}\';"
            print(updateStockTable)
            cursor.execute(updateStockTable)
            # conn.commit()
            # ticker_name = get_ticker_name(ticker)
            # print(f"The ticker name for {ticker} is: {tickerName}")
            conn.commit()
            tickers.remove(ticker)

        except Exception as e:
            conn.rollback()  # Roll back the transaction if an error occurs
            print(f"Error: {e}")
    return tickers

for i in range(1):
    tickers = ['MCO', 'ORLY']
    tickers = get_ticker_name(tickers)

cursor.close()
conn.close()

