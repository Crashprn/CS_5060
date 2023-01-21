
# Problem 1

	For the first problem I used what is essentially the vanilla stopping algorithm with a slight addition.
	This addition essentially randomly lowers the expectation of the stopper as it gets closer to the end of the list.
	I accomplish this by generating a random number and only decrementing the expectation if it is smaller than the percentage of the list left to select from. This allows the algorithm to pick the correct solution if the optimal solution occurs early in the list for uniform distributions. However this has an adverse effect on randomly shuffled lists as this document will show.

## Runnning
		To run the code all that needs to be done is run the HWK file. The main function then calls problem1 
		which runs the stopper on 4 data sets:

		- Uniform Distribution from 0-99
		- Shuffled list (list containing 0-9999 in the regular problem)
		- Scenario 1
		- Scenario 2

## Results
	This section shows the results from problem one. The results include a optimal stopping number and a graph showing the number
	of optimal stops at each index.

### Uniform

<img src="Figures/Uniform.png" width="500"/>

The output from the code shows the optimal stopping point of the uniform distribution with the vanilla stopping algorithm of 11 %. This makes sense because if the list is populated 0 to n numbers then all of the numbers are likely to occur in the first n elements. This means the optimal solution is likely to be in the n first elements quite early in the list and thus the stopper should stop early to avoid the optimal number being the expectation.

### Shuffled List

<img src="Figures/Shuffled.png" width="500"/>

This graph shows the problem as outlined in the slides with a number only occuring once in the list. The code ouputs a optimal stop of 31% of the length of the list. This is sufficiently close to the 36.8 % number given by the book. The reason why it is not the exact number is due to the fall through condition for the uniform numbers. In the shuffled list, the no number is the same, so the likelyhood of a number being greater than the expectation is fairly high as their are more options. The fallthrough condition reduces the effectiveness of the shuffled list there is a substantially higher chance that reducing the expectation will cause it to pick a non-optimal solution.

### Scenario 1

<img src="Figures/DataSet1.png" width="500"/>

This graph shows the same result of Uniform graph but has significantly less resolution because the algorithm was run on a single list. As mentioned before, the likelyhood of the optimal solution occuring is much higher in a uniform distribution making the best stopping point early in the list.

### Scenario 2

<img src="Figures/DataSet2.png" width="500" />

This graph shows the downfall of using the vanilla stopping algorithm on a single list. The algorithm fails because the algorithm forms and expectation before it starts selecting stopping points. Meaning that if the optimal solution occurs early in the list the rule of stopping at 36.8 % will fail to choose the optimal solution.



# Problem 2


		

