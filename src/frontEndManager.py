from datetime import datetime, timedelta, date
import eel
import json
import pandas
import os
from copy import deepcopy 
import numpy as np
from marketAnalyzer import MarketMatrix
from utils.marketStatusChecker import MarketStatusChecker
from utils.indicators import *
from utils.backTest import runBackTesting
from utils.dataBase import DataBase
from secondaries.threadStopper import threadStop
import matplotlib.pyplot as plt
import frontEndIndicatorsAlerts 
from frontEndIndicatorsAlerts import loadDashboardData, formatGoogleChart

eel.init("./src/web/")

winSize = None
dataBase = None
marketMatrix = None
marketStatusChecker = None 


def __init__(dimX, dimY, dataBaseRef: DataBase, marketStatusCheckerRef: MarketStatusChecker):
    global winSize
    winSize = [dimX, dimY]
    global dataBase
    dataBase = dataBaseRef
    global marketStatusChecker
    marketStatusChecker = marketStatusCheckerRef
    frontEndIndicatorsAlerts.__init__(dataBase)

def setMarketMatrix(marketMatrixRef: MarketMatrix):
    global marketMatrix
    marketMatrix = marketMatrixRef

def stopThreads(route, websockets):
    if not websockets:
        threadStop.stop = True
        exit()

def start():
    #eel.start("start.html", size=winSize, close_callback=stopThreads, shutdown_delay=10)
    eel.start("menu.html", size=winSize, close_callback=None, shutdown_delay=10)

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
    eel.setTitles({"marketList":marketMatrix.marketList})





@eel.expose
def formatData(markets, fromDate, toDate, interval, type, valueType, dataChartCode):
    if(len(markets)==0):
        return []
    data = marketMatrix.getMarketsData(markets, fromDate, toDate, interval, type)
    formattedData = formatGoogleChart(data, markets, valueType)

    
    eel.applyChart(formattedData, dataChartCode) 


@eel.expose
def calculateStats(markets, fromDate, toDate, interval, type, weightedCorrelationSections, elemsId):
    if(len(markets)==1):
        markets.append(marketMatrix.getIndexOfTitle(markets[0]))
    dataDaily = marketMatrix.getMarketsData(markets, fromDate, toDate, "d", type)
    dataWeekly = marketMatrix.getMarketsData(markets, fromDate, toDate, "wk", type)
    dataMonthly = marketMatrix.getMarketsData(markets, fromDate, toDate, "mo", type)
    correlation = marketMatrix.calculateCorrelation([d["value"] for d in dataDaily[markets[0]]], [d["value"] for d in dataDaily[markets[1]]])
    weightedCorrelation = marketMatrix.calculateWeightedCorrelation([d["value"] for d in dataDaily[markets[0]]], [d["value"] for d in dataDaily[markets[1]]], weightedCorrelationSections)
    def getBeta(data):
        try:
            return round(marketMatrix.calculateBeta([d["deltaPerc"] for d in data[markets[0]]], [d["deltaPerc"] for d in data[marketMatrix.getIndexOfTitle(markets[0])]]) / marketMatrix.calculateBeta([d["deltaPerc"] for d in data[markets[1]]], [d["deltaPerc"] for d in data[marketMatrix.getIndexOfTitle(markets[1])]]), 3)
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
def calculateCorrelationMatrix(markets, fromDate, toDate, interval, type, exportExcel):
    corrMatrix = marketMatrix.createCorrelationMatrix(markets, fromDate, toDate, interval, type)
    if(exportExcel):
        exportMatrix = [[0]*(len(markets)+1) for x in range(len(markets)+1)]
        for i in range(len(markets)):
            exportMatrix[i+1][0] = markets[i]
            exportMatrix[0][i+1] = markets[i]
        for i in range(len(markets)):
            for j in range(len(markets)):
                exportMatrix[i+1][j+1] = corrMatrix[i][j]
        
        jsonToXlsx(exportMatrix, "correlationalMatrix.xlsx")
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


@eel.expose()
def getRealtimeSuffixes():
    eel.setRealtimeSuffixes(marketStatusChecker.getRealtimeSuffixes())

@eel.expose
def getMarketStatus():
    if(marketStatusChecker.isReady()):
        eel.setMarketStatus(marketStatusChecker.getMarketStatus())
    else:
        eel.setMarketStatus(None)

@eel.expose
def calculateBackTesting(title):
    testsResults, testsResultsSummary = runBackTesting(title, marketMatrix)
    with open("sum.json", "w") as sum, open("res.json", "w") as res:
        sum.write(json.dumps(testsResultsSummary))
        res.write(json.dumps(testsResults))
    print(testsResults)



@eel.expose
def loadMenuData():
    #non ho potuto usare la deepcopy perchè aveva problemi col lock degli oggetti aggancati da thread
    dataTest = dataBase.config["dashboards"].copy()
    dateCur = date.today().strftime("%Y-%m-%d")
    datePast=""    
    interval=""

    for dashboard in dataTest:
        dataTest[dashboard] = dataTest[dashboard].copy()
        del dataTest[dashboard]["alertListeners"]
        isWatchlist = dataTest[dashboard]["type"]=="watchlist"
        isPortfolio = dataTest[dashboard]["type"]=="portfolio"
        if(isWatchlist):
            interval="wk"
            yearPast = 1
            datePast = (date.today() + timedelta(weeks=-52*yearPast)).strftime("%Y-%m-%d")
        elif(isPortfolio):
            interval="d"
            datePast = (date.today() + timedelta(days=-5)).strftime("%Y-%m-%d")
        markets = list(dataTest[dashboard]["titles"].keys())
        marketsData = dataBase.getMarketMatrix(dashboard).getMarketsData(markets, datePast, dateCur, interval, "close")
        latestValues = []
        emptyData=False
        for m in markets:
            if(len(marketsData[m])==0):
                    emptyData=True
                    break
            latestValues.append(marketsData[m][-1]["value"])
        if(emptyData):
            dataTest[dashboard]["chart"] = []
            continue
        latestValues.sort(reverse=True)
        
        minValueFilter=0
        if(isWatchlist):
            minValueFilter = latestValues[min(len(latestValues), 7) - 1]
        filteredMarketsData = {key:val for (key,val) in marketsData.items() if val[-1]["value"] >=  minValueFilter}
        
        if(isPortfolio):
            for title in marketsData:
                dataTest[dashboard]["titles"] =  dataTest[dashboard]["titles"].copy()
                dataTest[dashboard]["titles"][title] = dataTest[dashboard]["titles"][title].copy()
                dataTest[dashboard]["titles"][title]["latestPrice"] = marketsData[title][-1]["value"]

        dataTest[dashboard]["chart"] = formatGoogleChart(filteredMarketsData, list(filteredMarketsData.keys()), "value")
    eel.applyMenuData(dataTest)


@eel.expose
def loadDashboard(dashboard):
    mm = dataBase.getMarketMatrix(dashboard)
    setMarketMatrix(mm)
    loadDashboardData(mm)
    eel.openDashboard()