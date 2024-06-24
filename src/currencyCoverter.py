import requests

requestHeader = {
    "Host": "query1.finance.yahoo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",    "Upgrade-Insecure-Requests": "1",
    "Cookie": "A3=d=AQABBFqE5l8CEL7R-eecHzVTxCatVIRtRikFEgABCAGDemasZudVb2UB9qMAAAcIWoTmX4RtRik&S=AQAAAvarvbzeS7_rPOIchc_8ygw; A1=d=AQABBFqE5l8CEL7R-eecHzVTxCatVIRtRikFEgABCAGDemasZudVb2UB9qMAAAcIWoTmX4RtRik&S=AQAAAvarvbzeS7_rPOIchc_8ygw; GUC=AQABCAFmeoNmrEIhWAS0&s=AQAAAKqeFOvd&g=Znk0ww; cmp=t=1719219388&j=1&u=1---&v=31; PRF=t%3DSD%252B%255EDJI%252B%255EIXIC%252BCL%253DF; A1S=d=AQABBFqE5l8CEL7R-eecHzVTxCatVIRtRikFEgABCAGDemasZudVb2UB9qMAAAcIWoTmX4RtRik&S=AQAAAvarvbzeS7_rPOIchc_8ygw; GUCS=ASmcRCXb; EuConsent=CP9oCIAP9oCIAAOACBITA5EoAP_gAEPgACiQJhNB9G7WTXFneXp2YPskOYUX0VBJ4MAwBgCBAcABzBIUIAwGVmAzJEyIICACGAIAIGJBIABtGAhAQEAAYIAFAABIAEEAABAAIGAAACAAAABACAAAAAAAAAAQgEAXMBQgmAZEAFoIQUhAhgAgAQAAAAAEAIgBAgQAEAAAQAAICAAIACgAAgAAAAAAAAAEAFAIEQAAAAECAotkfQTBADINSogCLAkJCAQMIIEAIgoCACgQAAAAECAAAAmCAoQBgEqMBEAIAQAAAAAAAAQEACAAACABCAAIAAgQAAAAAQAAAAACAAAEAAAAAAAAAAAAAAAAAAAAAAAAAMQAhBAACAACAAgoAAAABAAAAAAAAAARAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAQAAAAAAAABAAILAAA",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "domain-id": "it"}

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
                req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d", headers=requestHeader)
                self.currenciesConv[c] = req.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]

        print("done")

    def getUsdConversion(self, currency):
        return self.currenciesConv[currency]
    
