import multiprocessing
from random import choice, choices
import numpy as np
from matplotlib import pyplot as plt
import os

from EpsilonGreedy import EpsilonGreedy
from ThompsonSampling import ThompsonSampling

def get_probabilities(drift=0, t=0):
    drift *= t
    if t > 3_000:
        band0 = 5
        band2 = 2
        band7 = 3
        band18 = 3
    else:
        band0 = 0
        band2 = 0
        band7 = 0
        band18 = 0

    probs = [
        np.random.normal(0 - drift + band0, 5),
        np.random.normal(-0.5 - drift,12),
        np.random.normal(2 - drift + band2,3.9),
        np.random.normal(-0.5 - drift,7),
        np.random.normal(-1.2 - drift,8),
        np.random.normal(-3 - drift,7),
        np.random.normal(-10 - drift,20),
        np.random.normal(-0.5 - drift + band7,1),
        np.random.normal(-1 - drift,2),
        np.random.normal(1 - drift,6),
        np.random.normal(0.7 - drift,4),
        np.random.normal(-6 - drift,11),
        np.random.normal(-7 - drift,1),
        np.random.normal(-0.5 - drift,2),
        np.random.normal(-6.5 - drift,1),
        np.random.normal(-3 - drift,6),
        np.random.normal(0 - drift,8),
        np.random.normal(2 - drift,3.9),
        np.random.normal(-9 - drift + band18,12),
        np.random.normal(-1 - drift,6),
        np.random.normal(-4.5 - drift,8)              
    ]
    
    return probs


def plotArrays(figTitle, titles, saveFile, y_title, x, arrays, x_title = "Time steps"):
    # Matplotlib Figure config
    fig, ax = plt.subplots(figsize=(10,7))
    numberOfPlots = len(arrays)
    colormap = plt.cm.nipy_spectral
    ax.set_prop_cycle('color',[colormap(i) for i in np.linspace(0, 1, numberOfPlots)])
    ax.set_title(figTitle)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    #ax.set_ylim([0,1])
    # Plotting data
    for array, title in zip(arrays, titles):
        ax.plot(x, array, label=title)
    ax.legend()
    fig.savefig(os.path.join("Figures", saveFile))



def loopWEpisodes(Solvers, steps):
    aveReward = []
    with multiprocessing.Pool() as pool:
        for result in pool.starmap(getRewards, [(solverType, steps) for solverType in Solvers]):
            aveReward.append(result)

    return aveReward

def getRewards(solverType, steps):
    rewards = np.zeros(steps, dtype=np.float32)
    for solver in solverType:
        solver.stepN(steps)
        _, y = solver.getAveReward()
        rewards = np.add(rewards, y)
    rewards = np.divide(rewards, len(solverType))
    
    return rewards

    


def problem1a(episodes):
    ### Epsilon Greedy
    steps = 10_000
    epsilons = [0.01, 0.05, 0.1, 0.4]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    aveRewards = loopWEpisodes(solvers, steps)

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_a.png", "Win Percentage", x, aveRewards)


def problem1b(episodes) -> None:
     ### Epsilon Greedy
    steps = 10_000
    epsilons = [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    aveRewards = loopWEpisodes(solvers, steps)
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_b.png", "Win Percentage", x, aveRewards)

def problem1c(episodes):
     ### Epsilon Greedy
    steps = 10_000
    epsilons = [0.02]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    epsilonTitles.append("Thompson Sampling")
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon) for i in range(episodes)])
    solvers.append([ThompsonSampling(get_probabilities) for i in range(episodes)])

    aveRewards = loopWEpisodes(solvers, steps)

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_c.png", "Win Percentage", x, aveRewards)


def problem2a(episodes):
    ### Epsilon Greedy
    steps = 10_000
    drift = 0.001
    epsilons = [0.01, 0.05, 0.1, 0.4]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon, drift) for i in range(episodes)])


    aveRewards = loopWEpisodes(solvers, steps)

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_Drift_a.png", "Win Percentage", x, aveRewards)




def problem2b(episodes) -> None:
     ### Epsilon Greedy
    steps = 10_000
    drift = 0.001
    epsilons = [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon, drift) for i in range(episodes)])


    aveRewards = loopWEpisodes(solvers, steps)

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_Drift_b.png", "Win Percentage", x, aveRewards)

def problem2c(episodes):
     ### Epsilon Greedy
    steps = 10_000
    drift = 0.001
    epsilons = [0.020, 0.075]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    epsilonTitles.append("Thompson Sampling")
    epsilonTitles.append("Thompson w/ Restart")

    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon, drift) for i in range(episodes)])
    solvers.append([ThompsonSampling(get_probabilities, drift) for i in range(episodes)])
    solvers.append([ThompsonSampling(get_probabilities, drift, reset=True) for i in range(episodes)])

    aveRewards = loopWEpisodes(solvers, steps)

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_Drift_c.png", "Win Percentage", x, aveRewards)

    



def main():
    episodes = 40
    problem1a(episodes)
    problem1b(episodes)
    problem1c(episodes)
    problem2a(episodes)
    problem2b(episodes)
    problem2c(episodes)

    plt.show()


if __name__ == "__main__":
    main()