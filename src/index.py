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




#jsonToXlsx(getBIMarketData("DE000VU32806"))
#jsonToXlsx(calculateDelta(getBIMarketData("DE000VU32806")), "jsonDeltaFile.json", "excelDeltaFile.xlsx")
#print(getUSMarketData("TIME_SERIES_DAILY", "IBM", "outputsize=full"))
    
CACHE_FILE="./cache"
MARKET_START=0
MARKET_STOP=3
MARKET_SINGLE_TITLE = [12,11]

FROM_YEAR = 2019
DAY_STEP = 1




fileIn = open("resources/marketListCode.txt", "r")
l = fileIn.read().split("\n")
fileIn.close()
mm = MarketMatrix(l, "FTSEMIB.MI", CACHE_FILE)
#mm.loadData(FROM_YEAR, DAY_STEP)

#createDebugFiles(mm)
 


frontEndManager.__init__(1200, 900, mm)
frontEndManager.start()

