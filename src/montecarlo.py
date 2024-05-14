import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt


def calculateMontecarlo(data, simulations, futureDataNum):
    initialPrice = data[-1]["value"]
    values = [v["value"] for v in data]
    logs = [v["log"] for v in data]
    mean = sum(logs)/len(logs)
    var = np.var(logs)
    std = np.std(logs)
    drift = mean - (var/2)
    
    daily_ret = np.exp(drift + std * np.random.normal(0, size=(simulations, futureDataNum)).T)
    new_data = np.zeros_like(daily_ret)
    new_data = initialPrice * daily_ret.cumprod(axis = 0)
    final_mean = []
    for i in range(len(new_data)):
        final_mean.append(new_data[i].mean())



    plt.plot(new_data)
    plt.show()
    print(final_mean[-1])
    plt.plot(final_mean)
    plt.show()



def calculateMontecarloV2(data, simulations, futureDataNum):

    vals = [v["value"] for v in data]
    initialPortfolio = vals[-1]
    dfInput = pd.DataFrame([vals]).T
    ret = dfInput.pct_change()
    mean = ret.mean()
    cov = ret.cov()

    weights = [1]

    meanM = np.full(shape=(futureDataNum, len(weights)), fill_value=mean).T
    portfolio_sim = np.full(shape=(futureDataNum, simulations), fill_value=0.0)
    for s in range(simulations):
        z = np.random.normal(size=(futureDataNum, len(weights)))
        l = np.linalg.cholesky(cov)
        dailyRet = meanM + np.inner(l, z)
        portfolio_sim[:,s] = np.cumprod(np.inner(weights, dailyRet.T)+1)*initialPortfolio
    
    final_mean = []
    for i in range(len(portfolio_sim)):
        final_mean.append(portfolio_sim[i].mean())
    
    plt.plot(portfolio_sim)
    plt.show()
    print(final_mean[-1])
    plt.plot(final_mean)
    plt.show()

    





    
    