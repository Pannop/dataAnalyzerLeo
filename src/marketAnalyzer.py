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
AV_KEY = "NPRZ3R6XPBJWSA26"



def getUSMarketData(func, symbol, additional):
    req = requests.get(f'https://www.alphavantage.co/query?function={func}&symbol={symbol}&apikey={AV_KEY}&{additional}')
    return req.json()

def getBIMarketData(symbol):
    req = requests.get(f"https://live.euronext.com/en/instrumentSearch/searchJSON?q={symbol}")
    response = req.json()
    if(len(response)==1):
        isin = symbol
        mic = "SEDX"
    else:
        isin = response[0]["isin"]
        mic = response[0]["mic"]
    req = requests.get(f"https://live.euronext.com/intraday_chart/getChartData/{isin}-{mic}/max")
    return req.json()


def getYaMarketData(symbol,interval="1d", retryCount = 0):
    t = str(time.time()).split(".")[0]
    header = {
    "Host": "query1.finance.yahoo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",    "Upgrade-Insecure-Requests": "1",
    "Cookie": "A3=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY; A1=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY; GUC=AQAACAFl8e1mIkIfJgSt&s=AQAAAFcXkJ1O&g=ZfCm1w; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiUFNESzVNTjRYN0xWRjVVMzJTR1AzNTVDV1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiIxZXBNbkMyMWhmbjkifX0.uVZ1PMsWmbl8EBrsCYaDa1xpFQdlInXecdyUqAPaQNSxro9447GvRX97Yonc7Dk2usPwT8ygXpQuQhDiYl8Tj0Fu5OCNuo_JoVEoyfV7GrlYm3-yM2oxWjicO53qWfPHeE050D2H4AfFw_lASAagpoHuN2eTlEj7SG14EL2mMpU; T=af=JnRzPTE3MTAyNzAxNDMmcHM9MzZyNnBoSmhoXzUwRFN0aWdJQlVtUS0t&d=bnMBeWFob28BZwFQU0RLNU1ONFg3TFZGNVUzMlNHUDM1NUNXWQFhYwFBTVlSdDZGcgFhbAFhbmRlcmxpbmlsZW9uYXJkbzIwMjBAZ21haWwuY29tAXNjAW1icl9sb2dpbgFmcwFIZzZyanJCbDhLYW8BenoBL2FLOGxCQTdFAWEBUUFFAWxhdAEvYUs4bEIBbnUBMA--&kt=EAAsGitdcakPGbY7irhMab_UQ--~I&ku=FAAorceeKNG.dFwPvHECfavzXuPQWkdaBpQrGQlQKgb8SimM0JGDaieeHi_4t1nV.fzzq4dXhPHXjZ9b6mlU7ApxAA.EAq.SjisF.ObYlJilkAQ24C9eFlOj8CRU2q8ldx_LzyVSK26Rvg8VTg1GC7oynUiGXYYlAbBZO5rxS_xYyE-~E; F=d=GzmZX_s9vJVWdy9AtP9WyR.sUT1t94C_KyfMZQucvctigjhhRz0cVK51Ud2PxXG1vMy7; PH=l=it-IT; Y=v=1&n=5sggjh94ph61e&l=ix0gc8w961a6944l5hmwm6n5uhk3m0bke9pgsmhn/o&p=n38vvit00000000&r=1d5&intl=it; cmp=t=1711488666&j=1&u=1---&v=19; PRF=t%3DFTSEMIB.MI%252BAAPL%26newChartbetateaser%3D0%252C1711488327445; A1S=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "domain-id": "it"}
    try:    
        req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1=0&period2={t}&useYfid=true&interval={interval}&includePrePost=true&events=div|split|earn&lang=it-IT&region=IT&crumb=bZtbC8282C3&corsDomain=it.finance.yahoo.com", headers=header)
    except:
        if(retryCount==100):
            raise ConnectionError()
        print("retrying")
        return getYaMarketData(symbol, interval, retryCount+1)
    return req.json()

def calculateBIDelta(data, fromYear=0, dayStep=1):
    deltas = []
    for i in range(dayStep, len(data), dayStep):
        if(int(data[i]["time"][:4])>=fromYear):
            deltas.append({"time":data[i]["time"], "deltaPerc":round((data[i]["price"]-data[i-dayStep]["price"])/data[i-dayStep]["price"], 7),"delta":(data[i]["price"]-data[i-dayStep]["price"]), "value":data[i]["price"]})
    return deltas


def getDeltas(x, y):
        deltas = []
        dayStep=1
        for i in range(len(x)):
            if(x[i] and y[i] and x[i-dayStep] and y[i-dayStep]):
                deltas.append({"time":str(datetime.date.fromtimestamp(x[i])), "timestamp":x[i], "deltaPerc":round((y[i]-y[i-dayStep])/y[i-dayStep], 7),"delta":(y[i]-y[i-dayStep]),"log": np.log(abs(y[i]/y[i-dayStep])), "value":y[i]})
      
                #time.sleep(0.1)

        return deltas

def calculateYaDelta(data, fromYear=0, dayStep=1):
    
    x=data["chart"]["result"][0]["timestamp"]

    yAdj=data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    yNor=data["chart"]["result"][0]["indicators"]["quote"][0]
    
    return {"open":getDeltas(x, yNor["open"]),
            "close":getDeltas(x, yNor["close"]),
            "adjclose":getDeltas(x, yAdj)}
    




def summt(d0, a0, d1, a1):
        s=0
        for i in range(len(d0)):
            s+=(d0[i]-a0)*(d1[i]-a1)
        return s

def listsIntersection(lists):
    if(len(lists)>0):
        inter = set(lists[0])
        for i in range(1, len(lists)):
            inter = inter.intersection(set(lists[i]))
        return list(inter)
    else:
        return []

class MarketMatrix:

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

        
    def loadMarketData(self, fromYear=0, dayStep=1):
        for m in self.marketList:
            print(f'getting {m}')
            self.marketData[m] = {}
            self.marketData[m]["d"] = calculateYaDelta(getYaMarketData(m, "1d"), fromYear, dayStep)
            self.marketData[m]["wk"] = calculateYaDelta(getYaMarketData(m, "1wk"), fromYear, dayStep)
            self.marketData[m]["mo"] = calculateYaDelta(getYaMarketData(m, "1mo"), fromYear, dayStep)

    def loadIndexData(self, fromYear=0, dayStep=1):
        self.indexData["d"] = calculateYaDelta(getYaMarketData(self.indexName, "1d"), fromYear, dayStep)
        self.indexData["wk"] = calculateYaDelta(getYaMarketData(self.indexName, "1wk"), fromYear, dayStep)
        self.indexData["mo"] = calculateYaDelta(getYaMarketData(self.indexName, "1mo"), fromYear, dayStep)

            
    def calculateMarketCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(m1!=m0):
                    if(len(self.marketData[m0Name]["d"]["adjclose"]) > 0 and len(self.marketData[m1Name]["d"]["adjclose"]) > 0):
                        m0Times = [v["time"] for v in self.marketData[m0Name]["d"]["adjclose"]]
                        m1Times = [v["time"] for v in self.marketData[m1Name]["d"]["adjclose"]]
                        commonTimes = [v for v in m1Times if v in m0Times]
                        self.correlationMarketMatrix[m0][m1] = self.calculateCorrelation([v["value"] for v in self.marketData[m0Name]["d"]["adjclose"] if v["time"] in commonTimes], [v["value"] for v in self.marketData[m1Name]["d"]["adjclose"] if v["time"] in commonTimes])
                    else:
                        self.correlationMarketMatrix[m0][m1] = 0
                else:
                    self.correlationMarketMatrix[m0][m1] = 1
    
    def calculateMarketBetas(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(len(self.marketData[m0Name]["wk"]["adjclose"]) > 0 and len(self.marketData[m1Name]["wk"]["adjclose"]) > 0):
                    m0Times = [v["time"] for v in self.marketData[m0Name]["wk"]["adjclose"]]
                    m1Times = [v["time"] for v in self.marketData[m1Name]["wk"]["adjclose"]]
                    commonTimes = [v for v in m1Times if v in m0Times]
                    self.betaMarketMatrix[m0][m1] = self.calculateBeta([v["deltaPerc"] for v in self.marketData[m0Name]["wk"]["adjclose"] if v["time"] in commonTimes], [v["deltaPerc"] for v in self.marketData[m1Name]["wk"]["adjclose"] if v["time"] in commonTimes])
                else:
                    self.betaMarketMatrix[m0][m1] = 0


    def calculateIndexCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            if(len(self.marketData[m0Name]["d"]["adjclose"]) > 0):    
                m0Times = [v["time"] for v in self.marketData[m0Name]["d"]["adjclose"]]
                indxTimes = [v["time"] for v in self.indexData["d"]["adjclose"]]
                commonTimes = [v for v in indxTimes if v in m0Times]
                self.correlationIndexList[m0] = self.calculateWeightedCorrelation([v["value"] for v in self.marketData[m0Name]["d"]["adjclose"] if v["time"] in commonTimes], [v["value"] for v in self.indexData["d"]["adjclose"] if v["time"] in commonTimes], 5)
            else:
                self.correlationIndexList[m0] = -2

    
    def calculateWeightedCorrelation(self, data0, data1, sections):
        try:
            lenData = len(data0)
            ranges = math.ceil(lenData/sections)
            sum = 0
            for i in range(sections):
                sum += self.calculateCorrelation(data0[max(0, lenData-(i+1)*ranges):], data1[max(0, lenData-(i+1)*ranges):])
            return round(sum/sections, 4)
        except TypeError:
            return "N/D"



    def calculateCorrelation(self, data0, data1):
        try:
            av0 = sum(data0)/len(data0)
            av1 = sum(data1)/len(data1)
            return round(summt(data0, av0, data1, av1) / math.sqrt(summt(data0, av0, data0, av0)*summt(data1, av1, data1, av1)), 4)
        except:
            return "N/D"


    def calculateBeta(self, data0, data1):
        try:
            av0 = sum(data0)/len(data0)
            av1 = sum(data1)/len(data1)
            return round(summt(data0, av0, data1, av1) / summt(data1, av1, data1, av1), 4)
        except:
            return "N/D"

    
    def calculateIndexBetas(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            if(len(self.marketData[m0Name]["wk"]["adjclose"]) > 0):
                m0Times = [v["time"] for v in self.marketData[m0Name]["wk"]["adjclose"]]
                indxTimes = [v["time"] for v in self.indexData["wk"]["adjclose"]]
                commonTimes = [v for v in indxTimes if v in m0Times]
                self.betaIndexList[m0] = self.calculateBeta([v["deltaPerc"] for v in self.marketData[m0Name]["wk"]["adjclose"] if v["time"] in commonTimes], [v["deltaPerc"] for v in self.indexData["wk"]["adjclose"] if v["time"] in commonTimes])
            else:
                self.betaIndexList[m0] = 0



    def createCorrelationMatrix(self, markets, fromDate, toDate, interval, type):
        data = self.getMarketsData(markets, fromDate, toDate, interval, type)
        dataMat = []
        for m in markets:
            dataMat.append([d["value"] for d in data[m]])
        df = pd.DataFrame(dataMat).T
        return df.corr()
            

    def loadData(self, fromYear=0, dayStep=1, loadOnlyCache=False):
        if((self.cache==None or self.cache["date"]!=str(datetime.date.today()) or self.cache["indexName"]!=self.indexName or self.cache["marketList"]!=self.marketList) and not loadOnlyCache):
            self.cache={"date":str(datetime.date.today())}
            try:
                self.loadMarketData(fromYear,dayStep)
                self.loadIndexData(fromYear,dayStep)
                self.cache["index"]=self.indexData
                self.cache["market"]=self.marketData
                self.cache["indexName"]=self.indexName
                self.cache["marketList"]=self.marketList
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

        