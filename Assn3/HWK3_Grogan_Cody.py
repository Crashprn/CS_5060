import numpy as np
import matplotlib.pyplot as plt
import os
import math
import multiprocessing
import pandas as pd
import seaborn as sns
from fitter import Fitter, get_common_distributions
from scipy import stats

def callPayoff(strike, current):
    return max(0, current - strike)

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
            
            #paths.append(self.S_0 * math.exp((self.mu - self.vol**2/2) * (i * self.dt) + self.vol * dW_t))
            #dW_t = np.random.normal(0, np.sqrt(self.dt))
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
    randoms = lambda : np.random.beta(14,6) - .7
    
    brownians = [BrownianSimulation(drift, volatility, S_0, dt, T, randoms) for i in range(pathNum)] 
    paths = [b.simulate() for b in brownians]
    plotArrays("Brownian motion", "Brownian", "Stock Price $", range(365), paths, "Days")
    
    riskFree = 1.01
    payoffs = [callPayoff(S_0, path[-1]/riskFree) for path in paths]
    
    callBinPrice = np.average(payoffs) * 100
    print(f"Sell price for 100 European Call Options is : {callBinPrice}")



def problem2():
    dataset1 = pd.read_csv('Data/stock1.csv')
    dataset2 = pd.read_csv('Data/stock2-1.csv')

    price1 = dataset1["Stock Price"].values
    
    f = Fitter(price1, distributions=get_common_distributions())
    f.fit(progress=False)
    params1 = f.get_best(method = 'sumsquare_error')["lognorm"]
    random1 = lambda params=params1 : stats.lognorm.rvs(s=params["s"]) - 1

    volatility = 0.5
    drift = 0.01
    dt = 1/365
    T = 1
    S_0 = 100
    pathNum = 5000
    
    brownians1 = [BrownianSimulation(drift, volatility, S_0, dt, T, random1) for i in range(pathNum)]

    paths1 = [b.simulate() for b in brownians1]
    
    plotArrays("Brownian motion", "Brownian1", "Stock Price $", range(365), paths1, "Days")


    price2 = dataset2["Stock Price"].values
    
    f = Fitter(price2, distributions=get_common_distributions())
    f.fit(progress=False)
    params2 = f.get_best(method = 'sumsquare_error')["chi2"]
    print(params2)
    random2 = lambda params=params2 : stats.chi2.rvs(df=params["df"]) - 1

    volatility = 0.5
    drift = 0.01
    dt = 1/365
    T = 1
    S_0 = 100
    pathNum = 5000
    
    brownians2 = [BrownianSimulation(drift, volatility, S_0, dt, T, random2) for i in range(pathNum)]

    paths2 = [b.simulate() for b in brownians2]
    
    plotArrays("Brownian motion", "Brownian2", "Stock Price $", range(365), paths2, "Days")
    

    
    


def main():
    #problem1()
    problem2()
    
    plt.show()


if __name__ == "__main__":
    main()