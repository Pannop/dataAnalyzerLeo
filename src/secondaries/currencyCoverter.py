import requests
from secondaries import requestHeaders

currenciesNames = ['ARS', 'USD', 'AUD', 'EUR', 'RON', 'BRL', 'CAD', 'CLP', 'CNY', 'HKD', 'CZK', 'DKK', 'HUF', 'ISK', 'INR', 'IDR', 'ILA', 'JPY', 'KWF', 'MYR', 'MXN', 'NZD', 'NOK', 'PLN', 'QAR', 'SAR', 'SGD', 'ZAc', 'KRW', 'SEK', 'CHF', 'TWD', 'THB', 'TRY', 'GBp', 'ILS']


class CurrencyConverter:
    def __init__(self) -> None:
        self.currenciesConv = {}
        self.updateCurrenciesConversion()
        

    def updateCurrenciesConversion(self):
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

    def getUsdConversion(self, currency):
        return self.currenciesConv[currency]
    
