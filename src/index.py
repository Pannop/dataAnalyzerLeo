import datetime
import os
import requests
import pandas
import json
import numpy as np
import time
import math
import matplotlib as mp
from marketAnalyzer import *
import frontEndManager
from alert import AlertChecker
from currencyCoverter import CurrencyConverter
from marketStatusChecker import MarketStatusChecker



#jsonToXlsx(getBIMarketData("DE000VU32806"))
#jsonToXlsx(calculateDelta(getBIMarketData("DE000VU32806")), "jsonDeltaFile.json", "excelDeltaFile.xlsx")
#print(getUSMarketData("TIME_SERIES_DAILY", "IBM", "outputsize=full"))
    
CACHE_FILE="./cache"




fileIn = open("resources/marketListCode.txt", "r")
marketList = fileIn.read().split("\n")
fileIn.close()




mm = MarketMatrix(marketList, "FTSEMIB.MI", CACHE_FILE)
cc= CurrencyConverter()
ac = AlertChecker(cc)
msc = MarketStatusChecker(5*60)
msc.start()


 
frontEndManager.__init__(1200, 900, mm, ac, msc)  
frontEndManager.start()
