import json
from datetime import date


class pastYields:
    def __init__(self, json_parser, postgres_api):
        self.json_parser = json_parser
        self.postgres_api = postgres_api

    # def fetch_and_process_data(self):
    def fetchData(self, stockTableName, startDate, endDate):
        # Fetch data from PostgreSQL
        # query = "SELECT * FROM \"STOCKS\" ;"
        yieldQuery = f"SELECT trade_date, closing_price from \"{stockTableName}\" where trade_date >=\'{startDate}\' and trade_date <=\'{endDate}\';"
        postgresData = self.postgres_api.fetchDataFromDatabase(yieldQuery)
        return postgresData
 
    
    def processData(self, pgRawData):
        
        processed_data = []
        for row in pgRawData:
            # Process each row, convert it to JSON
            # json_row = {'Stock Symbol': row[0], 'Stock Name': row[2], 'Stock Sector': row[1]}  
            json_row = {'Trade Date': row[0].isoformat(), 'Closing Price': row[1]}  
            processed_data.append(json_row)

        # Convert processed data to JSON
        json_data = self.json_parser.parse(json.dumps(processed_data))
        return json_data
    
    def calculateYield(self, initialValue, finalValue):        
        yieldPercent = ((finalValue['Closing Price']-initialValue['Closing Price'])/initialValue['Closing Price'])*100
        return yieldPercent
