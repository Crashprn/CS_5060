import numpy as np
import typing as t
import matplotlib.pyplot as plt
import os
import multiprocessing
import time

class OptimalStopping:

    def __init__(self, rejectPercent: float, rejectDrift: float, numTrials: int, numElements: int, numRange: t.Tuple[int, int], buffershift: t.Tuple[int, int] = (4, 0)):
        self.random = np.random.randint
        self.numElements = numElements
        self.numTrials = numTrials
        self.reject = rejectPercent
        self.rejectDrift = rejectDrift
        self.numMin = numRange[0]
        self.numMax = numRange[1]
        self.bufferLeft = buffershift[0]
        self.bufferRight = buffershift[1]

    
    def getOptimalStopping(self) -> t.Tuple[np.ndarray, np.ndarray]:
        successfulStops = np.zeros(self.numElements)
        stops = np.zeros(self.numElements)
        
        with multiprocessing.Pool() as pool:
            for result in pool.map(self.stop, self.generateRandomArrays()):
                successful, stop = result
                successfulStops = np.add(successfulStops, successful)
                stops = np.add(stops, stop)
        
        '''
        for trial in self.generateRandomArrays():
            successful, stop = self.stop(trial)
            successfulStops = np.add(successfulStops, successful)
            stops = np.add(stops, stop)
        '''
        return successfulStops, stops

    def stop(self, trial: np.ndarray) -> t.Tuple[np.ndarray, np.ndarray]:
        optimalNumber = max(trial)
        successfulStops = np.zeros(self.numElements)
        stops = np.zeros(self.numElements)

        for stopNumber in range(self.bufferLeft, self.numElements - self.bufferRight):
            expectation = max(trial[:stopNumber + 1])

            acceptedApplicant = -1
            for j in range(stopNumber + 1, self.numElements - self.bufferRight):
                if trial[j] > expectation:
                    # Slice out applicants based on buffer values
                    applicants = np.flip(trial[j - self.bufferLeft: j + self.bufferRight + 1].copy())

                    sortIndices = np.argsort(applicants.copy())
                    sortIndices = np.flip(sortIndices)
                    

                    for index in sortIndices:
                        if np.random.rand() > self.reject + self.rejectDrift * index:
                            acceptedApplicant = j + self.bufferRight - index

                            #print(f'Expectation: {expectation} \nLow, Upper: {j-self.bufferLeft}, {j + self.bufferRight} \nUnflipped: {trial[j - self.bufferLeft: j + self.bufferRight + 1].copy()} \nApplicants: {applicants} \nSort Indices: {sortIndices} \nStop, Accepted: {j} , {acceptedApplicant} \n')
                            #time.sleep(5)
                            break
                        #print(f'Failed at index {index} reject: {self.reject + self.rejectDrift * index}')
                    if acceptedApplicant != -1:
                        stops[stopNumber + self.bufferRight] += 1
                    
            if acceptedApplicant != -1 and trial[acceptedApplicant] == optimalNumber:
                successfulStops[stopNumber + self.bufferRight] += 1

        return successfulStops, stops
            

                
        
    def generateRandomArrays(self) -> t.List[np.ndarray]:
        return [self.random(self.numMin, self.numMax, self.numElements) for _ in range(self.numTrials)]

def plotHistogram(figTitle: str, dataList: t.List[np.ndarray], titles: t.List[str], xLabel: str, yLabel: str):
    fig, ax = plt.subplots(figsize=(7, 7))
    for data in dataList:
        ax.plot(range(1, len(data)+1), data)
    ax.set_title(figTitle)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.legend(titles)
    plotPath = os.path.join('Figures', figTitle.replace(' ', '_') + ".png")
    fig.savefig(plotPath)


def runSim(plotTitle: str, rejectPercent: float, rejectDrift: float):
    numTrials = 10000
    numElements = 100
    numRange = (0, 1000)
    bufferShift1 = (4, 0)
    bufferShift2 = (3, 1)
    bufferShift3 = (2, 2)
    bufferShift4 = (1, 3)
    bufferShift5 = (0, 4)
    titles = ["(5, 4, 3, 2, Choice)", "(5, 4, 3, Choice, 1)", "(5, 4, Choice, 2, 1)", "(5, Choice, 3, 2, 1)", "(Choice, 4, 3, 2, 1)"]

    optimalStopping1 = OptimalStopping(rejectPercent, rejectDrift, numTrials, numElements, numRange, bufferShift1)
    successfulStops1, stops1 = optimalStopping1.getOptimalStopping()

    optimalStopping2 = OptimalStopping(rejectPercent, rejectDrift, numTrials, numElements, numRange, bufferShift2)
    successfulStops2, stops2 = optimalStopping2.getOptimalStopping()

    optimalStopping3 = OptimalStopping(rejectPercent, rejectDrift, numTrials, numElements, numRange, bufferShift3)
    successfulStops3, stops3 = optimalStopping3.getOptimalStopping()

    optimalStopping4 = OptimalStopping(rejectPercent, rejectDrift, numTrials, numElements, numRange, bufferShift4)
    successfulStops4, stops4 = optimalStopping4.getOptimalStopping()

    optimalStopping5 = OptimalStopping(rejectPercent, rejectDrift, numTrials, numElements, numRange, bufferShift5)
    successfulStops5, stops5 = optimalStopping5.getOptimalStopping()

    plotHistogram(plotTitle, [successfulStops1, successfulStops2, successfulStops3, successfulStops4,successfulStops5] , titles, "Stop Number", "Number of Successful Stops")

    successfulStops = [successfulStops1, successfulStops2, successfulStops3, successfulStops4, successfulStops5]
    argMaxIndices = [np.argmax(stop) for stop in successfulStops]

    max = np.argmax([successfulStops1[argMaxIndices[0]], successfulStops2[argMaxIndices[1]], successfulStops3[argMaxIndices[2]], successfulStops4[argMaxIndices[3]], successfulStops5[argMaxIndices[4]]])

    print(f'Best Buffer is {titles[max]} with {successfulStops[max][argMaxIndices[max]]/numTrials:.4f} success rate at {argMaxIndices[max]/numElements * 100:.2f} % of applicants.')

     

    plt.show()



def main():
    runSim("Part A Successful Stops", 0.5, 0.0)
    runSim("Part B Successful Stops", 0.2, .15)
    

if __name__ == "__main__":
    main()