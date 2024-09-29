import math

import numpy as np
import pandas as pd


def summt(d0, a0, d1, a1):
        s=0
        for i in range(len(d0)):
            s+=(d0[i]-a0)*(d1[i]-a1)
        return s

class MarketMatrixCalculus:
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
        
    def calculateBetaV2(self, data0, data1, correlation):
        try:
            std0 = np.std(data0)
            std1 = np.std(data1)
            return round(correlation* (std0/std1), 4)
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
        dataMat = [[0 for j in range(len(markets))] for i in range(len(markets))]
        for i in range(len(markets)):
            for j in range(len(markets)):
                if(i < j):
                    data = self.getMarketsData([markets[i], markets[j]], fromDate, toDate, interval, type)
                    df = pd.DataFrame([[d["value"] for d in data[markets[i]]], [d["value"] for d in data[markets[j]]]]).T
                    cor = round(df.corr()[0][1], 3)
                    dataMat[i][j] = cor
                    dataMat[j][i] = cor

                if(i==j):
                    dataMat[i][j] = 1
        return dataMat
