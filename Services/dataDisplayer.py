import json
from datetime import date


class displayData:
    def __init__(self, json_parser, postgres_api):
        self.json_parser = json_parser
        self.postgres_api = postgres_api

    # def fetch_and_process_data(self):
    def fetchData(self, stockTableName, startDate, endDate):
        # Fetch data from PostgreSQL
        # query = "SELECT * FROM \"STOCKS\" ;"
        displayQuery = f"SELECT trade_date, closing_price from \"{stockTableName}\" where trade_date >=\'{startDate}\' and trade_date <=\'{endDate}\';"
        postgresData = self.postgres_api.fetchDataFromDatabase(displayQuery)
        return postgresData
 
    
    def processData(self, pgRawData):
        
        processed_data = []
        for row in pgRawData:
            # Process each row, convert it to JSON
            # json_row = {'Stock Symbol': row[0], 'Stock Name': row[2], 'Stock Sector': row[1]}  
            # json_row = {'Data ID': row[0], 'Trade Date': row[1].isoformat(), 'Open Price': row[2], 'Closing Price': row[3], 'Day High': row[4], 'Day Low': row[5], 'Adj Price': row[6], 'Traded Voiume': row[7]}  
            json_row = {'Trade Date': row[0].isoformat(), 'Closing Price': row[1]}  
            processed_data.append(json_row)

        # Convert processed data to JSON
        json_data = self.json_parser.parse(json.dumps(processed_data))
        return json_data
    
