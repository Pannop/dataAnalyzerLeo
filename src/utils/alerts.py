import pandas as pd
import eel
import time
import requests
import re
import math
from datetime import datetime
from secondaries.currencyCoverter import CurrencyConverter
from secondaries.threadStopper import threadStop
from secondaries import requestHeaders
from marketAnalyzer import MarketMatrix
from utils.dataBase import DataBase
from utils.indicators import *
import inspect

class InvalidGatheringDataSettingsException(Exception):
    pass

def setConstructorArguments(object, *vargs):
    #bello ma l'intellisense poi non ti mostra gli attributi consigliati :(
    args = inspect.getargs(object.__init__.__code__).args[1:]
    if(len(args)!=len(vargs)):
        raise Exception("invalid number of arguments, args: ", len(args), ", vargs: ", len(vargs))
    for i in range(len(vargs)):
        object.__dict__[args[i]] = vargs[i]
        




class Alert():

    def __init__(self, minutesCheckRate):
        self.minutesCheckRate = minutesCheckRate
        self.stopped=False
        pass


    def gatherData(self):
        pass

    def checkAlerts(self):
        pass

    def test(self):
        pass
    
    def run(self):
        while(not self.stopped and not threadStop.stop):
            self.gatherData()
            self.checkAlerts()

            for t in range(self.minutesCheckRate*60):
                time.sleep(1)
                if(threadStop.stop):
                    break


class VolumePriceFilterAlert(Alert):
    deletedAlertMax = 20

    def __init__(self, minutesCheckRate, db:DataBase, minVolumePerc, minPricePerc, minVolume, minVolumePrice, regions, caps):
        super().__init__(minutesCheckRate)
        self.db = db
        self.minVolumePerc = minVolumePerc
        self.minPricePerc = minPricePerc
        self.minVolume = minVolume
        self.minVolumePrice = minVolumePrice
        self.regions = regions
        self.caps = caps
        self.data = []
        self.oldSymbols = {}
        self.filteredAlerts = []

    def gatherData(self, progressBarId=None):
        self.data = self.db.getWorldLatestData(self.regions, self.caps, progressBarId)
        
    def removeDeletedAlerts(filteredAlerts):
        deletedCount = 0
        toRemove = []
        for i in range(len(filteredAlerts)):
            if(filteredAlerts[-i-1]["deleted"]):
                deletedCount+=1
                if(deletedCount>VolumePriceFilterAlert.deletedAlertMax):
                    toRemove.append(filteredAlerts[-i-1])

        for tr in toRemove:
            filteredAlerts.remove(tr)

    def test(self, oldSymbols, progressBarId):
        if(oldSymbols!=None):
            self.oldSymbols = oldSymbols
        self.gatherData(progressBarId)
        self.checkAlerts()
        return self.filteredAlerts, self.oldSymbols


    def checkAlerts(self):
        try:
            filteredAlerts = calculateVolumePriceFilter(self.data, self.minVolumePerc, self.minPricePerc, self.minVolume, self.minVolumePrice, None)
            
            symbolsUpdated = [a["symbol"] for a in filteredAlerts]
            notPresent = [a for a in self.oldSymbols if a not in  symbolsUpdated]
            
            newAlerts = 0
            for a in filteredAlerts:
                if(a["symbol"] in self.oldSymbols):
                    a["time"] = self.oldSymbols[a["symbol"]]
                    a["new"] = 0
                else:
                    newAlerts+=1
                    a["time"] = datetime.now().time().replace(microsecond=0)
                    self.oldSymbols[a["symbol"]] = a["time"]
                    a["new"] = 1
                a["deleted"] = 0

            for np in notPresent:
                a = {"symbol":np, "time":self.oldSymbols[np], "deleted":1}
                filteredAlerts.insert(0, a)

            orderObjectListBy(filteredAlerts, "time")

            VolumePriceFilterAlert.removeDeletedAlerts(filteredAlerts)

            for a in filteredAlerts:
                a["time"] = str(a["time"])

            self.filteredAlerts = filteredAlerts
            return newAlerts>0

        except ConnectionError:
            print("listener connection error")

        return False

    
        

class VolumePriceAlert(Alert):
    def __init__(self, minutesCheckRate, mm:MarketMatrix, market, periodTotal, periodToCheck, interval, type):
        super().__init__(minutesCheckRate)
        self.mm = mm
        self.data = []
        self.volumes = []
        self.market = market
        self.interval = interval
        self.type = type
        self.periodTotal = periodTotal
        self.periodToCheck = periodToCheck

        
    def gatherData(self, fromDate=-1, toDate=-1):
        #self.mm.loadMarketData(self.market, [self.interval])
        self.data = self.mm.getMarketsData([self.market], fromDate, toDate, self.interval, self.type)[self.market][-self.periodTotal:]
        self.volumes = self.mm.getMarketsData([self.market], fromDate, toDate, self.interval, "volume")[self.market][-self.periodTotal:]


    def checkAlerts(self):
        vols = [d["value"] for d in self.volumes]
        avgVol = sum(vols)/len(vols)
        volsToCheck = vols[-self.periodToCheck:]
        avgVolToCheck = sum(volsToCheck)/min(self.periodToCheck, len(volsToCheck))
        
        prices = [d["value"] for d in self.data]
        avgPrice = sum(prices)/len(prices)
        pricesToCheck = prices[-self.periodToCheck:]
        avgPriceToCheck = sum(pricesToCheck)/min(self.periodToCheck, len(pricesToCheck))
        return (avgVolToCheck/avgVol-1)*100, ((avgPriceToCheck/avgPrice)-1)*100

    def test(self, fromDate, toDate):
        tmp = self.periodTotal
        self.periodTotal = 0
        self.gatherData(fromDate, toDate)
        self.periodTotal = tmp
        dataCopy = self.data.copy()
        volumesCopy = self.volumes.copy()
        alertsChecked = []
        for i in range(len(self.data) - self.periodTotal + 1):
            self.data = dataCopy[-self.periodTotal-i:len(dataCopy)-i]
            self.volumes = volumesCopy[-self.periodTotal-i:len(volumesCopy)-i]
            alertsChecked.insert(0, self.checkAlerts())
        return dataCopy, volumesCopy, alertsChecked
            
        


        

        
        

class IcebergAlert(VolumePriceAlert):
    def __init__(self, minutesCheckRate, mm:MarketMatrix, market, periodTotal, periodToCheck, interval, type, minAvgVolumeDeltaPerc, maxAvgPriceDeltaPerc):
        super().__init__(minutesCheckRate, mm, market, periodTotal, periodToCheck, interval, type)
        self.minAvgVolumeDeltaPerc = minAvgVolumeDeltaPerc
        self.maxAvgPriceDeltaPerc = maxAvgPriceDeltaPerc

    def checkAlerts(self):
        volPerc, pricePerc = super().checkAlerts()
        if(volPerc > self.minAvgVolumeDeltaPerc and abs(pricePerc) < self.maxAvgPriceDeltaPerc):
            return True

        return False

class BubbleAlert(VolumePriceAlert):
    def __init__(self, minutesCheckRate, mm:MarketMatrix, market, periodTotal, periodToCheck, interval, type, maxAvgVolumeDeltaPerc, minAvgPriceDeltaPerc):
        super().__init__(minutesCheckRate, mm, market, periodTotal, periodToCheck, interval, type)
        self.maxAvgVolumeDeltaPerc = maxAvgVolumeDeltaPerc
        self.minAvgPriceDeltaPerc = minAvgPriceDeltaPerc

    def checkAlerts(self):
        volPerc, pricePerc = super().checkAlerts()
        if(volPerc < self.maxAvgVolumeDeltaPerc and abs(pricePerc) > self.minAvgPriceDeltaPerc):
            return True
        return False


class MacdObvAlert(Alert):
    def __init__(self, minutesCheckRate, mm:MarketMatrix, market, periodTotal, interval, macdType, macdPeriodFast, macdPeriodSlow, macdPeriodSignal, macdThresholdIntersectedRatio, obvCurvePointsThresholdDeltaPerc):
        super().__init__(minutesCheckRate)
        self.mm = mm
        self.dataOpen = []
        self.dataClose = []
        self.dataVolume = []
        self.dataMacd = []
        self.market = market
        self.periodTotal = periodTotal
        self.interval = interval
        self.macdType = macdType
        self.macdPeriod1 = macdPeriodFast
        self.macdPeriod2 = macdPeriodSlow
        self.macdPeriodSignal = macdPeriodSignal
        self.macdThresholdIntersectedRatio = macdThresholdIntersectedRatio
        self.obvCurvePointsThresholdDeltaPerc = obvCurvePointsThresholdDeltaPerc

    def gatherData(self, fromDate=-1, toDate=-1):
        #self.mm.loadMarketData(self.market, [self.interval])
        self.dataOpen = self.mm.getMarketsData([self.market], fromDate, toDate, self.interval, "open")[self.market][-self.periodTotal:]
        self.dataClose = self.mm.getMarketsData([self.market], fromDate, toDate, self.interval, "close")[self.market][-self.periodTotal:]
        self.dataVolume = self.mm.getMarketsData([self.market], fromDate, toDate, self.interval, "volume")[self.market][-self.periodTotal:]
        self.dataMacd = self.mm.getMarketsData([self.market], fromDate, toDate, self.interval, self.macdType)[self.market][-self.periodTotal:]
        
    def test(self, fromDate, toDate):
        tmp = self.periodTotal
        self.periodTotal = 0
        self.gatherData(fromDate, toDate)
        self.periodTotal = tmp
        dataOpenCopy = self.dataOpen.copy()
        dataCloseCopy = self.dataClose.copy()
        dataVolumeCopy = self.dataVolume.copy()
        dataMacdCopy = self.dataMacd.copy()
        alertsChecked = []
        for i in range(len(dataMacdCopy) - self.periodTotal + 1):
            self.dataOpen = dataOpenCopy[-self.periodTotal-i:len(dataOpenCopy)-i]
            self.dataClose = dataCloseCopy[-self.periodTotal-i:len(dataCloseCopy)-i]
            self.dataVolume = dataVolumeCopy[-self.periodTotal-i:len(dataVolumeCopy)-i]
            self.dataMacd = dataMacdCopy[-self.periodTotal-i:len(dataMacdCopy)-i]
            alertsChecked.insert(0, self.checkAlerts())
        macd = calculateMACD(dataMacdCopy, self.macdPeriod1, self.macdPeriod2, self.macdPeriodSignal)[0]
        obv = calculateOBV(dataOpenCopy, dataCloseCopy, dataVolumeCopy)
        return dataMacdCopy, macd, obv, alertsChecked

        

    def checkAlerts(self):
        macd = calculateMACD(self.dataMacd, self.macdPeriod1, self.macdPeriod2, self.macdPeriodSignal)[0]
        obv = calculateOBV(self.dataOpen, self.dataClose, self.dataVolume)
        avgMacd = sum([abs(d) for d in macd])/len(macd)
        lastDate = macd[-1]
        if(abs(lastDate)*100/avgMacd > self.macdThresholdIntersectedRatio):
            firstDate=0
            firstDateIndex = 0
            for i in range(2,len(macd)):
                firstDate=macd[-i]
                firstDateIndex=-i
                if(abs(firstDate)*100/avgMacd > self.macdThresholdIntersectedRatio):
                    break
            if(math.copysign(1, firstDate)!=math.copysign(1,lastDate)):
                obvCurvePoints = [obv[firstDateIndex-1], obv[firstDateIndex], obv[-1]]
                avgObvDelta = 0
                for i in range(len(obv)-1):
                    avgObvDelta += abs(obv[i+1]-obv[i])
                avgObvDelta/=len(obv)-1

                obvCurvePointsDeltasPerc = [((obvCurvePoints[1]-obvCurvePoints[0])/avgObvDelta - 1)*100, ((obvCurvePoints[2]-obvCurvePoints[1])/avgObvDelta - 1)*100]
                
                if(abs(obvCurvePointsDeltasPerc[0])>self.obvCurvePointsThresholdDeltaPerc and abs(obvCurvePointsDeltasPerc[1])>self.obvCurvePointsThresholdDeltaPerc):
                    info = {"trend":0, "macdHighlight":firstDateIndex, "obvHighlight":firstDateIndex}
                    if(obvCurvePointsDeltasPerc[0]>0):
                        info["trend"] = 1
                    else:
                        info["trend"] = -1
                    return True, info


        return False, {}




