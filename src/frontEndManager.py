import eel
import json
import pandas
import os
import numpy as np
from marketAnalyzer import MarketMatrix
from montecarlo import calculateMontecarlo, calculateMontecarloV2

eel.init("./src/web/")

winSize = None
marketMatrix = None



def __init__(dimX, dimY, marketMatrixObj: MarketMatrix):
    global winSize
    winSize = [dimX, dimY]
    global marketMatrix
    marketMatrix = marketMatrixObj

def start():
    marketMatrix.loadCache()
    marketMatrix.loadData()
    marketMatrix.saveCache()
    eel.start("start.html", size=winSize)

DATA_DIR = "./data/"
def jsonToXlsx(data, excelFile="excelFile.xlsx"):
    jsonFile="temp.json"
    with open(DATA_DIR+jsonFile, "w") as file:
        file.write(json.dumps(data))
    dataPd = pandas.read_json(DATA_DIR+jsonFile)
    os.remove(DATA_DIR+jsonFile)
    return dataPd.to_excel(DATA_DIR+excelFile)

@eel.expose
def setDefaultSize():
    eel.setSize(winSize[0], winSize[1])

@eel.expose
def loadTitles():
    eel.setTitles({"indexName":marketMatrix.cache["indexName"], "marketList":marketMatrix.cache["marketList"]})

@eel.expose
def formatData(markets, fromDate, toDate, interval, type, valueType, elemId, dataChartCode):
    if(len(markets)==0):
        return []
    data = marketMatrix.getMarketsData(markets, fromDate, toDate, interval, type)
    formattedData = []
    for t in range(len(data[markets[0]])):
        formattedData.append([data[markets[0]][t]["timestamp"]])
        for m in markets:
            formattedData[t].append(data[m][t][valueType])
    eel.applyChart(formattedData, elemId, dataChartCode) 


@eel.expose
def calculateStats(markets, fromDate, toDate, interval, type, weightedCorrelationSections, elemsId):
    markets.append(marketMatrix.indexName)
    dataDaily = marketMatrix.getMarketsData(markets, fromDate, toDate, "d", type)
    dataWeekly = marketMatrix.getMarketsData(markets, fromDate, toDate, "wk", type)
    dataMonthly = marketMatrix.getMarketsData(markets, fromDate, toDate, "mo", type)
    
    correlation = marketMatrix.calculateCorrelation([d["value"] for d in dataDaily[markets[0]]], [d["value"] for d in dataDaily[markets[1]]])
    weightedCorrelation = marketMatrix.calculateWeightedCorrelation([d["value"] for d in dataDaily[markets[0]]], [d["value"] for d in dataDaily[markets[1]]], weightedCorrelationSections)
    def getBeta(data):
        try:
            return round(marketMatrix.calculateBeta([d["deltaPerc"] for d in data[markets[0]]], [d["deltaPerc"] for d in data[marketMatrix.indexName]]) / marketMatrix.calculateBeta([d["deltaPerc"] for d in data[markets[1]]], [d["deltaPerc"] for d in data[marketMatrix.indexName]]), 3)
        except:
            return "N/D"

    betaDaily = getBeta(dataDaily)
    betaWeekly = getBeta(dataWeekly)
    betaMonthly = getBeta(dataMonthly)
    #betaWeekly = marketMatrix.calculateBeta([d["deltaPerc"] for d in dataWeekly[markets[0]]], [d["deltaPerc"] for d in dataWeekly[markets[1]]])
    #betaMonthly= marketMatrix.calculateBeta([d["deltaPerc"] for d in dataMonthly[markets[0]]], [d["deltaPerc"] for d in dataMonthly[markets[1]]])
    
    def getDeltaTrend(data):
        maxThreshold = 10
        beforeMean = 0.1
        lst = []
        try:
            for i in range(len(data[markets[0]])):
                if data[markets[1]][i]["deltaPerc"]!=0:
                    val = data[markets[0]][i]["deltaPerc"]/data[markets[1]][i]["deltaPerc"]
                    prog = i/len(data[markets[0]])
                    if(prog<=beforeMean or (prog>beforeMean and abs(val/np.average(lst)) < maxThreshold)):
                        lst.append(val)
            
            return round(sum(lst)/len(lst), 3)
        except:
            return "N/D"
        
    deltaTrendDaily = getDeltaTrend(dataDaily)
    deltaTrendWeekly = getDeltaTrend(dataWeekly)
    deltaTrendMonthly = getDeltaTrend(dataMonthly)
    #deltaTrendWeekly = np.average([dataWeekly[markets[0]][i]["deltaPerc"]/dataWeekly[markets[1]][i]["deltaPerc"] for i in range(len(dataWeekly[markets[0]])) if dataWeekly[markets[1]][i]["deltaPerc"]!=0])
    #deltaTrendMonthly = np.average([dataMonthly[markets[0]][i]["deltaPerc"]/dataMonthly[markets[1]][i]["deltaPerc"] for i in range(len(dataMonthly[markets[0]])) if dataMonthly[markets[1]][i]["deltaPerc"]!=0])
    eel.applyStats(correlation, weightedCorrelation, betaDaily, betaWeekly, betaMonthly, deltaTrendDaily, deltaTrendWeekly, deltaTrendMonthly, elemsId)


@eel.expose
def calculateCorrelationMatrix(markets, fromDate, toDate, interval, type):
    corrMatrix = marketMatrix.createCorrelationMatrix(markets, fromDate, toDate, interval, type)
    eel.createCorrelationTable(corrMatrix)
    

@eel.expose
def exportExcel(market, fromDate, toDate, interval, type):

    data = marketMatrix.getMarketsData([market], fromDate, toDate, interval, type)
    dataExp={
        "deltaPerc":{d["time"]:d["deltaPerc"] for d in data[market]},
        "delta":{d["time"]:d["delta"] for d in data[market]},
        "value":{d["time"]:d["value"] for d in data[market]}
    }
    jsonToXlsx(dataExp, "market"+market+".xlsx")
    
@eel.expose
def sendStopDrawing():
    eel.stopDrawing()


@eel.expose
def mont(market, fromDate, toDate, interval, type, simulations, dataNum):
    data = marketMatrix.getMarketsData([market], fromDate, toDate, interval, type)
    calculateMontecarloV2(data[market], simulations, dataNum)


