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
    
    return final_mean

    

def calculateMontecarloGeometricBrownianMotion(data, simulations, futureDataNum):
    vals = [v["value"] for v in data]
    initialPortfolio = vals[-1]
    dfInput = pd.DataFrame([vals]).T

    ret = np.log(1+dfInput.pct_change())
    df = dfInput
    mean = ret.mean()[0]
    std = ret.std()[0]
    
    
    mu = mean
    n = futureDataNum  # Number of intervals
    T = futureDataNum/252  # Time in years
    M = simulations  # Number of simulations
    S0 = initialPortfolio  # Initial stock price
    sigma = std  # Volatility

    # Calculate each time step
    dt = T / n

    np.random.seed(42)
    St = np.exp(
        (mu - sigma ** 2 / 2) * dt
        + sigma * np.random.normal(0, np.sqrt(dt), size=(M, n)).T
    )

    St = S0 * St.cumprod(axis=0)

    final_mean = []
    for i in range(futureDataNum):
        final_mean.append(St[i].mean())
    return final_mean

def calculateHeston(data, simulations, futureDataNum):
    vals = [v["value"] for v in data]
    initialPortfolio = vals[-1]
    dfInput = pd.DataFrame([vals]).T

    ret = np.log(1+dfInput.pct_change())

    std = ret.std()[0]
    # Calculate parameters for the Heston model
    kappa = 2  # Mean reversion speed of variance
    theta = std ** 2  # Long-term average variance
    sigma = std  # Volatility of volatility
    rho = -0.5  # Correlation between the stock price and its volatility

    # Heston model parameters
    S0 = initialPortfolio  # Initial stock price
    r = 0.05  # Risk-free interest rate
    T = futureDataNum/252  # Time to maturity (in years)
    N = futureDataNum  # Number of time steps
    dt = T / N  # Time increment
    num_simulations = simulations  # Number of simulations

    # Simulate stock prices using the Heston model
    #np.random.seed(42)
    simulations_hm = []

    plt.figure(figsize=(12, 6))

    for i in range(num_simulations):
        V = np.zeros(N+1)
        V[0] = theta

        for t in range(1, N+1):
            #dz1 used to model the randomness or noise in the volatility process.
            dZ1 = np.random.normal(0, np.sqrt(dt))
            # generated to introduce correlation between the stock price and its volatility. 
            dZ2 = rho * dZ1 + np.sqrt(1 - rho**2) * np.random.normal(0, np.sqrt(dt))
            # generated to introduce correlation between the stock price and its volatility. mean reversion
            V[t] = V[t-1] + kappa * (theta - V[t-1]) * dt + sigma * np.sqrt(V[t-1]) * dZ2

        S = np.zeros(N+1)
        S[0] = S0

        for t in range(1, N+1):
            dW = np.random.normal(0, np.sqrt(dt))
            S[t] = S[t-1] * np.exp((r - 0.5 * V[t]) * dt + np.sqrt(V[t]) * dW)

        #df_heston = pd.DataFrame(S)
        simulations_hm.append(S)
    
    df = pd.DataFrame(simulations_hm)

    finalMean = []
    for i in range(futureDataNum):
        finalMean.append(df[i].mean())
    return finalMean

    
    