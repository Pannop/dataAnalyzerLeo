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




fileIn = open("resources/marketListCode.txt", "r")
l = fileIn.read().split("\n")
fileIn.close()
mm = MarketMatrix(l, "FTSEMIB.MI", CACHE_FILE)

 


frontEndManager.__init__(1200, 900, mm)  
frontEndManager.start()

