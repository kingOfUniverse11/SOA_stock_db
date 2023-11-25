import os
import pandas as pd
import yfinance as yf

# Function to download historical data for each S&P 500 company
def download_sp500_data(startYear, endYear, folder_path):
    # List of S&P 500 tickers
    # tickers = yf.download('^GSPC', start=startYear, end=endYear).index
    
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500_df = table[0]
    tickers = sp500_df['Symbol'].tolist()
    tickerCategory = sp500_df.set_index('Symbol')['GICS Sector'].to_dict()
    # TODO need to add the company name too. fetch it using this and then get the name from a diff table acc to symbol

    # Creating the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    # tickers = ['AAPL'] 
    # Download data for each ticker
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=startYear, end=endYear)
            if not data.empty:
                outputFileName = f"{folder_path}/{ticker}.csv"
                data.to_csv(outputFileName)
                csv_input = pd.read_csv(outputFileName)
                csv_input['GICS Sector'] = tickerCategory[ticker]
                csv_input.to_csv(outputFileName, index=False)

                print(f"Downloaded {ticker} data.")
            else:
                print(f"No data available for {ticker}.")
        except Exception as e:
            print(f"Failed to download {ticker}: {e}")

# Define the folder path on the desktop to save the data
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "SP500_Historical_Data")

# Define the date range
startYear = '2015-01-01'
endYear = '2020-12-31'

# Call the function to download data
download_sp500_data(startYear, endYear, folder_path)