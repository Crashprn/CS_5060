import numpy as np


class ThompsonSampling:

    def __init__(self, probs, drift=0, reset = False) -> None:
        self.probs = probs
        self.probN = len(probs())
        self.betaTuples = [[1,1] for i in range(self.probN)]
        self.values = [0 for i in range(self.probN)]
        self.nArray = [0 for i in range(self.probN)]
        self.picks = []
        self.reward = []
        self.aveReward = []
        self.drift = drift
        self.stepCount = 0
        self.reset = reset
        self.q = [[0 for i in range(self.probN)]]


    def stepN(self, iterations: int):
        for i in range(iterations):
            if self.reset and i == 3000:
                self.restart()
            self.step()
    
    def step(self):
        self.stepCount += 1
        samples = [np.random.beta(i[0], i[1]) for i in self.betaTuples]
        choice = np.argmax(samples)
        value = self.probs(self.drift, self.stepCount if self.drift > 0 else 0)[choice]
        outcome = 1 if value > 0 else 0

        # Add to reward and aveReward
        self.reward.append(outcome)
        self.aveReward.append(sum(self.reward)/self.stepCount)

        # Increment the number of choices and add value
        self.nArray[choice] += 1
        self.values[choice] += value

        # Update beta Tuples
        self.betaTuples[choice][0] += outcome
        self.betaTuples[choice][1] += (1 - outcome)

        # Create new q array and add to history
        self.q.append([self.divide(i,j) for i,j in zip(self.values, self.nArray)])

        # Update picks
        self.picks.append([n/ (len(self.picks) + 1) for n in self.nArray])

    def restart(self):
        self.betaTuples = [[1,1] for i in range(self.probN)]

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




