import numpy as np
import typing as t
import matplotlib.pyplot as plt



def getDistributions()-> t.List[float]:
    distributions = [
        np.random.beta(7,3) + 2,
        np.random.uniform(0,4),
        np.random.beta(3,7) + 2,
        np.random.normal(2,1.4),
        np.random.normal(1.3, 7)
    ]
    return distributions

class EpsilonGreedy():
    def __init__(self, epsilon: float, distibutionGen: t.Callable[[], t.List[float]], baseline: t.Callable[[], float], minSteps: int):
        self.epsilon = epsilon
        self.distributionGen = distibutionGen
        self.probLength = len(self.distributionGen())
        self.baseline = baseline
        self.q = [[0,0,0,0,0]]
        self.qTemporal = np.zeros(5)
        self.n = np.zeros(5)
        self.values = np.zeros(5)
        self.picks = [np.zeros(5)]
        self.stepCount = 0
        self.numberOfPicks = 0
        self.minSteps = minSteps

    def stepTillConvergence(self):
        while True:
            self.step()
            if self.stepCount > self.minSteps and self.picks[-1][np.argmax(self.picks[-1])] > 0.5:
                break

                    

    def step(self):
        self.stepCount += 1
        if np.random.random() < self.epsilon:
            choice = np.random.randint(0, self.probLength)
        else:
            choice = np.argmax(self.q[-1])

        # Get Outcome from probaility generator
        outcome = self.distributionGen()[choice]
        baseline = self.baseline()
        # Check if outcome is greater than baseline
        if outcome > baseline:
            self.numberOfPicks += 1

            # Add outcome to values and increment n
            self.values[choice] += outcome
            self.n[choice] += 1

            # Update q and qTemporal
            self.qTemporal[choice] += self.divide(outcome - self.qTemporal[choice], self.n[choice])
            self.q.append(self.qTemporal.copy())

            # Update picks
            self.picks.append(np.array([n / self.numberOfPicks for n in self.n]))

        else:
            self.q.append(self.q[-1])
            self.picks.append(self.picks[-1])

    def getQ(self):
        x = range(len(self.q))
        return x, self.breakIntoSubArrays(self.q, self.probLength)

    def getPercentPicks(self):
        x = range(self.stepCount + 1)
        return x, self.breakIntoSubArrays(self.picks, self.probLength)
    
    @staticmethod
    def breakIntoSubArrays(arrays, n):
        valueArrays = np.zeros((n, len(arrays)), dtype='float32')
        for i in range(len(arrays)):
            for j in range(n):
                valueArrays[j][i] = arrays[i][j]
        
        return valueArrays
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            return 0
        return a / b
    
def plotArrays(figTitle: str, titles: t.List[str], x: t.List[int], arrays: t.List[t.List[float]], yLabel: str = "Y", xLabel: str = "X"):
    fig, ax = plt.subplots(figsize=(7,7))
    numberOfLines = len(arrays)
    colormap = plt.cm.nipy_spectral
    ax.set_prop_cycle("color", [colormap(i) for i in np.linspace(0, 1, numberOfLines)])
    ax.set_title(figTitle)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)

    for i in range(len(arrays)):
        ax.plot(x, arrays[i])
    
    ax.legend(titles)

def baseline1():
    return float('-inf')

def baseline2():
    return max(np.random.normal(1.5, 3), 0)

def simulate(baseline: t.Callable[[], float], epsilon: float, minSteps: int, figTitle: str):
    distributions = getDistributions
    greedy = EpsilonGreedy(epsilon, distributions, baseline, minSteps)

    greedy.stepTillConvergence()

    x, q = greedy.getQ()
    x_1, p_1 = greedy.getPercentPicks()


    plotArrays(figTitle, ["beta(7,3) + 2", "uniform(0,4)", "beta(3,7) + 2", "normal(2,1.4)", "normal(1.3, 7)"], x, q, "% Picks", "Steps")
    plt.show()


if __name__ == "__main__":
    simulate(baseline1, 0.1, 100, figTitle="Problem 1")
    simulate(baseline2, 0.2, 1000, figTitle="Problem 2")


