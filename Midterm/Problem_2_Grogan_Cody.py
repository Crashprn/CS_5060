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
    def __init__(self, epsilon: float, distibutionGen: t.Callable[[], t.List[float]], baseline: t.Callable[[], float]):
        self.epsilon = epsilon
        self.distributionGen = distibutionGen
        self.probLength = len(self.distributionGen())
        self.baseline = baseline
        
    
    def stepN(self, steps: int):
        self.q = [[0,0,0,0,0]]
        self.qTemporal = np.zeros(5)
        self.n = np.zeros(5)
        self.values = np.zeros(5)
        self.picks = [np.zeros(5)]
        self.stepCount = 0
        self.numberOfPicks = 0
        
        for i in range(steps):
            self.step()

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
            self.q.append(self.q[-1].copy())
            self.picks.append(self.picks[-1].copy())

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
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    numberOfLines = len(arrays[0])
    colormap = plt.cm.nipy_spectral
    
    for i in range(len(arrays)):
        ax[i].set_prop_cycle("color", [colormap(i) for i in np.linspace(0, 1, numberOfLines)])
        ax[i].set_title(figTitle)
        ax[i].set_xlabel(xLabel)
        ax[i].set_ylabel(yLabel[i])
        ax[i].legend(titles)
        
    for array in arrays[0]:
        ax[0].plot(x, array)
    
    for array in arrays[1]:
        ax[1].plot(x, array)
    
    
    fig.savefig(("Figures/Problem_2_" + figTitle + ".png").replace(" ", "_"))

def baseline1():
    return float('-inf')

def baseline2():
    return max(np.random.normal(1.5, 3), 0)

def simulate(baseline: t.Callable[[], float], epsilon: float, figTitle: str):
    distributions = getDistributions
    greedy = EpsilonGreedy(epsilon, distributions, baseline)
    episodes = 300
    steps = 500
        
    overallQ = np.zeros((5, steps+1))
    overallP = np.zeros((5, steps+1))
    for i in range(episodes):
        greedy.stepN(steps)
        x, q = greedy.getQ()
        x_1, p = greedy.getPercentPicks()
        overallQ += q
        overallP += p

    overallQ /= episodes
    overallP /= episodes

    plotArrays(figTitle, ["beta(7,3) + 2", "uniform(0,4)", "beta(3,7) + 2", "normal(2,1.4)", "normal(1.3, 7)"], range(steps+1), [overallQ, overallP], ["Q value", "% picked"], "Steps")
    print(f"Total days: {greedy.stepCount}, Total skipped days: {greedy.stepCount - greedy.numberOfPicks}")
    
    plt.show()


if __name__ == "__main__":
    simulate(baseline1, 0.1, figTitle="Part A")
    simulate(baseline2, 0.1, figTitle="Part B")


