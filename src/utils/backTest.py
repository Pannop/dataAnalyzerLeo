
from marketAnalyzer import MarketMatrix
import math
from utils import indicators
from collections import defaultdict

KEY_MONTECARLO = "montecarlo"

KEYS_PREVISIONS = [KEY_MONTECARLO]

testConfig = {        
    "types":["d", "wk", "mo"],
    "historicalData":[10, 100, 1000, 7000],
    "futureData":[1, 10, 100, 1000, 5000],
    "simulations":[1000, 5000],
    "tests":10,
    "algorithms":[indicators.calculateMontecarloV2]
}


def checkPrevision(data, previsionFunction,  historicalData, futureData, simulations, tests):
    remainingData = len(data)-historicalData-futureData+1
    if(remainingData<=0):
        return []
    tests = min(tests, remainingData)
    step = int(remainingData/tests)
    print(len(data), step, tests)
    errors = []
    for t in range(tests):
        pivot = len(data)-1 - futureData - t*step
        prev = previsionFunction(data[pivot-(historicalData-1):pivot+1], simulations, futureData)
        prevDelta = prev[-1]-data[pivot]["value"]
        realDelta = data[pivot+futureData]["value"]-data[pivot]["value"]
        if(realDelta==0):
            continue
        errorPerc = round(prevDelta/realDelta, 2)
        errors.append(errorPerc)

            
        
    return errors
        
        

class AutoCreatingDict(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            self[key] = AutoCreatingDict()
            return self[key]
            

            

def runBackTesting(title, marketMatrix:MarketMatrix):
    data = {"d": marketMatrix.getMarketsData([title], "1980-01-01", "2040-01-01", "d", "close"),
        "wk": marketMatrix.getMarketsData([title], "1980-01-01", "2040-01-01", "wk", "close"),
        "mo": marketMatrix.getMarketsData([title], "1980-01-01", "2040-01-01", "mo", "close")}
    testsResults = AutoCreatingDict()
    testsResultsSummary = AutoCreatingDict()

    for a in testConfig["algorithms"]:
        for t in testConfig["types"]:
            for h in testConfig["historicalData"]:
                for f in testConfig["futureData"]:
                    for s in testConfig["simulations"]:
                        if(a.__module__ == indicators.__name__):
                            print(a.__name__, t, h, f, s)
                            errors = checkPrevision(data[t][title], a, h, f, s, testConfig["tests"])
                            testsResultsSummary[a.__name__][t][str(h)][str(f)][str(s)] = ("N/D" if len(errors)==0 else round(sum(errors)/len(errors), 3))
                            errors += ["N/D"]*(testConfig["tests"]-len(errors))
                            testsResults[a.__name__][t][str(h)][str(f)][str(s)] = errors
    return testsResults, testsResultsSummary


