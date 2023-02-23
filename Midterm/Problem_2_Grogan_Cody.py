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
        self.q = [np.zeros(5)]
        self.qTemporal = np.zeros(5)
        self.n = np.zeros(5)
        self.values = np.zeros(5)
        self.picks = [np.zeros(5)]
        self.stepCount = 0
    
    def stepTillConvergence(self):
        Done = False
        while not Done:
            self.step()
            curDone = True
            for prevQ, currQ in zip(self.q[-2], self.q[-1]):
                if abs(prevQ - currQ) < 0.001:
                    curDone = Done and True
                else:
                    curDone = False
            Done = curDone
                    

    def step(self):
        self.stepCount += 1
        if np.random.random() < self.epsilon:
            choice = np.random.randint(0, self.probLength)
        else:
            choice = np.argmax(self.q)
        print(choice)
        # Get Outcome from probaility generator
        outcome = self.distributionGen()[choice]

        # Check if outcome is greater than baseline
        if outcome < self.baseline():
            return
        
        
        # Add outcome to values and increment n
        self.values[choice] += outcome
        self.n[choice] += 1

        # Update q and qTemporal
        self.qTemporal[choice] += self.divide(outcome - self.qTemporal[choice], self.n[choice])
        self.q.append(self.qTemporal.copy())

        # Update picks
        self.picks.append(np.array([n / self.stepCount for n in self.n]))

    def getQ(self):
        x = [i for i in range(self.stepCount)]
        return x, self.breakIntoSubArrays(self.q, self.probN)

    def getPercentPicks(self):
        x = [i for i in range(self.stepCount)]
        return x, self.breakIntoSubArrays(self.picks, self.probN)
    
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

def problem1():
    epsilon = 0.1
    distributions = getDistributions
    baseline = baseline1
    greedy = EpsilonGreedy(epsilon, distributions, baseline)

    greedy.stepTillConvergence()

    x, q = greedy.getQ()
    plotArrays("Problem 1", ["Epsilon 0.l"], x, [q], "Q", "Steps")


if __name__ == "__main__":
    problem1()


