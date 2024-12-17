import math

import numpy as np
import pandas as pd


def summt(d0, a0, d1, a1):
        s=0
        for i in range(len(d0)):
            s+=(d0[i]-a0)*(d1[i]-a1)
        return s

class MarketMatrixCalculus:
    
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
