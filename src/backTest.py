
from marketAnalyzer import MarketMatrix
import math
import prevision

KEY_MONTECARLO = "montecarlo"

KEYS_PREVISIONS = [KEY_MONTECARLO]

testConfig = {        
    "types":["d", "wk", "mo"],
    "hystoricalData":[10, 100, 1000, 10000],
    "futureData":[1, 10, 100, 1000, 10000],
    "simulations":[50, 500, 5000],
    "tests":40,
    "algorithms":[prevision.calculateMontecarloV2]
}


def checkPrevision(data, previsionFunction,  hystoricalData, futureData, simulations, tests):
    remainingData = len(data)-hystoricalData-futureData+1
    if(remainingData<=0):
        return []
    tests = min(tests, remainingData)
    step = remainingData/tests
    errors = []
    for t in range(tests):
        pivot = len(remainingData)-1 - futureData - t*step
        prev = previsionFunction(data[pivot-(hystoricalData-1):pivot+1], simulations, futureData)
        lastValue = prev[-1]
        realValue = data[pivot+futureData]["value"]
        errorPerc = (lastValue-realValue)*100/realValue
        errors.append(errorPerc)
    return errors
        
        


def runBackTesting(title, marketMatrix:MarketMatrix):
    data = {"d": marketMatrix.getMarketsData([title], 0, math.inf, "d", type),
        "wk": marketMatrix.getMarketsData([title], 0, math.inf, "wk", type),
        "mo": marketMatrix.getMarketsData([title], 0, math.inf, "mo", type)}
    
    for a in testConfig["algorithms"]:
        for t in testConfig["types"]:
            for h in testConfig["hystoricalData"]:
                for f in testConfig["futureData"]:
                    for s in testConfig["simulations"]:
                        if(a.__module__ == prevision.__name__):
                            errors = checkPrevision(data[t], a, h, f, s, testConfig["tests"])
                            errors += ["N/D"]*(testConfig["tests"]-len(errors))