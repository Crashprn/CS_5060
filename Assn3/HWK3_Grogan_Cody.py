import numpy as np
import matplotlib.pyplot as plt
import os
import math
import multiprocessing


def callPayoff(strike, current):
    return max(0, current - strike)

class BrownianSimulation:
    def __init__(self, mu: float, vol: float, S_0: float, dt: float, T: float):
        self.mu = mu
        self.vol = vol
        self.S_t = S_0
        self.S_0 = S_0
        self.dt = dt
        self.T = T
    
    
    def simulate(self):
        paths = []
        
        for i in range(int(self.T /self.dt)):
            dW_t =  np.random.beta(14,6) - 0.85
            
            paths.append(self.S_0 * math.exp((self.mu - self.vol**2/2) * (i * self.dt) + self.vol * dW_t))
            #dW_t = np.random.normal(0, np.sqrt(self.dt))
            #dY_t =  self.mu * self.dt + self.vol * dW_t
            #paths.append(paths[-1] + dY_t)

            
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
    
    brownians = [BrownianSimulation(drift, volatility, S_0, dt, T) for i in range(pathNum)]
    with multiprocessing.Pool() as pool:
        paths = pool.map(callSimulate, brownians)
    
    plotArrays("Brownian motion", "Brownian", "Stock Price $", range(365), paths, "Days")
    
    riskFree = 1.01
    payoffs = [callPayoff(S_0, path[-1]/riskFree) for path in paths]
    
    callBinPrice = np.average(payoffs) * 100
    print(f"Sell price for 100 European Call Options is : {callBinPrice}")
    
    
def main():
    problem1()

    plt.show()
if __name__ == "__main__":
    main()