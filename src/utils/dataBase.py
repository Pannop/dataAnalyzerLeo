import os
import json
import datetime
import time
from secondaries import requestHeaders
from secondaries.currencyCoverter import CurrencyConverter
from marketAnalyzer import MarketMatrix
import requests
import numpy as np
import traceback
import eel

regionsNames = {'Belgium': 'be', 'Austria': 'at', 'Argentina': 'ar', 'Australia': 'au', 'Brazil': 'br', 'Switzerland': 'ch', 'Canada': 'ca', 'Chile': 'cl', 'China': 'cn', 'Germany': 'de', 'Estonia': 'ee', 'Czechia': 'cz', 'Denmark': 'dk', 'Egypt': 'eg', 'Finland': 'fi', 'United Kingdom': 'gb', 'Indonesia': 'id', 'France': 'fr', 'Spain': 'es', 'Greece': 'gr', 'Hong Kong SAR China': 'hk', 'Israel': 'il', 'Hungary': 'hu', 'Ireland': 'ie', 'New Zealand': 'nz', 'Mexico': 'mx', 'Philippines': 'ph', 'Poland': 'pl', 'Netherlands': 'nl', 'Qatar': 'qa', 'Saudi Arabia': 'sa', 'Singapore': 'sg', 'Norway': 'no', 'Malaysia': 'my', 'Latvia': 'lv', 'Pakistan': 'pk', 'Portugal': 'pt', 'Russia': 'ru', 'Sweden': 'se', 'Peru': 'pe', 'Lithuania': 'lt', 'Italy': 'it', 'Iceland': 'is', 'Japan': 'jp', 'Kuwait': 'kw', 'South Korea': 'kr', 'India': 'in', 'Sri Lanka': 'lk', 'Thailand': 'th', 'Suriname': 'sr', 'United States': 'us', 'Taiwan': 'tw', 'Venezuela': 've', 'South Africa': 'za', 'Vietnam': 'vn', 'Turkey': 'tr'}

def getYaWorldLatestData(regions, caps, currencyConverter: CurrencyConverter, progressBarId=None):
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



def getYaMarketData(symbol, lastDate, interval="1d", retryCount = 0):
    t = str(time.time()).split(".")[0]
    try:    
        req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1={lastDate}&period2={t}&useYfid=true&interval={interval}&includePrePost=true&events=div|split|earn&lang=it-IT&region=IT&crumb=bZtbC8282C3&corsDomain=it.finance.yahoo.com", headers=requestHeaders.yahooChartHeader)
    except:
        if(retryCount==100):
            raise ConnectionError()
        print("retrying")
        return getYaMarketData(symbol, lastDate, interval, retryCount+1)
    reqJson = req.json()
    firstTimestamp = -1
    try:
        firstTimestamp = reqJson["chart"]["result"][0]["timestamp"][0]
    except:
        pass
    return reqJson, firstTimestamp




def getDeltas(x, y, previousValue):

    def findFirstNonZeroValue(data, i):
        for j in range(i, len(data)):
            if(data[j]!=0):
                return data[j]
        return 0.0001
    
    deltas = []
    dayStep=1
    try:
            if(previousValue!=None):
                x = [0]+x
                y = [previousValue]+y
            y = [d if d!=None else 0 for d in y]
            y[0] = findFirstNonZeroValue(y, 0)
            for i in range(1, len(x)):
                if(y[i]==0):
                    y[i] = (y[i-1] if y[i-1]!=0 else findFirstNonZeroValue(y, i))
                
                deltas.append({"time":str(datetime.date.fromtimestamp(x[i])), "timestamp":x[i], "deltaPerc":round((y[i]-y[i-dayStep])/y[i-dayStep], 7),"delta":(y[i]-y[i-dayStep]),"log": np.log(abs(y[i]/y[i-dayStep])), "value":y[i]})
    
    except:
        traceback.print_exc() 
        print(x)
        print(y)
        os.system("pause > nul")
    return deltas

def calculateYaDelta(data, previousCache):
    
    x=data["chart"]["result"][0]["timestamp"]

    yAdj=data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    yNor=data["chart"]["result"][0]["indicators"]["quote"][0]
    
    def getCacheLastValue(type):
        return (previousCache[type][-1]["value"] if previousCache!=None else None)

    return {"open":getDeltas(x, yNor["open"], getCacheLastValue("open")),
            "close":getDeltas(x, yNor["close"], getCacheLastValue("close")),
            "adjclose":getDeltas(x, yAdj, getCacheLastValue("adjclose")),
            "volume":getDeltas(x, yNor["volume"], getCacheLastValue("volume"))}
    


class DataBase:
    
    def __init__(self, cacheFile, configFile, currencyConverter:CurrencyConverter):
        self.cacheFile = cacheFile
        self.configFile = configFile
        self.cache = None
        self.marketList = []
        self.indexList = []
        self.marketData = {}
        self.currencyConverter = currencyConverter
        self.marketMatrixDict = {}

    def start(self):
        self.loadConfig()
        self.loadCache()
        self.loadData()
        self.saveCache()

    def loadMarketData(self, m, intervalToLoad=["d", "wk", "mo"]):
        self.marketData[m] = {}
        if("d" in intervalToLoad):
            self.setData(self.marketData, m, "d", "1d")
        if("wk" in intervalToLoad):
            self.setData(self.marketData, m, "wk", "1wk")
        if("mo" in intervalToLoad):
            self.setData(self.marketData, m, "mo", "1mo")


    def loadMarketsData(self):
        for m in self.marketList:
            print(f'getting {m}')
            self.loadMarketData(m)
            

    def loadData(self, loadOnlyCache=False):
        indexList=[]
        marketList=[]
        self.marketMatrixDict = {}
        dashboards = self.config["dashboards"]
        for dash in dashboards:
            for title in dashboards[dash]["titles"]:
                indexList.append(dashboards[dash]["titles"][title]["index"])
                marketList.append(title)
        indexList = list(set(indexList))
        marketList = list(set(marketList+indexList))
        marketList.sort()
        self.marketList = marketList
        if((self.cache==None or self.cache["date"]!=str(datetime.date.today()) or "currencyConverter" not in self.cache) and not loadOnlyCache):
            cache={"date":str(datetime.date.today())}
            try:
                self.loadMarketsData()
                cache["market"]=self.marketData
                self.currencyConverter.updateCurrenciesConversion()
                cache["currencyConverter"]=self.currencyConverter.getCurrencyConversion()
                self.cache = cache
            except ConnectionError:
                print("Connection Error: using cache")
                
        self.marketData = self.cache["market"]
        self.currencyConverter.setCurrencyConversion(self.cache["currencyConverter"])
        for dash in dashboards:
            self.marketMatrixDict[dash] = MarketMatrix(self.marketData, dashboards[dash], self)
        

    def setData(self, data, title, interval, unit):
        lastDate=0
        cache=None
        d=data[title]
        backInTimeReload = 2

        try:
            cache=self.cache["market"][title][interval]
            for type in cache:
                del cache[type][-backInTimeReload:]
            lastDate = cache["open"][-1]["timestamp"]


        except:
            #print("Exception retriving cache for ", title, interval)
            #traceback.print_exc() 
            lastDate = 0
        
        
        newRawData, firstNewDate = getYaMarketData(title, lastDate, unit)
        
        previousCache = cache
        if(firstNewDate==lastDate):
            previousCache = None
        newData = calculateYaDelta(newRawData, previousCache)

        if(cache):
            for x in newData:
                if (len(newData[x])>0):
                    newData[x] = cache[x]+newData[x][(1 if newData[x][0]["timestamp"]==lastDate else 0):]
                else:
                    newData[x] = cache[x]
        d[interval] = newData


        

    def loadConfig(self):
        if(os.path.isfile(self.configFile)):
            file = open(self.configFile, "r")
            data = json.loads(file.read())
            file.close()
            self.config=data
        else:
            self.config=None
        
    def saveConfig(self):
        if(self.config!=None):
            file = open(self.configFile, "w")
            file.write(json.dumps(self.config))
            file.close()

    def loadCache(self):
        if(os.path.isfile(self.cacheFile)):
            file = open(self.cacheFile, "r")
            data = json.loads(file.read())
            file.close()
            self.cache=data

        else:
            self.cache=None
        
    def saveCache(self):
        if(self.cache!=None):
            with open(self.cacheFile, "w") as file:
                file.write(json.dumps(self.cache))

    def getMarketMatrix(self, dashboard):
        return self.marketMatrixDict[dashboard]
    
    def getWorldLatestData(self, regions, caps, progressBarId):
        return getYaWorldLatestData(regions, caps, self.currencyConverter, progressBarId)


                