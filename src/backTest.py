
from marketAnalyzer import MarketMatrix

KEY_MONTECARLO = "montecarlo"


test = {        
    "types":["d", "wk", "mo"],
    "hystoricalData":[10, 100, 1000, 10000],
    "futureData":[1, 10, 100, 1000, 10000],
    "tests":40,
    "algorithms":[KEY_MONTECARLO]
}

def runBackTesting(title, marketMatrix:MarketMatrix):
    data = marketMatrix.getMarketsData([title], fromDate, toDate, interval, type)
    for a in test["algorithms"]:
        for t in test["types"]:
            for h in test["hystoricalData"]:
                for f in test["futureData"]:
                    if(a==KEY_MONTECARLO):
