import requests
from secondaries import requestHeaders

currenciesNames = ['ARS', 'USD', 'AUD', 'EUR', 'RON', 'BRL', 'CAD', 'CLP', 'CNY', 'HKD', 'CZK', 'DKK', 'HUF', 'ISK', 'INR', 'IDR', 'ILA', 'JPY', 'KWF', 'MYR', 'MXN', 'NZD', 'NOK', 'PLN', 'QAR', 'SAR', 'SGD', 'ZAc', 'KRW', 'SEK', 'CHF', 'TWD', 'THB', 'TRY', 'GBp', 'ILS']


class CurrencyConverter:
    def __init__(self) -> None:
        self.currenciesConv = {}
        

    def updateCurrenciesConversionOld(self):
        print("getting currencies conversion")
        for c in currenciesNames:
            if(c=="USD"):
                self.currenciesConv[c] = 1
            else:
                symbol=f"{c}USD=X"
                if(c=="ILA"):
                    symbol="ILA-USD"
                if(c=="KWF"):
                    symbol="KWDUSD=X"
                req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d", headers=requestHeaders.yahooChartHeader)
                self.currenciesConv[c] = req.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        print("done")

    def updateCurrenciesConversion(self):
        print("getting currencies conversion")
        symbolsList = [c+"USD=X" for c in currenciesNames]
        symbolsList[symbolsList.index("ILAUSD=X")] = "ILA-USD"
        symbolsList[symbolsList.index("KWFUSD=X")] = "KWDUSD=X"
        symbols = ",".join(symbolsList)
        req = requests.get(f"https://query1.finance.yahoo.com/v7/finance/quote?fields=regularMarketPrice&formatted=true&symbols={symbols}&crumb={requestHeaders.yahooCrumb}", headers=requestHeaders.yahooChartHeader)
        reqJson = req.json()
        for i in range(len(currenciesNames)):
            self.currenciesConv[currenciesNames[i]] = reqJson["quoteResponse"]["result"][i]["regularMarketPrice"]["raw"]
        print("done")

    def getUsdConversion(self, currency):
        return self.currenciesConv[currency]
    
    def setCurrencyConversion(self, currencyConversion):
        self.currenciesConv = currencyConversion

    def getCurrencyConversion(self):
        return self.currenciesConv

