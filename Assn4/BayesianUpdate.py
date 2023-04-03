import numpy as np
import typing as t
import math


class BayesianUpdate:
    def __init__(self, pis: np.ndarray, priors: np.ndarray) -> None:
        self. pis = pis
        self.priors = priors
    

    def update(self, y: int, n):
        posterior = np.zeros_like(self.priors)
        for i in range(len(self.priors)):
             pi = self.pis[i]
             prior = self.priors[i]

             likelihood = pi**y * (1-pi)**(n-y)
             likelihood *= math.comb(n,y)
             posterior[i] = prior * likelihood
        
        posterior /= np.sum(posterior)
        return posterior
    

def main():

    bayes = BayesianUpdate(
        np.array([0.15, 0.25, 0.5, 0.75, 0.85]),
        np.array([0.15, 0.15, 0.4, 0.15, 0.15])
        )
    # bayes = BayesianUpdate(
    #     np.array([0.2, 0.5, 0.8]),
    #     np.array([0.1, 0.25, 0.65])
    # )
    result = bayes.update(3, 13)
    np.set_printoptions(suppress=True)
    print(f'Posterior: {result}\n Sum Post: {np.sum(result)}')


if __name__ == "__main__":
    main()
