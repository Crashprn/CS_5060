# Problem 1

For this problem I used the vanilla stopping rule of forming an expectation from 0 to stop number and then stopping
the search when the current number exceeded the expectation. The slight twist I added was the addition of what I call
a 'buffer' which contains 5 candidates. Using this buffer I can control where the candidate that exceeded the expectation
is. For example, (1, 2, Choice, 4, 5) means that the algorithm looked 2 additional candidates more than the candidate
that exceeded the expectation.

## Run the Code

To run this code, all that needs to be done is run the python with the prefix Problem_1 the following should be outputted:

* Graph with rejection rate of 50%
* Best buffer, % Success Rate, Stop % for Success Rate

* Graph with 20% rejection and 15% for subsequent canditates
* Best buffer, % Success Rate, Stop % for Success Rate

## Part A

![image](Figures/Part_A_Successful_Stops.png)

Buffer: (5, 4, 3, 2, Choice)

Success %: 20.54%

Stop %: 36%

### What is the early stopping rule that maximizes the likelihood of obtaining the optimal optimal answer?

The optimal stopping policy from the figure above is stopping when the
expectation is exceeded like the vanilla stopping algorithm situation.
However, the figure above shows there is no significant difference between
each of the different buffer locations. This makes sense because each
applicant has an equally likely chance of rejecting the job offer
regardless of position in the buffer.

### How does this compare with simple early stopping problem?

This result is essentially the same as the simple early stopping problem
in stopping percentage but not in the success percentage. This is because
of the possibility of rejection because the value of 50% rejection explains
why the success percentage is roughly half of the simple early stopping
problem.

## Part B

![image](Figures/Part_B_Successful_Stops.png)

Buffer: (5, 4, 3, 2, Choice)

Success %: 31.1%

Stop %: 34%

### What is the early stopping rule that maximizes the likelihood of obtaining the optimal optimal answer?

The optimal stopping policy for this problem is to stop as soon as the
expectation is exceeded. This is obvious from the graph above as the buffer
location with the chosen candidate last has the best performance. This is
because the rejection percentage increases with each successive candidate.
This decentivizes the algorithm from looking at candidates past the chosen
because the rejection % increases.

### How does this compare with simple early stopping problem?

This iteration of the early stopping problem comes even closer to the simple
early stoppig problem because the base rejection % is much lower than the
part A. This then proves the conclusion from part A because the success % is
roughly 20% lower than the simple early stopping success rate. This means 
that the addition of a buffer does nothing to the optimal stopping policy.

# Problem 2

For this problem I use the epsilon greedy algorithm to determine the best
location to put a sensor. In this algorithm, the quality function I use is
the average reward from each site over time. Then I run the algorithm over
500 potential days and 500 episodes and average the outcomes of each
episode. This allows me to determine the average convergence speed to 
a particular site.

## Run the Code

The file for this problem has the prefix Problem__2 and the following is
outputted:

* Q graph w/o baseline
* Percent picked of each site w/o baseline
* Total days, Number of days skipped

* Q graph w/ baseline
* Percent picked of each site w/ baseline
* Total days, Number of days skipped

## Part A

![image](Figures/Problem_2_Part_A.png)

Optimal Area: beta(7,3) + 2 or 1st location

Epsilon: 0.1

### How many days will it take for you to make the decision to place the permanent sensor?

The graph above shows the algorithm converges in roughly 50 days rather
consistently with an epsilon of 0.1. 

## Part B

![image](Figures/Problem_2_Part_B.png)

Optimal Area: normal(1.3, 7) or 5th site

Epsilon: 0.1

Number of days Skipped: 246/500

### Does this change the final decision of the placement

The addition of the baseline significatly changes the permanent sensor site
because it reduces the values outputted from each distribution. This greatly
favors the non-terminating distributions such as the normal distribution
because the highly negative tail values are never recorded thus shifting the
the q value. This is evident from the number of days skipped because the
normal distribution had the highest q value but nearly 50% of data points 
were thrown out. Meaning the 5th site was below the baseline 50% of the time
which should have disqualified it from being the optimal area.

### How long does it take before you choose to place the sensor?

Based on the graph, the time it took to place the sensor should be around
the area where site 5 overtook site 1 in the % picks graph. This is because
the it is fairly random when the greedy algorithm determines the 5th site
is the best. Thus the % pick graph is the most indicative of convergence 
time at 250-300 days.

# Problem 3



