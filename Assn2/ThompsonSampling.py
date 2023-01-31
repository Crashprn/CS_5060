import numpy as np


class ThompsonSampling:

    def __init__(self, probs, drift=0, reset = False) -> None:
        self.probs = probs
        self.probN = len(probs())
        self.betaTuples = [[1,1] for i in range(self.probN)]
        self.nArray = [0 for i in range(self.probN)]
        self.picks = []
        self.reward = []
        self.aveReward = []
        self.drift = drift
        self.stepCount = 0
        self.reset = reset


    def stepN(self, iterations: int):
        for i in range(iterations):
            if self.reset and i == 3000:
                self.restart()
            self.step()
    
    def step(self):
        self.stepCount += 1
        samples = [np.random.beta(i[0], i[1]) for i in self.betaTuples]
        choice = np.argmax(samples)
        outcome = 1 if self.probs(self.drift, self.stepCount if self.drift > 0 else 0)[choice] > 0 else 0

        # Add to reward and aveReward
        self.reward.append(outcome)
        self.aveReward.append(sum(self.reward)/self.stepCount)

        # Increment the number of choices
        self.nArray[choice] += 1

        # Update beta Tuples
        self.betaTuples[choice][0] += outcome
        self.betaTuples[choice][1] += (1 - outcome)

        # Update picks
        self.picks.append([n/ (len(self.picks) + 1) for n in self.nArray])

    def restart(self):
        self.betaTuples = [[1,1] for i in range(self.probN)]

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




