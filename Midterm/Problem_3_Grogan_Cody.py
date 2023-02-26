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
        derivative = 0
        profit = 0
        for i in range(1, int(self.T /self.dt)):
            
            if (path[i - 1] > sellPrice and derivative < 0) or path[i-1] + profit< self.S_0:
                return (path[0:i], profit)
            
            if i  == self.newParamTime:
                vol = self.newVol
                mu = self.newMu
            if i > 4:
                var = np.poly1d(np.polyfit(np.arange(0, 4), path[i-4:i].copy(), 3))
                derivative = var.deriv()(4)

            profit += self.monthlyProfit()/ (1 + self.inflation)**(i)

            dW_t =  np.random.normal(0, np.sqrt(self.dt))
            dY_t =  self.S_t * (mu * self.dt + vol * dW_t)
            self.S_t += dY_t
            path[i] = self.S_t / (1 + self.inflation)**(i)
        
        return (path, profit)
        



def plotArrays(figTitle, saveFile, arrays: list[list[np.ndarray]],y_title= "Today's Dollars", x_title = "Time steps"):
    # Matplotlib Figure config
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    numberOfLines = len(arrays[0])
    colormap = plt.cm.nipy_spectral
    
    for i in range(len(arrays)):
        ax[i].set_prop_cycle("color", [colormap(i) for i in np.linspace(0, 1, numberOfLines)])
        ax[i].set_title(figTitle[i])
        ax[i].set_xlabel(x_title)
        ax[i].set_ylabel(y_title)
        
    for array in arrays[0]:
        ax[0].plot(range(len(array)), array)
    
    for array in arrays[1]:
        ax[1].plot(range(len(array)), array)
    
    fig.savefig(os.path.join("Figures", saveFile))

    
def simulate(savePrefix: str, newVol: float, newDrift, newVolTime: float):
    startPrice = 385_000
    T = 10
    dt = 1/12
    sellPrice = 535_000
    drift = 0.04
    vol = 0.03
    inflation = np.random.normal(0.04, 0.01) * dt
    monthlyProfit = lambda : np.random.normal(1000, 1000)
    numPaths = 10000

    sim = BrownianSimulation(drift, vol, startPrice, dt, T, newVol, newDrift, int(newVolTime / dt), inflation, monthlyProfit)
    
    # American style
    amerPaths = [sim.simulateAmer(sellPrice) for i in range(numPaths)]
    averageSellPriceAmer = np.average([payoff(path[0][-1], startPrice) for path in amerPaths])
    averageProfitAmer = np.average([path[1] for path in amerPaths])
    print(f"American style lease-to-own")
    print(f"\tAverage Profit: {averageSellPriceAmer + averageProfitAmer:.4f}")
    print(f"\tAverage Store Price: {averageSellPriceAmer:.4f}")

    # European style
    euroPaths = [sim.simulateEuro() for i in range(numPaths)]
    averageSellPriceEuro = np.average([payoff(path[0][-1], startPrice) for path in euroPaths])
    averageProfitEuro = np.average([path[1] for path in euroPaths])
    print(f"European style lease-to-own:")
    print(f"\tAverage Profit: {averageSellPriceEuro + averageProfitEuro:.4f}")
    print(f"\tAverage Store Price: {averageSellPriceEuro:.4f}")

    # Plotting
    plotArrays(["American Selling Model", "European Selling Model"], savePrefix + "VolInjection" + ".png", [[path[0] for path in amerPaths], [path[0] for path in euroPaths]])
    
    plt.show()


if __name__ == "__main__":
    simulate("No", 0.03, 0.04, 5)
    print("--------------------------------------------------")
    simulate("", 0.19, 0.04, 5)

