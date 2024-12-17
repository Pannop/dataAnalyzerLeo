from datetime import datetime, timedelta, date
import eel
import json
import pandas
import os
from threading import Thread
from copy import deepcopy 
import numpy as np
from marketAnalyzer import MarketMatrix
from utils.marketStatusChecker import MarketStatusChecker
from utils.indicators import *
from utils.alerts import *
from utils.backTest import runBackTesting
from utils.dataBase import DataBase
from secondaries.threadStopper import threadStop
import matplotlib.pyplot as plt

marketMatrix = None
dataBase = None

def __init__(dataBaseRef:DataBase):
    global dataBase
    dataBase = dataBaseRef

def loadDashboardData(marketMatrixRef: MarketMatrix):
    global marketMatrix
    marketMatrix = marketMatrixRef

def formatGoogleChart(data, markets, valueType):
    formattedData = []
    try:
        for t in range(len(data[markets[0]])):
            formattedData.append([data[markets[0]][t]["timestamp"]])
            for m in markets:
                formattedData[t].append(data[m][t][valueType])
    except:
        print("-----------------")
        print(data)

    return formattedData

def joinGoogleChart(data0, data1):
    formatted = []
    i0=0
    i1=0
    while(i0<len(data0) or i1<len(data1)):
        t0 = data0[i0][0] if i0<len(data0) else math.inf
        t1 = data1[i1][0] if i1<len(data1) else math.inf
        tmin = min(t0, t1)
        row = [tmin]
        if(t0==tmin):
            row.extend(data0[i0][1:])
            i0+=1
        else:
            row.extend([None]*(len(data0[0])-1))
        if(t1==tmin):
            row.extend(data1[i1][1:])
            i1+=1
        else:
            row.extend([None]*(len(data1[0])-1))
        formatted.append(row)
    return formatted
            

def formatDataFromValueList(marketData, dataLists):
    formatted = []
    for i in range(len(dataLists[0])):
        slice = [marketData[len(marketData)-len(dataLists[0])+i]["timestamp"]]
        for dataList in dataLists:
            slice.append(dataList[i])
        formatted.append(slice)
    return formatted

def formatDataWithMultipleSeparations(marketData, separationMasks, valueType="value"):
    formatted = []
    minMaskLen = math.inf
    for m in separationMasks:
        if(len(m) < minMaskLen):
            minMaskLen = len(m)

    for i in range(minMaskLen):
        dataIndex = len(marketData)-minMaskLen+i
        val = marketData[dataIndex][valueType]
        slice = [marketData[dataIndex]["timestamp"], val]
        for mask in separationMasks:
            slice.append(val if mask[i] else None)
        formatted.append(slice)
    return formatted

def formatDataWithSeparation(marketData, separationMask, valueType="value"):
    return formatDataWithMultipleSeparations(marketData, [separationMask], valueType)


def mupltipleSeparateFormattedData(formattedData, separationMasks):
    formatted = []
    minMaskLen = math.inf
    for m in separationMasks:
        if(len(m) < minMaskLen):
            minMaskLen = len(m)

    for i in range(minMaskLen):
        dataIndex = len(formattedData)-minMaskLen+i
        val = formattedData[dataIndex][1]
        slice = formattedData[dataIndex].copy()
        for mask in separationMasks:
            slice.append(val if mask[i] else None)
        formatted.append(slice)
    return formatted

def separateFormattedData(formattedData, separationMask):
    return mupltipleSeparateFormattedData(formattedData, [separationMask])


########################## INDICATORS #########################

@eel.expose
def indicator_prevision_calculate(market, dataChartCode, futureData, simulations, historicalData, interval, type):
    fromDate=historicalData[0]
    toDate=historicalData[1]
    data = marketMatrix.getMarketsData([market], fromDate, toDate, interval, type)
    formattedData = formatGoogleChart(data, [market], "value")
    formattedPrevision = []
    montecarloData = calculateMontecarloV2(data[market], simulations, futureData)
    montecarloGBMData = calculateMontecarloGeometricBrownianMotion(data[market], simulations, futureData)
    hestonData = calculateHeston(data[market], simulations, futureData)
    date = datetime.fromtimestamp(formattedData[-1][0])
    for i in range(futureData):
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
    formatted = joinGoogleChart(formattedData, formattedPrevision)
    eel.applyChart(formatted, dataChartCode)
    #eel.applyChartPrevision(formattedData, formattedPrevision)



@eel.expose
def indicator_rsi_calculate(market, dataChartCode, historicalData, interval, type, period):
    fromDate=historicalData[0]
    toDate=historicalData[1]
    data = marketMatrix.getMarketsData([market], fromDate, toDate, interval, type)[market]
    rsi = calculateExpRSI(data, period)
    formatted = formatDataFromValueList(data, [rsi])
    eel.applyChart(formatted, dataChartCode)

@eel.expose
def indicator_obv_calculate(market, dataChartCode, historicalData, interval):
    fromDate=historicalData[0]
    toDate=historicalData[1]
    dataOpen = marketMatrix.getMarketsData([market], fromDate, toDate, interval, "open")[market]
    dataClose = marketMatrix.getMarketsData([market], fromDate, toDate, interval, "close")[market]
    dataVolume = marketMatrix.getMarketsData([market], fromDate, toDate, interval, "volume")[market]
    obv = calculateOBV(dataOpen, dataClose, dataVolume)
    formatted = formatDataFromValueList(dataClose, [obv])
    eel.applyChart(formatted, dataChartCode)


@eel.expose
def indicator_macd_calculate(market, macdChartCode, signalChartCode , historicalData, interval, type, period1, period2, periodSignal):
    fromDate=historicalData[0]
    toDate=historicalData[1]
    data = marketMatrix.getMarketsData([market], fromDate, toDate, interval, type)[market]
    macd, macdSignal, signal = calculateMACD(data, period1, period2, periodSignal)
    formattedMacd = formatDataFromValueList(data, [macd])
    formattedSignal = formatDataFromValueList(data, [macdSignal, signal])
    eel.applyChart(formattedMacd, macdChartCode)
    eel.applyChart(formattedSignal, signalChartCode)

@eel.expose
def indicator_volumePriceFilter_calculate(minVolumePerc, minPricePerc, minVolume, minVolumePrice, regions, caps, forceUpdateData, sort, progressBarId, prevData, prevRegions, prevCaps):
    data = prevData
    if(prevData==None or regions!=prevRegions or caps!=prevCaps  or forceUpdateData):
        data = marketMatrix.getWorldLatestData(regions, caps, progressBarId)
    filtered = calculateVolumePriceFilter(data, minVolumePerc, minPricePerc, minVolume, minVolumePrice, sort)
    eel.indicator_volumePriceFilter_applyTable(filtered, data, regions, caps)




########################## ALERTS #########################


@eel.expose
def alert_iceberg_test(market, dataChartCode, volumeChartCode, volumeBarChartCode, historicalData, periodTotal, periodToCheck, interval, type, minAvgVolumeDeltaPerc, maxAvgPriceDeltaPerc):
    fromDate = historicalData[0]
    toDate = historicalData[1]
    alert = IcebergAlert(0, marketMatrix, market, periodTotal, periodToCheck, interval, type, minAvgVolumeDeltaPerc, maxAvgPriceDeltaPerc)
    print(alert.__dict__)
    data, volumes, alertsChecked = alert.test(fromDate, toDate)
    formattedData = formatDataWithSeparation(data, alertsChecked)
    formattedVolumes = formatDataWithSeparation(volumes, alertsChecked)
    eel.applyChart(formattedData, dataChartCode)
    eel.applyChart(formattedVolumes, volumeChartCode)
    eel.applyChart(formattedVolumes, volumeBarChartCode)
    eel.alert_iceberg_testApplyResults(len([x for x in alertsChecked if x]))


@eel.expose
def alert_macdObv_test(market, dataChartCode, macdChartCode, obvChartCode, historicalData, periodTotal, interval, macdType, macdPeriod1, macdPeriod2, macdPeriodSignal, macdThresholdIntersectedRatio, obvCurvePointsThresholdDeltaPerc):
    fromDate = historicalData[0]
    toDate = historicalData[1]
    alert = MacdObvAlert(0, marketMatrix, market, periodTotal, interval, macdType, macdPeriod1, macdPeriod2, macdPeriodSignal, macdThresholdIntersectedRatio, obvCurvePointsThresholdDeltaPerc)
    data, dataMacd, dataObv, alertsChecked = alert.test(fromDate, toDate)
    alertsCheckedTrendGain = {"dataHighlight":[v[0] if(v[0] and v[1]["trend"]==1) else False for v in alertsChecked]}
    alertsCheckedTrendLoss = {"dataHighlight":[v[0] if(v[0] and v[1]["trend"]==-1) else False for v in alertsChecked]}
    for highlight in ["macdHighlight", "obvHighlight"]:
        alertsCheckedTrendGain[highlight] = [v[0] if(v[0] and v[1]["trend"]==1) else False for v in alertsChecked]
        alertsCheckedTrendLoss[highlight] = [v[0] if(v[0] and v[1]["trend"]==-1) else False for v in alertsChecked]
        for alertsCheckedTrend in [alertsCheckedTrendGain[highlight], alertsCheckedTrendLoss[highlight]]:
            for i in range(len(alertsCheckedTrend)):
                if(alertsCheckedTrend[i]):
                    for j in range(1, abs(alertsChecked[i][1][highlight])):
                        alertsCheckedTrend[i-j] = True

    formattedData = formatDataWithMultipleSeparations(data, [alertsCheckedTrendGain["dataHighlight"], alertsCheckedTrendLoss["dataHighlight"]])    
    formattedMacd = formatDataFromValueList(data, [dataMacd])
    formattedMacd = mupltipleSeparateFormattedData(formattedMacd, [alertsCheckedTrendGain["macdHighlight"], alertsCheckedTrendLoss["macdHighlight"]])
    formattedObv = formatDataFromValueList(data, [dataObv])
    formattedObv = mupltipleSeparateFormattedData(formattedObv, [alertsCheckedTrendGain["obvHighlight"], alertsCheckedTrendLoss["obvHighlight"]])
    eel.applyChart(formattedData, dataChartCode)
    eel.applyChart(formattedMacd, macdChartCode)
    eel.applyChart(formattedObv, obvChartCode)

@eel.expose
def alert_volumePriceFilter_test(minVolumePerc, minPricePerc, minVolume, minVolumePrice, regions, caps, progressBarId, oldSymbols):
    if(oldSymbols):
        for s in oldSymbols:
            oldSymbols[s] = datetime.strptime(oldSymbols[s], "%H:%M:%S").time()
    alert = VolumePriceFilterAlert(0, dataBase, minVolumePerc, minPricePerc, minVolume, minVolumePrice, regions, caps)
    data, oldSymbols = alert.test(oldSymbols, progressBarId)
    for s in oldSymbols:
        oldSymbols[s] = str(oldSymbols[s])
    eel.alert_volumePriceFilter_testApplyTable(data, oldSymbols)




########################## LISTENERS #########################

def alert_addListener(alert, globalAlert=False):
    configListeners = (dataBase.config["alertListeners"] if globalAlert else marketMatrix.config["alertListeners"])
    configListeners.append(alert)
    Thread(target=alert.run).start()

def getDashboardAlertListeners():
    pass

def getGlobalAlertListeners():
    pass

@eel.expose
def alert_iceberg_addListener(market, minutesCheckRate, data):
    alert = IcebergAlert(minutesCheckRate, marketMatrix, market, *data)
    alert_addListener(alert)
