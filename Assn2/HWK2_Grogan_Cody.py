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
    results = []
    with multiprocessing.Pool() as pool:
        for result in pool.starmap(stepToN, [(solverType, steps) for solverType in Solvers]):
            results.append(result)

    return results

def stepToN(solverType, steps):
    for solver in solverType:
        solver.stepN(steps)

    return solverType

def getRewards(solverType, steps):
    rewards = np.zeros(steps, dtype=np.float32)
    for solver in solverType:
        _, y = solver.getAveReward()
        rewards = np.add(rewards, y)
    rewards = np.divide(rewards, len(solverType))
    
    return rewards

def getAveQ(solverType, steps):
    qs = []
    for solver in solverType:
        _, q = solver.getQ()
        qs.append(q)

    q_final = np.zeros([len(qs[0]), len(qs[0][0])])

    for q in qs:
        q_final = np.add(q_final, q)

    return np.divide(q_final, len(qs))



def problem1a(episodes):
    ### Epsilon Greedy
    steps = 10_000
    epsilons = [0.01, 0.05, 0.1, 0.4]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    solvers = loopWEpisodes(solvers, steps)

    aveRewards = [getRewards(solver, steps) for solver in solvers]

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_a.png", "Win Percentage", x, aveRewards)

    # Plot each q array
    x = [i for i in range(steps + 1)]
    for solverType, epsilon in zip(solvers, epsilons):
        qs = getAveQ(solverType, steps)
        plotArrays(f"Q values Epsilon: {epsilon:.3f}", armTitles, f"Q_Graph_{epsilon:.3f}_a.png", "Q value", x, qs)


def problem1b(episodes) -> None:
    
    steps = 10_000
    epsilons = [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    solvers = loopWEpisodes(solvers, steps)

    aveRewards = [getRewards(solver, steps) for solver in solvers]

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_b.png", "Win Percentage", x, aveRewards)

    # Plot each q array
    x = [i for i in range(steps + 1)]
    for solverType, epsilon in zip(solvers, epsilons):
        qs = getAveQ(solverType, steps)
        plotArrays(f"Q values Epsilon: {epsilon:.3f}", armTitles, f"Q_Graph_{epsilon:.3f}_b.png", "Q value", x, qs)

def problem1c(episodes):
     ### Epsilon Greedy
    steps = 10_000
    epsilons = [0.03]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    epsilonTitles.append("Thompson Sampling")
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon) for i in range(episodes)])
    solvers.append([ThompsonSampling(get_probabilities) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    solvers = loopWEpisodes(solvers, steps)

    aveRewards = [getRewards(solver, steps) for solver in solvers]

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_c.png", "Win Percentage", x, aveRewards)

    # Plot each Epsilon q array
    x = [i for i in range(steps + 1)]
    for solverType, epsilon in zip(solvers[0:len(epsilons)], epsilons):
        qs = getAveQ(solverType, steps)
        plotArrays(f"Q values Epsilon: {epsilon:.3f}", armTitles, f"Q_Graph_{epsilon:.3f}_c.png", "Q value", x, qs)
    
    # Plot each Thompson q array
    qs = getAveQ(solvers[-1], steps)
    plotArrays("Q values Thompson", armTitles, "Q_Graph_Thompson_c.png", "Q value", x, qs)



def problem2a(episodes):
    ### Epsilon Greedy
    steps = 10_000
    drift = 0.001
    epsilons = [0.01, 0.05, 0.1, 0.4]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon, drift) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    solvers = loopWEpisodes(solvers, steps)

    aveRewards = [getRewards(solver, steps) for solver in solvers]

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_Drift_a.png", "Win Percentage", x, aveRewards)

    # Plot each q array
    x = [i for i in range(steps + 1)]
    for solverType, epsilon in zip(solvers, epsilons):
        qs = getAveQ(solverType, steps)
        plotArrays(f"Q values Epsilon: {epsilon:.3f}", armTitles, f"Q_Graph_{epsilon:.3f}_Drift_a.png", "Q value", x, qs)




def problem2b(episodes) -> None:
     ### Epsilon Greedy
    steps = 10_000
    drift = 0.001
    epsilons = [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1]
    epsilonTitles = [f"Epsilon: {epsilon:.3f}" for epsilon in epsilons]
    solvers = []
    for epsilon in epsilons:
        solvers.append([EpsilonGreedy(get_probabilities,epsilon, drift) for i in range(episodes)])

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    solvers = loopWEpisodes(solvers, steps)

    aveRewards = [getRewards(solver, steps) for solver in solvers]

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_Drift_b.png", "Win Percentage", x, aveRewards)

    # Plot each q array
    x = [i for i in range(steps + 1)]
    for solverType, epsilon in zip(solvers, epsilons):
        qs = getAveQ(solverType, steps)
        plotArrays(f"Q values Epsilon: {epsilon:.3f}", armTitles, f"Q_Graph_{epsilon:.3f}_Drift_b.png", "Q value", x, qs)

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

    armTitles = ["Arm: {}".format(i+1) for i in range(len(get_probabilities()))]
    
    solvers = loopWEpisodes(solvers, steps)

    aveRewards = [getRewards(solver, steps) for solver in solvers]

    # Plot aveReward
    x = [i for i in range(steps)]
    plotArrays("Average Reward", epsilonTitles, "Average_Reward_Drift_c.png", "Win Percentage", x, aveRewards)

    # Plot each Epsilon q array
    x = [i for i in range(steps + 1)]
    for solverType, epsilon in zip(solvers[0:len(epsilons)], epsilons):
        qs = getAveQ(solverType, steps)
        plotArrays(f"Q values Epsilon: {epsilon:.3f}", armTitles, f"Q_Graph_{epsilon:.3f}_Drift_c.png", "Q value", x, qs)
    
    # Plot each Thompson q array
    qs = getAveQ(solvers[-2], steps)
    plotArrays("Q values Thompson", armTitles, "Q_Graph_Thompson_Drift.png", "Q value", x, qs)

    # Plot each Thompson restart q array
    qs = getAveQ(solvers[-1], steps)
    plotArrays("Q values Thompson Restart", armTitles, "Q_Graph_ThompsonRestart_Drift.png", "Q value", x, qs)

    



def main():
    np.random.seed(0)
    episodes = 40
    #problem1a(episodes)
    #problem1b(episodes)
    problem1c(episodes)
    #problem2a(episodes)
    #problem2b(episodes)
    #problem2c(episodes)

    plt.show()


if __name__ == "__main__":
    main()