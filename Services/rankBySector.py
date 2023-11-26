import json
from datetime import date


class rankingBySector:
    def __init__(self, json_parser, postgres_api):
        self.json_parser = json_parser
        self.postgres_api = postgres_api

    # def fetch_and_process_data(self):
    def getSectors(self, sectorName):
        getSectors = f"SELECT stock_symbol, stock_name from \"STOCKS\" where stock_gics_sector = \'{sectorName}\' ;"
        companies = self.postgres_api.fetchDataFromDatabase(getSectors)
        return companies 
    
    
    def processCompaniesData(self, pgRawData):
        processed_data = []
        for row in pgRawData:
            # Process each row, convert it to JSON
            json_row = {'Stock Symbol': row[0], 'Stock Name': row[1]}  
            processed_data.append(json_row)

        # Convert processed data to JSON
        json_data = self.json_parser.parse(json.dumps(processed_data))
        return json_data
    
    def getIndividualCompanyData(self, companiesJsonData, startDate, endDate):
        # Fetch data from PostgreSQL
        individualDataDict = {}
        for row in companiesJsonData:
            stockSymbol = row['Stock Symbol']
            stockName = row['Stock Name']
            individualCompanyData = f"Select trade_date, closing_price from \"{row['Stock Symbol']}\" where trade_date >=\'{startDate}\' and trade_date <=\'{endDate}\';"
            postgresData = self.postgres_api.fetchDataFromDatabase(individualCompanyData)
            if len(postgresData)!=0:
                firstDataRow = postgresData[0]
                lastDataRow = postgresData[-1]
                performance = ((lastDataRow[1]-firstDataRow[1])/firstDataRow[1])*100
                individualDataDict[stockSymbol] = (stockName, performance)
            
            
            #sorting the dictionary 
            individualDataDictSorted = dict(sorted(individualDataDict.items(), key=lambda item: item[1][1], reverse = True))
                    
        return individualDataDictSorted
     
    
