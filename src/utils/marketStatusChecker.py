from threading import Thread
import time
import requests
from secondaries import requestHeaders
from secondaries.threadStopper import threadStop

regionsNames = {'Belgium': 'be', 'Austria': 'at', 'Argentina': 'ar', 'Australia': 'au', 'Brazil': 'br', 'Switzerland': 'ch', 'Canada': 'ca', 'Chile': 'cl', 'China': 'cn', 'Germany': 'de', 'Estonia': 'ee', 'Czechia': 'cz', 'Denmark': 'dk', 'Egypt': 'eg', 'Finland': 'fi', 'United Kingdom': 'gb', 'Indonesia': 'id', 'France': 'fr', 'Spain': 'es', 'Greece': 'gr', 'Hong Kong SAR China': 'hk', 'Israel': 'il', 'Hungary': 'hu', 'Ireland': 'ie', 'New Zealand': 'nz', 'Mexico': 'mx', 'Philippines': 'ph', 'Poland': 'pl', 'Netherlands': 'nl', 'Qatar': 'qa', 'Saudi Arabia': 'sa', 'Singapore': 'sg', 'Norway': 'no', 'Malaysia': 'my', 'Latvia': 'lv', 'Pakistan': 'pk', 'Portugal': 'pt', 'Russia': 'ru', 'Sweden': 'se', 'Peru': 'pe', 'Lithuania': 'lt', 'Italy': 'it', 'Iceland': 'is', 'Japan': 'jp', 'Kuwait': 'kw', 'South Korea': 'kr', 'India': 'in', 'Sri Lanka': 'lk', 'Thailand': 'th', 'Suriname': 'sr', 'United States': 'us', 'Taiwan': 'tw', 'Venezuela': 've', 'South Africa': 'za', 'Vietnam': 'vn', 'Turkey': 'tr'}
regionsRealTime = [{'country': 'Australia', 'suffix': '.XA'}, {'country': 'Canada', 'suffix': '.CN'}, {'country': 'Canada', 'suffix': '.NE'}, {'country': 'Canada', 'suffix': '.TO'}, {'country': 'Canada', 'suffix': '.V'}, {'country': 'Denmark', 'suffix': '.CO'}, {'country': 'Estonia', 'suffix': '.TL'}, {'country': 'Europe', 'suffix': '.XD'}, {'country': 'Finland', 'suffix': '.HE'}, {'country': 'Global', 'suffix': '.REGA'}, {'country': 'Global', 'suffix': '=X'}, {'country': 'Iceland', 'suffix': '.IC'}, {'country': 'India', 'suffix': '.NS'}, {'country': 'Latvia', 'suffix': '.RG'}, {'country': 'Lithuania', 'suffix': '.VS'}, {'country': 'Sweden', 'suffix': '.ST'}, {'country': 'United Kingdom', 'suffix': '.XC'}]


class MarketStatusChecker(Thread):
    def __init__(self, updateTime):
        Thread.__init__(self)
        self.updateTime = updateTime
        self.stopped=False
        self.ready=False
        self.marketStatus = {reg:{"open":"NOT_INIT", "realtime":False} for reg in regionsNames}

    def getMarketStatus(self):
        return self.marketStatus
    
    def getRealtimeSuffixes(self):
        return [r["suffix"] for r in regionsRealTime]

    def isReady(self):
        return self.ready

    def run(self):
        for r in regionsNames:
            self.marketStatus[r]["realtime"] = len([realTime for realTime in regionsRealTime if realTime["country"]==r])>0
        while(not self.stopped and not threadStop.stop):
            for r in regionsNames:
                payload = {"size":1,"offset":0,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"or","operands":[{"operator":"EQ","operands":["region", regionsNames[r]]}]}]},"userId":"","userIdType":"guid"}
                retries=0
                while(retries<10):
                    try:
                        req = requests.post(f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={requestHeaders.yahooCrumb}&lang=it-IT&region=IT&formatted=true&corsDomain=it.finance.yahoo.com", headers=requestHeaders.yahooScreenerHeader, json=payload)
                    except:
                        time.sleep(5)
                        retries+=1
                        continue
                    break
                if(retries==10):
                    print("error retrieving status data")
                data = req.json()
                self.marketStatus[r]["open"] = (data["finance"]["result"][0]["count"]>0 and data["finance"]["result"][0]["quotes"][0]["marketState"] == "REGULAR")
            self.ready = True
            for t in range(self.updateTime):
                time.sleep(1)
                if(threadStop.stop):
                    break