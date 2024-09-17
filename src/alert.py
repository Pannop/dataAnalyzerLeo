import pandas as pd
import eel
import time
import requests
import re
from datetime import datetime
from currencyCoverter import CurrencyConverter
from threading import Thread
from threadStopper import threadStop
import requestHeaders




def orderObjectListBy(list, column):
    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if(list[i][column] < list[j][column]):
                tmp = list[i]
                list[i] = list[j]
                list[j] = tmp


regionsNames = {'Belgium': 'be', 'Austria': 'at', 'Argentina': 'ar', 'Australia': 'au', 'Brazil': 'br', 'Switzerland': 'ch', 'Canada': 'ca', 'Chile': 'cl', 'China': 'cn', 'Germany': 'de', 'Estonia': 'ee', 'Czechia': 'cz', 'Denmark': 'dk', 'Egypt': 'eg', 'Finland': 'fi', 'United Kingdom': 'gb', 'Indonesia': 'id', 'France': 'fr', 'Spain': 'es', 'Greece': 'gr', 'Hong Kong SAR China': 'hk', 'Israel': 'il', 'Hungary': 'hu', 'Ireland': 'ie', 'New Zealand': 'nz', 'Mexico': 'mx', 'Philippines': 'ph', 'Poland': 'pl', 'Netherlands': 'nl', 'Qatar': 'qa', 'Saudi Arabia': 'sa', 'Singapore': 'sg', 'Norway': 'no', 'Malaysia': 'my', 'Latvia': 'lv', 'Pakistan': 'pk', 'Portugal': 'pt', 'Russia': 'ru', 'Sweden': 'se', 'Peru': 'pe', 'Lithuania': 'lt', 'Italy': 'it', 'Iceland': 'is', 'Japan': 'jp', 'Kuwait': 'kw', 'South Korea': 'kr', 'India': 'in', 'Sri Lanka': 'lk', 'Thailand': 'th', 'Suriname': 'sr', 'United States': 'us', 'Taiwan': 'tw', 'Venezuela': 've', 'South Africa': 'za', 'Vietnam': 'vn', 'Turkey': 'tr'}
regionsLoaded = []



def getYaMarketData(progressBarId, regions, caps, currencyConverter: CurrencyConverter):
    data = []
    name=None
    rCount = 0
    if(progressBarId):
        eel.setProgress(progressBarId, 0)
    
    capsConditions = [{"operator":"LT","operands":["intradaymarketcap",2000000000]},
                      {"operator":"BTWN","operands":["intradaymarketcap",2000000000,10000000000]},
                      {"operator":"BTWN","operands":["intradaymarketcap",10000000000,100000000000]},
                      {"operator":"GT","operands":["intradaymarketcap",100000000000]}]

    filteredCapsConditions = []
    for c in caps:
        if(c!=-1):
            filteredCapsConditions.append(capsConditions[c])
    for r in regions:
        for o in range(0, 10000, 250):
            reqList=[]
            retryNum=10
            for retry in range(retryNum):
                try:
                    payload = {"size":250,"offset":o,"sortField":"dayvolume","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"or","operands":[{"operator":"EQ","operands":["region", regionsNames[r]]}]},{"operator":"or","operands":filteredCapsConditions},{"operator":"gt","operands":["avgdailyvol3m",10]},{"operator":"gt","operands":["percentchange",0]},{"operator":"gt","operands":["dayvolume",10]}]},"userId":"","userIdType":"guid"}
                    req = requests.post(f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={requestHeaders.yahooCrumb}&lang=it-IT&region=IT&formatted=true&corsDomain=it.finance.yahoo.com", headers=requestHeaders.yahooScreenerHeader, json=payload).json()
                    reqList = req["finance"]["result"][0]["quotes"]
                    break
                except:
                    if(retry==retryNum-1):
                        raise ConnectionError
                    continue
            if(len(reqList)==0):
                break
            for d in reqList:
                try:
                    if d["averageDailyVolume3Month"]["raw"] > 0:
                        try:
                            name = d["shortName"]
                        except KeyError:
                            try:
                                name = d["longName"]
                            except KeyError:
                                name = d["symbol"]

                        data.append({"symbol":d["symbol"],
                                    "name":name,
                                    "region":r,
                                    "valueDeltaPerc":round(d["regularMarketChangePercent"]["raw"], 3), 
                                    "volume":d["regularMarketVolume"]["raw"], 
                                    "volumeAvg":d["averageDailyVolume3Month"]["raw"], 
                                    "volumeDeltaPerc":round((d["regularMarketVolume"]["raw"]-d["averageDailyVolume3Month"]["raw"])*100/d["averageDailyVolume3Month"]["raw"]), 
                                    "marketState":d["marketState"], 
                                    "volumePrice":round(d["regularMarketPreviousClose"]["raw"]*d["regularMarketVolume"]["raw"]*currencyConverter.getUsdConversion(d["currency"]))} )

                except KeyError:
                    pass
            total = req["finance"]["result"][0]["total"]
            if(progressBarId):
                eel.setProgress(progressBarId, (rCount*100)/len(regions) + o*(1/len(regions)*100)/total)
        rCount+=1
    if(progressBarId):
        eel.setProgress(progressBarId, 100)
    print(len(data))
    return data


class AlertListener(Thread):
    def __init__(self,num, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, refreshRate, currencyConverter : CurrencyConverter):
        Thread.__init__(self)
        self.stopped = False
        self.num=num
        self.volumePerc=volumePerc
        self.valuePerc=valuePerc
        self.minVolume=minVolume
        self.minVolumePrice=minVolumePrice
        self.regions=regions
        self.caps=caps
        self.refreshRate=refreshRate
        self.currencyConverter = currencyConverter
        self.oldSymbols = {}


    def run(self):
        while(not self.stopped and not threadStop.stop):
            try:
                alerts = getYaMarketData(None, self.regions, self.caps, self.currencyConverter)
                filteredAlerts = [d for d in alerts if d["volumeAvg"]>self.minVolume and 
                                            d["volumeDeltaPerc"]>=self.volumePerc and 
                                            d["valueDeltaPerc"]>=self.valuePerc and
                                            d["volumePrice"]>=self.minVolumePrice]
                
                symbolsUpdated = [a["symbol"] for a in filteredAlerts]
                notPresent = [a for a in self.oldSymbols if a not in  symbolsUpdated]
                
                for a in filteredAlerts:
                    if(a["symbol"] in self.oldSymbols):
                        a["time"] = self.oldSymbols[a["symbol"]]
                        a["new"] = 0
                    else:
                        a["time"] = datetime.now().time().replace(microsecond=0)
                        self.oldSymbols[a["symbol"]] = a["time"]
                        a["new"] = 1
                    a["deleted"] = 0

                for np in notPresent:
                    a = {"symbol":np, "time":self.oldSymbols[np], "deleted":1}
                    filteredAlerts.insert(0, a)

                orderObjectListBy(filteredAlerts, "time")

                for a in filteredAlerts:
                    a["time"] = str(a["time"])

                eel.applyAlertListenerTable(filteredAlerts, self.num)
            except ConnectionError:
                print("listener connection error")


            for t in range(self.refreshRate*60):
                time.sleep(1)
                if(threadStop.stop):
                    break
        



class AlertChecker:
    
    def __init__(self, currencyConverter : CurrencyConverter):
        self.data = None
        self.alerts = []
        self.regions=[]
        self.caps=[]
        self.currencyConverter = currencyConverter
        self.alertListeners = {}

    def getData(self, progressBarId):
        try:
            self.data = getYaMarketData(progressBarId, self.regions, self.caps, self.currencyConverter)

        except ConnectionError:
            print("alert connection error")



    def check(self, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, progressBarId, forceUpdateData = False):
        
        if(self.data==None or regions!=self.regions or caps!=self.caps  or forceUpdateData):
            self.regions = regions
            self.caps = caps
            self.getData(progressBarId)
        self.alerts = [d for d in self.data if d["volumeAvg"]>minVolume and 
                                                d["volumeDeltaPerc"]>=volumePerc and 
                                                d["valueDeltaPerc"]>=valuePerc and
                                                d["volumePrice"]>=minVolumePrice]
        orderObjectListBy(self.alerts, "volumeDeltaPerc")

    def addListener(self, num, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, refreshRate):
        al = AlertListener(num, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, refreshRate, self.currencyConverter)
        self.alertListeners[str(num)] = al
        al.start()

    def removeListener(self, num):
        self.alertListeners[str(num)].stopped = True
        del self.alertListeners[str(num)]

