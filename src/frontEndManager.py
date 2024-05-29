from datetime import datetime, timedelta
import eel
import json
import pandas
import os
import numpy as np
from marketAnalyzer import MarketMatrix
from alert import AlertChecker
from prevision import calculateHeston, calculateMontecarlo, calculateMontecarloGeometricBrownianMotion, calculateMontecarloV2

eel.init("./src/web/")

winSize = None
marketMatrix = None
alertChecker = None


def __init__(dimX, dimY, marketMatrixRef: MarketMatrix, alertCheckerRef: AlertChecker):
    global winSize
    winSize = [dimX, dimY]
    global marketMatrix
    marketMatrix = marketMatrixRef
    global alertChecker
    alertChecker = alertCheckerRef

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

def format(data, markets, valueType):
    formattedData = []
    for t in range(len(data[markets[0]])):
        formattedData.append([data[markets[0]][t]["timestamp"]])
        for m in markets:
            formattedData[t].append(data[m][t][valueType])
    return formattedData

@eel.expose
def formatData(markets, fromDate, toDate, interval, type, valueType, elemId, dataChartCode):
    if(len(markets)==0):
        return []
    data = marketMatrix.getMarketsData(markets, fromDate, toDate, interval, type)
    formattedData = format(data, markets, valueType)
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
        
    def getBetaV2(data):
        return marketMatrix.calculateBetaV2([d["deltaPerc"] for d in data[markets[0]]], [d["deltaPerc"] for d in data[markets[1]]], correlation)

    betaDaily = getBetaV2(dataDaily)
    betaWeekly = getBetaV2(dataWeekly)
    betaMonthly = getBetaV2(dataMonthly)
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
        
    #deltaTrendDaily = getDeltaTrend(dataDaily)
    #deltaTrendWeekly = getDeltaTrend(dataWeekly)
    #deltaTrendMonthly = getDeltaTrend(dataMonthly)
    eel.applyStats(correlation, weightedCorrelation, betaDaily, betaWeekly, betaMonthly, elemsId)


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
def calculatePrevision(market, fromDate, toDate, interval, type, simulations, dataNum):
    data = marketMatrix.getMarketsData([market], fromDate, toDate, interval, type)
    formattedData = format(data, [market], "value")
    formattedPrevision = []
    montecarloData = calculateMontecarloV2(data[market], simulations, dataNum)
    montecarloGBMData = calculateMontecarloGeometricBrownianMotion(data[market], simulations, dataNum)
    hestonData = calculateHeston(data[market], simulations, dataNum)
    date = datetime.fromtimestamp(formattedData[-1][0])
    for i in range(dataNum):
        day = [date.timestamp()]
        if(interval=="d"):
            date += timedelta(days=1)
            if(date.weekday() == 5 ):
                date += timedelta(days=2)
        elif(interval=="wk"):
            date += timedelta(weeks=1)
        elif(interval=="mo"):
            date += timedelta(days=(31 if date.month in (1,3,5,7,8,10,12) else 30))
       
        day.append(montecarloData[i])
        day.append(montecarloGBMData[i])
        day.append(hestonData[i])
        formattedPrevision.append(day)

    eel.applyChartPrevision(formattedData, formattedPrevision)


@eel.expose
def checkAlert(volumePerc, valuePerc, minVolume):
    alertChecker.fastCheck(volumePerc, valuePerc, minVolume)
    eel.applyAlertTable(alertChecker.alerts)


