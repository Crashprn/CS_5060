import numpy as np
import matplotlib.pyplot as plt
import os

def payoff(endPrice: float, strikePrice: float):
    return endPrice - strikePrice


class BrownianSimulation:
    def __init__(self, mu: float, vol: float, S_0: float, dt: float, T: float, newVol: float, newMu, newParamTime: int, inflation: float, monthlyProfit: float):
        self.mu = mu
        self.newVol = newVol
        self.newMu = newMu
        self.newParamTime = newParamTime
        self.vol = vol
        self.inflation = inflation
        self.monthlyProfit = monthlyProfit
        self.S_t = S_0
        self.S_0 = S_0
        self.dt = dt
        self.T = T


    def simulateEuro(self):
        path = np.zeros(int(self.T /self.dt))
        self.S_t = self.S_0
        vol = self.vol
        mu = self.mu
        profit = 0
        for i in range(int(self.T /self.dt)):

            if i == self.newParamTime:
                vol = self.newVol
                mu = self.newMu
            
            profit += self.monthlyProfit() / (1 + self.inflation)**(i)

            dW_t =  np.random.normal(0, np.sqrt(self.dt))
            dY_t =  self.S_t * (mu * self.dt + vol * dW_t)
            self.S_t += dY_t
            path[i] = self.S_t / (1 + self.inflation)**(i)

        return (path, profit)
    
    def simulateAmer(self, sellPrice: float):
        path = np.zeros(int(self.T /self.dt))
        path[0] = self.S_0
        self.S_t = self.S_0
        vol = self.vol
        mu = self.mu
        profit = 0
        for i in range(1, int(self.T /self.dt)):
            
            if (path[i - 1] > sellPrice and path[i-1] < path[i-2]) or path[i-1] + profit < self.S_0:
                return (path[0:i], profit)
            
            if i  == self.newParamTime:
                vol = self.newVol
                mu = self.newMu

            profit += self.monthlyProfit()/ (1 + self.inflation)**(i)

            dW_t =  np.random.normal(0, np.sqrt(self.dt))
            dY_t =  self.S_t * (mu * self.dt + vol * dW_t)
            self.S_t += dY_t
            path[i] = self.S_t / (1 + self.inflation)**(i)
        
        return (path, profit)
        



def plotArrays(figTitle, saveFile, y_title, arrays: list[np.ndarray], x_title = "Time steps"):
    # Matplotlib Figure config
    fig, ax = plt.subplots(figsize=(10,7))
    numberOfPlots = len(arrays)
    colormap = plt.cm.nipy_spectral
    ax.set_prop_cycle('color',[colormap(i) for i in np.linspace(0, 1, numberOfPlots)])
    ax.set_title(figTitle)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.ticklabel_format(style='plain')
    
    # Plotting data
    for array in arrays:
        x = np.arange(0, array.shape[0])
        ax.plot(x, array)
    
    fig.savefig(os.path.join("Figures", saveFile))

    
def simulate(saveSuffix: str, newVol: float, newDrift, newVolTime: float):
    startPrice = 385_000
    T = 10
    dt = 1/12
    sellPrice = 535_000.
    drift = 0.04
    vol = 0.03
    inflation = np.random.normal(0.04, 0.01) * dt
    monthlyProfit = lambda : 0
    numPaths = 1000

    sim = BrownianSimulation(drift, vol, startPrice, dt, T, newVol, newDrift, int(newVolTime / dt), inflation, monthlyProfit)
    
    amerPaths = [sim.simulateAmer(sellPrice) for i in range(numPaths)]

    plotArrays("American Selling Model", "amerCall" + saveSuffix + ".png", "Price in Today's Dollars", [path[0] for path in amerPaths])
    averageSellPriceAmer = np.average([payoff(path[0][-1], startPrice) + path[1] for path in amerPaths])
    print(f"Average Profit From Selling Anytime: {averageSellPriceAmer:.4f}")

    euroPaths = [sim.simulateEuro() for i in range(numPaths)]

    plotArrays("European Selling Model", "euroCall" + saveSuffix + ".png", "Price in Today's Dollars", [path[0] for path in euroPaths])
    averageSellPriceEuro = np.average([payoff(path[0][-1] + path[1], startPrice) for path in euroPaths])
    print(f"Average Profit From Selling after 10 years: {averageSellPriceEuro:.4f}")

    paths = [sim.simulateAmer(sellPrice) for i in range(numPaths)]


    plt.show()


if __name__ == "__main__":
    simulate("", 0.03, 0.04, 5)
    print("--------------------------------------------------")
    simulate("VolInjection", 0.19, 0.04, 5)

