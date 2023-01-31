import typing
import numpy as np

class EpsilonGreedy:

    def __init__(self, probablilities: typing.Callable[[None], typing.List[float]], epsilon: float, drift: float = 0) -> None:
        self.probs = probablilities
        self.probN = len(self.probs())
        self.values = [0 for i in range(self.probN)]
        self.nArray = [0 for i in range(self.probN)]
        self.q = [[0 for i in range(self.probN)]]
        self.qTemporal = [0 for i in range(self.probN)]
        self.picks = []
        self.epsilon = epsilon
        self.reward = []
        self.aveReward = []
        self.drift = drift
        self.stepCount = 0

    def stepN(self,iterations: int):
        for i in range(iterations):
            self.step()

    def step(self):
        self.stepCount += 1

        if np.random.random()  < self.epsilon:
            choice =  np.random.randint(0,self.probN)
        else:
            choice = np.argmax(self.qTemporal)
            #choice = np.argmax(self.q[-1])
        
        # Get Result
        outcome = self.probs(self.drift, self.stepCount if self.drift > 0 else 0)[choice]

        # Add to reward and aveReward
        self.reward.append(1 if outcome > 0 else 0)
        self.aveReward.append(sum(self.reward)/ self.stepCount)

        # Add result to values
        self.values[choice] += outcome
        self.nArray[choice] += 1

        # Create new q array and add to history
        self.q.append([self.divide(i,j) for i,j in zip(self.values, self.nArray)])
        self.qTemporal[choice] += self.divide(outcome - self.qTemporal[choice], self.nArray[choice])

        # Update picks
        self.picks.append([n/ self.stepCount for n in self.nArray])

    def getQ(self):
        x = [i for i in range(self.stepCount)]
        return x, self.breakIntoSubArrays(self.q, self.probN)

    def getPercentPicks(self):
        x = [i for i in range(self.stepCount)]
        return x, self.breakIntoSubArrays(self.picks, self.probN)
    
    def getAveReward(self):
        x = [i for i in range(len(self.aveReward))]
        return x, self.aveReward

    @staticmethod
    def breakIntoSubArrays(arrays, n):
        valueArrays = []
        for i in range(n):
            y = []
            for array in arrays:
                y.append(array[i])
            valueArrays.append(y)
        return valueArrays

    @staticmethod
    def divide(n, d):
        return 0 if d == 0 else n/d




