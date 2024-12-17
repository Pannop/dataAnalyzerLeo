from marketAnalyzer import *
import frontEndManager
from secondaries.currencyCoverter import CurrencyConverter
from utils.marketStatusChecker import MarketStatusChecker
from utils.dataBase import DataBase

CACHE_FILE="./resources/cache.json"
CONFIGURATION_FILE="./resources/config.json"


cc= CurrencyConverter()
db = DataBase(CACHE_FILE, CONFIGURATION_FILE, cc)
db.start()
msc = MarketStatusChecker(30*60)
msc.start()


  
frontEndManager.__init__(1200, 900, db, msc)  
frontEndManager.start()
