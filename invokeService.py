from Postgres.PostgresAPI import PostgresAPI
from JsonDataParser.JSONParser import JSONParser
from Services.pastYields import pastYields
from Services.dataDisplayer import displayData
from Services.rankBySector import rankingBySector

# Instantiate the classes
class invokeService:
    def __init__(self, jsonParser, pgAPI) -> None:
            self.jParser = jsonParser
            self.pgAPI = pgAPI
            
    def pastYields(self, stockSymbol, startDate, endDate):
        pastYield = pastYields(self.jParser, self.pgAPI)
        # Fetch and process data
        pgData = pastYield.fetchData(stockSymbol,startDate, endDate)
        jsonData = pastYield.processData(pgData) #this data can be used to plot the graph
        if(len(jsonData)==0):
            return None
        else:
            yieldPercent = pastYield.calculateYield(jsonData[0], jsonData[-1]) 
            # print(f"{yieldPercent}%")
            return yieldPercent
        
    def displayingData(self, stockSymbol, startDate, endDate):
        dataDisplay = displayData(self.jParser, self.pgAPI)
        pgData = dataDisplay.fetchData(stockSymbol, startDate, endDate)
        jsonData = dataDisplay.processData(pgData)
        if(len(jsonData)==0):
            return None
        else:
            return jsonData
        
            
    def rankingBySector(self, ticker, sectorName, startDate, endDate):
        rankSector = rankingBySector(self.jParser, self.pgAPI)
        companiesDataTuple = rankSector.getSectors(sectorName)
        companiesDataJson = rankSector.processCompaniesData(companiesDataTuple)
        if len(companiesDataJson)==0:
            return None
        else:
            companiesDataDict = rankSector.getIndividualCompanyData(companiesDataJson, startDate, endDate)
            inputtedTickerIndex = list(companiesDataDict).index(ticker)
            firstFiveDictItems = list(companiesDataDict.items())[:5]
            # print(inputtedTickerIndex)
            # print(f'\n{firstFiveDictItems}')
            return (inputtedTickerIndex, firstFiveDictItems)
                    


if __name__ == "__main__":
    jParser = JSONParser()
    pgAPI = PostgresAPI()
    service = invokeService(jParser, pgAPI)

    #add a way to invoke services depending on user choice
    yieldResult = invokeService.pastYields(service, 'AAPL', '2015-01-01', '2015-12-25') #take these as inputs
    displayDataresult = invokeService.displayingData(service, 'AAPL', '2015-01-01', '2015-12-25') #take these as inputs
    tickerLocation, top5 = invokeService.rankingBySector(service, 'AAPL', 'Information Technology', '2015-01-01', '2015-12-25') #take these as inputs

    
    