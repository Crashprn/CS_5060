import multiprocessing
import os
from collections.abc import Callable
from statistics import mean
from matplotlib import pyplot as plt
import typing
import numpy as np
import math

SCENARIO_DIR = 'Scenarios'
TEST_FILE_1 = 'scenario1.csv'
TEST_FILE_2 = 'scenario2.csv'

class OptimalStopper:

    def __init__(self, randGen: Callable[[int,int], int] , stopper="vanilla", numberElements: int = 1000, listCount: int = 100, numRange: typing.Tuple[int,int] = (0, 100), normalStats: typing.Tuple[int,int] = (50, 20)) -> None:
        self.randGen = randGen
        self.numberElements = numberElements
        self.listCount = listCount
        self.mean, self.stdDev = normalStats
        self.min = numRange[0]
        self.max = numRange[1]
        self.stopper = self.vanillaStop if stopper == "vanilla" else self.maxBenefitStop

    def getRandomList(self) -> list[list[int]]:
        scenarios = []
        for i in range(self.listCount):
            scenarios.append([int(self.randGen(self.min, self.max)) for x in range(self.numberElements)])

        return scenarios
    
    def getNormalList(self) -> list[list[float]]:
        scenarios = []
        for i in range(self.listCount):
            normalList = []
            for i in range(self.numberElements):
                number = np.random.normal(self.mean, self.stdDev)
                if number < self.min:
                    number = 1
                elif number > 99:
                    number = 99
                normalList.append(number)
            scenarios.append(normalList)


        return scenarios
            

    def getShuffledList(self) -> list[list[int]]:
        scenarios = []
        for i in range(self.listCount):
            orderedList = [i for i in range(self.numberElements)]
            np.random.shuffle(orderedList)
            scenarios.append(orderedList)

        return scenarios

    def getOptimalStopping(self, listGenerator: Callable[[], list[list[int]]]) -> typing.Tuple[list[float], float]:
        
        successfulStops = [0 for i in range(self.numberElements)]
        Stops = [0 for i in range(self.numberElements)]

        with multiprocessing.Pool() as pool:
            for result in pool.map(self.stopper, listGenerator()):
                Stops = np.add(Stops, result[0])
                successfulStops = np.add(successfulStops, result[1])

        return Stops, successfulStops

    def vanillaStop(self, scenario: list[int]) -> typing.Tuple[list[int], list[int]]:
            
            # Set initial stop number, scenario list, and optimal number
            optimalNumber = max(scenario)
            successfulStops = [0 for i in range(self.numberElements)]
            Stops = [0 for i in range(self.numberElements)]
            

            # Loop through all stop numbers (stop at len - 1 because it has to stop at some point)
            for stopNumber in range(len(scenario) - 1):
                # Get expected lowest number for stopNumber first elements
                expectation = max(scenario[:stopNumber+1])

                # Loop through the remaining data and stop on first number lower than expectation
                for j in range(stopNumber, len(scenario)):
                    if scenario[j] > expectation:
                        Stops[stopNumber] += 1
                        break
                    # Fall through condition
                    elif np.random.random() < (j - stopNumber)/(len(scenario) - stopNumber - 1):
                        expectation -= 1

                # If the optimal number was chosen add increment successful stop count
                if scenario[j] == optimalNumber:
                    successfulStops[stopNumber] += 1

            return (Stops, successfulStops)

    def maxBenefitStop(self, scenario: list[int]) -> typing.Tuple[list[int], list[int]]:
        # Set initial stop number, scenario list, and optimal number
            successfulStops = [0 for i in range(self.numberElements)]
            Stops = [0 for i in range(self.numberElements)]
            
            # Get the optimal number in the list by finding the the highest number-index
            optimalNumber = 0
            for i in range(len(scenario)):
                optimalNumber = max(optimalNumber, scenario[i] - (i+1))
            

            # Loop through all stop numbers (stop at len - 1 because it has to stop at some point)
            for stopNumber in range(len(scenario) - 1):
                # Get expected lowest number for stopNumber first elements
                expectation = max(scenario[0:stopNumber+1]) - stopNumber

                # loop throught the list until finding a number better than the expectation
                for j in range(stopNumber+1, len(scenario)):
                    if scenario[j] - (j+1) > expectation:
                        Stops[stopNumber] += 1
                    
                    # Fall through condition
                    elif np.random.random() < (j - stopNumber)/(len(scenario) - stopNumber - 1):
                        expectation -= 1
                
                # If the optimal number was chosen increment successful stop count
                if scenario[stopNumber] - (stopNumber+1) == optimalNumber:
                    successfulStops[stopNumber] += 1

            return (Stops, successfulStops)

def getScenario1() -> list[int]:
    scenario1 = open(os.path.join(SCENARIO_DIR, TEST_FILE_1))

    scenarioList1 = [int(x) for x in scenario1.readlines()]

    scenario1.close()
    return [scenarioList1]

def getScenario2() -> list[int]:
    scenario2 = open(os.path.join(SCENARIO_DIR, TEST_FILE_2))

    scenarioList2 = [int(x) for x in scenario2.readlines()]

    scenario2.close()
    return [scenarioList2]

def controlGraph():
    elements = 1000
    iterations = 10000

    solver = OptimalStopper(np.random.uniform, listCount=iterations) 

    shuffledStops, shuffledOptimalStops = solver.getOptimalStopping(solver.getShuffledList)
    print(f"Shuffled: {np.argmax(shuffledOptimalStops) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(elements), shuffledOptimalStops)
    ax.set_title("Shuffled List Control")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/ShuffledControl.png")
   

def problem1():
    elements = 1000
    iterations = 10000

    solver = OptimalStopper(np.random.uniform, listCount=iterations) 
    print("Problem 1 Optimal Stopping percentages:")

    # Uniform Distribution
    uniformStops, uniformOptimalStops = solver.getOptimalStopping(solver.getRandomList)
    
    print(f"Uniform: {np.argmax(uniformOptimalStops) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(elements), uniformOptimalStops)
    ax.set_title("Uniform Distribution")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/Uniform.png")
    
    # Shuffled Distribution
    shuffledStops, shuffledOptimalStops = solver.getOptimalStopping(solver.getShuffledList)
    print(f"Shuffled: {np.argmax(shuffledOptimalStops) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(elements), shuffledOptimalStops)
    ax.set_title("Shuffled List")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/Shuffled.png")

    # Dataset 1
    data1Stops, data1OptimalStops= solver.getOptimalStopping(getScenario1)
    print(f"DataSet: {np.argmax(data1OptimalStops) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(elements), data1OptimalStops)
    ax.set_title("Data Set 1")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/DataSet1.png")

    # Dataset 2
    data2Stops, data2OptimalStops= solver.getOptimalStopping(getScenario2)
    print(f"DataSet: {np.argmax(data2OptimalStops) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(elements), data2OptimalStops)
    ax.set_title("Data Set 2")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/DataSet2.png")
    
     # Dataset 2 Total Stops
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(elements), data2Stops)
    ax.set_title("Data Set 2 Total Stops")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/DataSet2TotalStops.png")
    


def problem2():
    iterations = 10000
    elements = 100
    solver = OptimalStopper(np.random.uniform, stopper="maxBenefit", numberElements=elements, listCount=iterations, numRange=(1, 99))
    
    print("Problem 2 Optimal Stopping Percentages:")    

    uniformStops, uniformOptimalStops = solver.getOptimalStopping(solver.getRandomList)

    print(f"Uniform: {(np.argmax(uniformOptimalStops)+1) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(1,elements+1), uniformOptimalStops)
    ax.set_title("Uniform Distribution")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/Uniform_2.png")

    normalStops, normalOptimalStops = solver.getOptimalStopping(solver.getNormalList)

    print(f"Normal: {(np.argmax(normalOptimalStops)+1) / elements:.2f}")
    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(range(1,elements+1), normalOptimalStops)
    ax.set_title("Normal Distribution")
    ax.set_xlabel("Stopping number")
    ax.set_ylabel("Optimal solution count")
    fig.savefig("Figures/Normal.png")


if __name__ == "__main__":

    # Must comment out fall through condition to get this graph.
    #controlGraph()

    problem1()

    
    problem2()
    
    plt.show()




