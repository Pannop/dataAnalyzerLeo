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
from marketAnalyzerCalculus import MarketMatrixCalculus
from secondaries.currencyCoverter import CurrencyConverter




def listsIntersection(lists):
    if(len(lists)>0):
        inter = set(lists[0])
        for i in range(1, len(lists)):
            inter = inter.intersection(set(lists[i]))
        return list(inter)
    else:
        return []

class MarketMatrix(MarketMatrixCalculus):

    def __init__(self, marketData, config, database):
        self.marketList = []
        self.indexList = []
        self.marketData = marketData
        self.config = config
        self.database = database
        
        for title in config["titles"]:
            self.marketList.append(title)
            self.indexList.append(config["titles"][title]["index"])
        self.indexList = list(set(self.indexList))
        self.marketList = list(set(self.marketList))
        self.marketList.sort()

    def getIndexOfTitle(self, title):
        if(title in self.config["titles"]):
            return self.config["titles"][title]["index"]
        return None
    
    def loadMarketData(self, m, intervalToLoad=["d", "wk", "mo"]):
        self.database.loadMarketData(m, intervalToLoad)

    def getMarketsData(self, markets, fromDate, toDate, interval, type):
        data = {}
        fromDateTimeStamp = 0
        if(fromDate!=-1):
            fromDateTimeStamp = datetime.datetime.strptime(fromDate, "%Y-%m-%d").timestamp()
        toDateTimeStamp = math.inf
        if(toDate!=-1):
            toDateTimeStamp = datetime.datetime.strptime(toDate, "%Y-%m-%d").timestamp()
        for m in markets:
            data[m] = [d for d in self.marketData[m][interval][type] if int(d["timestamp"])>=fromDateTimeStamp and int(d["timestamp"])<=toDateTimeStamp]
        
        totalTimestamps = []
        for m in markets:
            totalTimestamps.append([d["time"] for d in data[m]])
        commonsTimestamps = listsIntersection(totalTimestamps)
        for m in markets:
            data[m] = [d for d in data[m] if d["time"] in commonsTimestamps]
        return data
    
    def getWorldLatestData(self, regions, caps, progressBarId=None):
        return self.database.getWorldLatestData(regions, caps, progressBarId)

