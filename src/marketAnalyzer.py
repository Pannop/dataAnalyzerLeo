import datetime
import os
import requests
import pandas
import json
import numpy as np
import time
import math
import matplotlib as mp
import pandas as pd
from secondaries import requestHeaders
from marketAnalyzerCalculus import MarketMatrixCalculus


def getYaMarketData(symbol, lastDate, interval="1d", retryCount = 0):
    t = str(time.time()).split(".")[0]
    
    try:    
        req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1={lastDate}&period2={t}&useYfid=true&interval={interval}&includePrePost=true&events=div|split|earn&lang=it-IT&region=IT&crumb=bZtbC8282C3&corsDomain=it.finance.yahoo.com", headers=requestHeaders.yahooChartHeader)
    except:
        if(retryCount==100):
            raise ConnectionError()
        print("retrying")
        return getYaMarketData(symbol, lastDate, interval, retryCount+1)
    return req.json()




def getDeltas(x, y):
    deltas = []
    dayStep=1
    for i in range(1, len(x)):
        if(x[i] and y[i] and x[i-dayStep] and y[i-dayStep]):
            deltas.append({"time":str(datetime.date.fromtimestamp(x[i])), "timestamp":x[i], "deltaPerc":round((y[i]-y[i-dayStep])/y[i-dayStep], 7),"delta":(y[i]-y[i-dayStep]),"log": np.log(abs(y[i]/y[i-dayStep])), "value":y[i]})
    
            #time.sleep(0.1)

    return deltas

def calculateYaDelta(data):
    
    x=data["chart"]["result"][0]["timestamp"]

    yAdj=data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    yNor=data["chart"]["result"][0]["indicators"]["quote"][0]    
    return {"open":getDeltas(x, yNor["open"]),
            "close":getDeltas(x, yNor["close"]),
            "adjclose":getDeltas(x, yAdj),
            "volume":getDeltas(x, yNor["volume"])}
    


def listsIntersection(lists):
    if(len(lists)>0):
        inter = set(lists[0])
        for i in range(1, len(lists)):
            inter = inter.intersection(set(lists[i]))
        return list(inter)
    else:
        return []

class MarketMatrix(MarketMatrixCalculus):

    def __init__(self, marketList, indexName, cacheFile):
        self.marketList = marketList
        #mat = [[0.]*len(marketList)]*len(marketList)
        #mat = [[0.]*len(marketList) for n in range(len(marketList))]
        #lst = [0.]*len(marketList)
        self.correlationMarketMatrix = np.array([[0.]*len(marketList) for n in range(len(marketList))])
        self.betaMarketMatrix = np.array([[0.]*len(marketList) for n in range(len(marketList))])
        self.correlationIndexList = np.array([0.]*len(marketList))
        self.betaIndexList = np.array([0.]*len(marketList))
        self.marketData = {}
        self.indexData = {}
        self.corrispondences=[]
        self.indexName = indexName
        self.CORRISPONDECE_THRESHOLD = 0.6
        self.cacheFile = cacheFile


    def setData(self, data, title, interval, unit):
        d=data
        lastDate=0
        cache=None
        if(title!=self.indexName):
            d=data[title]
        try:
            if(title!=self.indexName):
                lastDate=self.cache["market"][title][interval]["open"][-1]["timestamp"]
                cache=self.cache["market"][title][interval]
            else:
                lastDate=self.cache["index"][interval]["open"][-1]["timestamp"]
                cache=self.cache["index"][interval]
        except:
            pass
        newData = calculateYaDelta(getYaMarketData(title, lastDate, unit))
        if(cache):
            for x in newData:
                newData[x] = cache[x]+newData[x]
        d[interval] = newData

        
    def loadMarketData(self, fromYear=0, dayStep=1):
        for m in self.marketList:
            print(f'getting {m}')
            self.marketData[m] = {}
            self.setData(self.marketData, m, "d", "1d")
            self.setData(self.marketData, m, "wk", "1wk")
            self.setData(self.marketData, m, "mo", "1mo")
            #self.marketData[m]["d"] = calculateYaDelta(getYaMarketData(m, 0, "1d"), fromYear, dayStep)
            #self.marketData[m]["wk"] = calculateYaDelta(getYaMarketData(m,0, "1wk"), fromYear, dayStep)
            #self.marketData[m]["mo"] = calculateYaDelta(getYaMarketData(m,0, "1mo"), fromYear, dayStep)

    def loadIndexData(self, fromYear=0, dayStep=1):
        self.setData(self.indexData, self.indexName, "d", "1d")
        self.setData(self.indexData, self.indexName, "wk", "1wk")
        self.setData(self.indexData, self.indexName, "mo", "1mo")
        #self.indexData["d"] = calculateYaDelta(getYaMarketData(self.indexName,0, "1d"), fromYear, dayStep)
        #self.indexData["wk"] = calculateYaDelta(getYaMarketData(self.indexName,0, "1wk"), fromYear, dayStep)
        #self.indexData["mo"] = calculateYaDelta(getYaMarketData(self.indexName,0, "1mo"), fromYear, dayStep)

            
            

    def loadData(self, fromYear=0, dayStep=1, loadOnlyCache=False):
        if((self.cache==None or self.cache["date"]!=str(datetime.date.today()) or self.cache["indexName"]!=self.indexName or self.cache["marketList"]!=self.marketList) and not loadOnlyCache):
            cache={"date":str(datetime.date.today())}
            try:
                self.loadMarketData(fromYear,dayStep)
                self.loadIndexData(fromYear,dayStep)
                cache["index"]=self.indexData
                cache["market"]=self.marketData
                cache["indexName"]=self.indexName
                cache["marketList"]=self.marketList
                self.cache = cache
                return
            except ConnectionError:
                print("Connection Error: using cache")
                
        self.indexData = self.cache["index"]
        self.marketData = self.cache["market"]  

        
    def calculateAllData(self):
        self.calculateMarketCorrelation()
        self.calculateMarketBetas()
        self.calculateIndexCorrelation()
        self.calculateIndexBetas()
        self.createCorrispondences()

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
            file = open(self.cacheFile, "w")
            file.write(json.dumps(self.cache))
            file.close()
                
    def getMarketsData(self, markets, fromDate, toDate, interval, type):
        data = {}
        fromDateTimeStamp = datetime.datetime.strptime(fromDate, "%Y-%m-%d").timestamp()
        toDateTimeStamp = datetime.datetime.strptime(toDate, "%Y-%m-%d").timestamp()
        for m in markets:
            if(m==self.indexName):
                data[m] = [d for d in self.indexData[interval][type] if int(d["timestamp"])>=fromDateTimeStamp and int(d["timestamp"])<=toDateTimeStamp]
            else:
                data[m] = [d for d in self.marketData[m][interval][type] if int(d["timestamp"])>=fromDateTimeStamp and int(d["timestamp"])<=toDateTimeStamp]
        
        totalTimestamps = []
        for m in markets:
            totalTimestamps.append([d["time"] for d in data[m]])
        commonsTimestamps = listsIntersection(totalTimestamps)
        for m in markets:
            data[m] = [d for d in data[m] if d["time"] in commonsTimestamps]
        return data

        