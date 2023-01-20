
# Problem 1

	For the first problem I used what is essentially the vanilla stopping algorithm with a slight addition.
	This addition allows for better odds of finding the optimal solution in the list by making an "I've seen
	this before" counter. Meaning, if the algorithm sees the expectation 4 times it selects that as its
	solution. This allows the algorithm to pick the correct solution if the optimal solution occurs early in
	the list.

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

The output from the code shows the optimal stopping point of the uniform distribution with the vanilla stopping algorithm of 14 %.
This makes sense because there is a much higher probability of the optimal solution occurring. This means the optimal solution is likely
to be in the m first elements quite early in the list.

### Shuffled List

<img src="Figures/Shuffled.png" width="500"/>

This graph shows the problem as outlined in the slides with a number only occuring once in the list. The code ouputs a optimal stop of 35%
of the length of the list. This is sufficiently close to the 36.8 % number given by the book. In addition, the probability of selecting the
optimal number at the best stop is 37 %. This aligns with the answer given by the book.

### Scenario 1

<img src="Figures/DataSet1.png" width="500"/>

This graph shows the same result of Uniform graph but has significantly less resolution because the algorithm was run on a single list.
As mentioned before, the likelyhood of the optimal solution occuring is much higher in a uniform distribution making the best stopping
point early in the list.

### Scenario 2

<img src="Figures/DataSet2.png" width="500" />

This graph shows the downfall of using the vanilla stopping algorithm on a single list. The algorithm fails because the algorithm forms and expectation before
it starts selecting stopping points. Meaning that if the optimal solution occurs early in the list the rule of stopping at 36.8 % will fail to choose the optimal solution.



# Problem 2


		

