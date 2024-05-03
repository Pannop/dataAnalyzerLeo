import eel
import json
import pandas
import os
from marketAnalyzer import MarketMatrix

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
    eel.setTitles(marketMatrix.cache)

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
    if(len(markets)==1):
        markets.append(marketMatrix.indexName)
    dataDaily = marketMatrix.getMarketsData(markets, fromDate, toDate, "d", type)
    dataWeekly = marketMatrix.getMarketsData(markets, fromDate, toDate, "wk", type)
    dataMonthly = marketMatrix.getMarketsData(markets, fromDate, toDate, "mo", type)
    
    correlation = marketMatrix.calculateCorrelation([d["value"] for d in dataDaily[markets[0]]], [d["value"] for d in dataDaily[markets[1]]])
    weightedCorrelation = marketMatrix.calculateWeightedCorrelation([d["value"] for d in dataDaily[markets[0]]], [d["value"] for d in dataDaily[markets[1]]], weightedCorrelationSections)
    betaDaily = marketMatrix.calculateBeta([d["deltaPerc"] for d in dataDaily[markets[0]]], [d["deltaPerc"] for d in dataDaily[markets[1]]])
    betaWeekly = marketMatrix.calculateBeta([d["deltaPerc"] for d in dataWeekly[markets[0]]], [d["deltaPerc"] for d in dataWeekly[markets[1]]])
    betaMonthly= marketMatrix.calculateBeta([d["deltaPerc"] for d in dataMonthly[markets[0]]], [d["deltaPerc"] for d in dataMonthly[markets[1]]])
    eel.applyStats(correlation, weightedCorrelation, betaDaily, betaWeekly, betaMonthly, elemsId)


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

