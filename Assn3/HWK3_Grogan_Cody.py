import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from fitter import Fitter
from scipy import stats

def callPayoff(strike, current):
    return max(0, current - strike)

def callPayoffAve(target, price1, price2):
    return max(0, target - (price1 + price2)/2)

def callPayoffMax(target, price1, price2):
    return max(0, target - max(price1, price2))

class BrownianSimulation:
    def __init__(self, mu: float, vol: float, S_0: float, dt: float, T: float, random ):
        self.mu = mu
        self.vol = vol
        self.S_t = S_0
        self.S_0 = S_0
        self.dt = dt
        self.T = T
        self.random = random
    
    
    def simulate(self):
        paths = []
        
        for i in range(int(self.T /self.dt)):
            dW_t =  self.random()
            dY_t =  self.mu * self.dt + self.vol * dW_t
            self.S_t += dY_t
            paths.append(self.S_t)

            
        return paths    

def plotArrays(figTitle, saveFile, y_title, x, arrays, x_title = "Time steps"):
    # Matplotlib Figure config
    fig, ax = plt.subplots(figsize=(10,7))
    numberOfPlots = len(arrays)
    colormap = plt.cm.nipy_spectral
    ax.set_prop_cycle('color',[colormap(i) for i in np.linspace(0, 1, numberOfPlots)])
    ax.set_title(figTitle)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    
    # Plotting data
    for array in arrays:
        ax.plot(x, array)
    
    aves = arrays[0]
    # Plotting Average Line
    for array in arrays[1:]:
        for i in range(len(array)):
            aves[i] += array[i]

    aves = np.divide(aves, len(arrays))

    ax.plot(x,aves)
        
    fig.savefig(os.path.join("Figures", saveFile))

def callSimulate(obj: BrownianSimulation):
    return obj.simulate()

def problem1():
    volatility = 0.5
    drift = 0.01
    dt = 1/365
    T = 1
    S_0 = 100
    pathNum = 5000
    randoms = lambda : np.random.beta(14,6) - .65
    
    brownians = [BrownianSimulation(drift, volatility, S_0, dt, T, randoms) for i in range(pathNum)] 
    paths = [b.simulate() for b in brownians]
    
    riskFree = 1.01
    payoffs = [callPayoff(S_0, path[-1]/riskFree) for path in paths]
    
    callBinPrice = np.average(payoffs) * 100
    print(f"Sell price for 100 European Call Options is : {callBinPrice}")

    plotArrays("Predicted Target Stock Price", "TargetGraph.png", "Stock Price $", range(365), paths, "Days")


def problem2():
    distributions = ['beta', 'lognorm', 'norm']
    dataset1 = pd.read_csv('Data/stock1.csv')
    dataset2 = pd.read_csv('Data/stock2-1.csv')

    #sns.displot(data=dataset1, x='Stock Price', kind="hist", bins=100, aspect=1.5)
    #sns.displot(data=dataset2, x='Stock Price', kind="hist", bins=100, aspect=1.5)

    price1 = dataset1["Stock Price"].values
    price2 = dataset2["Stock Price"].values

    # Normalizing data
    max1 = max(price1)
    min1 = min(price1)  
    for i in range(len(price1)):
        price1[i] = (price1[i] - min1)/(max1 - min1)

    max2 = max(price2)
    min2 = min(price2)  
    for i in range(len(price2)):
        price2[i] = (price2[i] - min2)/(max2 - min2)
    
    shift1 = (100 - min1)/(max1 - min1)
    shift2 = (100 - min2)/(max2 - min2)

    # Fitting first price set
    f = Fitter(price1, distributions=distributions)
    f.fit(progress=False)
    params1 = f.get_best(method = 'sumsquare_error')['lognorm']
    print("---Stock 1 Fit Info---")
    print(f.summary())
    print(f"Best fit Lognormal with params s: {params1['s']:.4f}, location: {params1['loc']}, scale: {params1['scale']}")

    # Plotting distribution with shift line for sanity
    
    fig, ax = plt.subplots(figsize=(10,7))
    r = stats.lognorm.rvs(s=params1["s"], loc=params1['loc'], scale=params1['scale'], size=1000)
    ax.hist(r, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
    ax.plot([shift1 for i in range(200)], [.01 * i for i in range(200)])
    


    # Fitting second price set
    f = Fitter(price2, distributions=distributions)
    f.fit(progress=False)
    params2 = f.get_best(method = 'sumsquare_error')['lognorm']

    print("---Stock 2 Fit Info---")
    print(f.summary())
    print(f"Best fit Lognormal with params s: {params2['s']:.4f}, location: {params2['loc']}, scale: {params2['scale']}")

    # Plotting distribution with shift line for sanity
    
    fig, ax = plt.subplots(figsize=(10,7))
    r = stats.lognorm.rvs(s=params2["s"], loc=params2['loc'], scale=params2['scale'], size=1000)
    ax.hist(r, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
    ax.plot([shift2 for i in range(200)], [.01 * i for i in range(200)])
    plt.show()

    # Performing simulation
    volatility = 0.5
    drift = 0.01
    dt = 1/365
    T = 1
    S_0 = 100
    pathNum = 5000
    riskFree = 1.01

    # Calculating S_0 shift in normalized data
    shift1 = (S_0 - min1)/(max1 - min1)
    shift2 = (S_0 - min2)/(max2 - min2)

    # Random lambdas
    targetRandom = lambda : np.random.beta(14,6) - .65
    random1 = lambda params=params1, shift=shift1 : stats.lognorm.rvs(s=params["s"], loc=params['loc'], scale=params['scale']) - shift
    random2 = lambda params=params2, shift=shift2 : stats.lognorm.rvs(s=params["s"], loc=params['loc'], scale=params['scale']) - shift

    targetBrownians = [BrownianSimulation(drift, volatility, S_0, dt, T, targetRandom) for i in range(pathNum)]
    brownians1 = [BrownianSimulation(drift, volatility, S_0, dt, T, random1) for i in range(pathNum)]
    brownians2 = [BrownianSimulation(drift, volatility, S_0, dt, T, random2) for i in range(pathNum)]

    targetPaths = [b.simulate() for b in targetBrownians]
    paths1 = [b.simulate() for b in brownians1]
    paths2 = [b.simulate() for b in brownians2]
    
    avePayoff = []
    maxPayoff = []
    for target, path1, path2 in zip(targetPaths, paths1, paths2):
        avePayoff.append(callPayoffAve(target[-1]/riskFree, path1[-1], path2[-1]))
        maxPayoff.append(callPayoffMax(target[-1]/riskFree, path1[-1], path2[-1]))

    aveBinPrice = np.average(avePayoff) * 100
    maxBinPrice = np.average(maxPayoff) * 100

    print(f'Sell price for European Call Option with average of 2 other stocks: {aveBinPrice:.2f}')
    print(f'Sell price for European Call Option with max of 2 other stocks: {maxBinPrice:.2f}')

    plotArrays("Predicted 1st Stock Price", "Stock1Graph.png", "Stock Price $", range(365), paths1, "Days")
    plotArrays("Predicted 2nd Stock Price", "Stock2Graph.png", "Stock Price $", range(365), paths2, "Days")

    
    


def main():
    #problem1()
    #plt.show()
    problem2()
    plt.show()
    


if __name__ == "__main__":
    main()