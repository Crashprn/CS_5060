# CS 5060 Homework 2

## Running Code
	To run this code all that needs to be done is run the HWK2_Grogan_Cody file and the following graphs
	should be outputted:

	- Average reward from epsilon greedy for epsilons of 0.01, 0.05, 0.1, and 0.4
	- Average reward for epsilon greedy for various epsilons
	- Average reward with optimal epsilon and thompson sampling
	- Average reward from epsilon greedy with drift for epsilons of 0.01, 0.05, 0.1, and 0.4
	- Average reward for epsilon greedy with drift for various epsilons
	- Average reward with drift for optimal epsilon, thompson, and thompson w/ restart

NOTE: I generate all graphs using the average of 40 runs for each epsilon or thompson sampling strategy


## Problem 1
For this section the reward amount from each arm is determined using a predetermined normal distribution.

<p align=center>
	<img src="Figures/Average_Reward_a.png" width="1000"/>
</p>
<p>
	The graph above shows average win percentage over 40 episodes of the epsilon greedy algorithm
	with varying values of epsilon. As can be seen the epsilon of 0.05 converges to its steady state win percentage
	much faster than the other epsilons. This is because the value of 0.05 is closest to the perfect ratio of 
	exploration	to exploitation. The ratio can be seen with an epsilon of 0.4 where the algorithm converges to
	slightly under a 60% win rate. This makes sense because the algorithm explores 40% of the time and the optimal
	arm only wins at a certain rate. This then transfers to the other epsilons as the lower epsilons converge to 
	higher win percentages because they exploit their knowledge more frequently.
</p>

<img src="Figures/Q_Graph_0.010_a.png" width="500"/>
<img src="Figures/Q_Graph_0.050_a.png" width="500"/>
<img src="Figures/Q_Graph_0.100_a.png" width="500"/>
<img src="Figures/Q_Graph_0.400_a.png" width="500"/>

<p>
The above graphs show the same result from the previous in more detail. As we can see, the epsilon of 0.05 finds the optimal arm 3 much
faster than the epsilon of 0.01. This is because the exploration is 5 times higher, giving the algorithm more opportunities to find
the optimal arm. These graphs also show why too much exploration can be bad as seen in the epsilon 0.4 figure. As can be seen, the
q lines are fairly continuous for all arms. This causes the algorithm to perform poorly because it is not exploiting its prior 
knowledge to the fullest extent.
</p>


<p align=center>
	<img src="Figures/Average_Reward_b.png" width="1000"/>
</p>
<p>
	The graph above shows the average win percentage over 40 episodes in order to find the optimal epsilon value
	to use for the problem. As could have been predicted from the previous graph, the optimal epsilon is between
	0.01 and 0.05. I find the optimal epsilon to be 0.02 because it has much better convergence and to a higher
	win rate. This graph also shows the downfall of having very low epsilons such as 0.01. This is because algorithm
	doesn't explore enough to find the optimal arm and instead gets stuck pulling a sub-optimal arm. This then shows
	the algorithm got lucky and found the optimal arm early in the previous graph.
</p>

<img src="Figures/Q_Graph_0.020_b.png" width="500"/>
<img src="Figures/Q_Graph_0.030_b.png" width="500"/>

<p>
The graphs above show the 2 best performing epsilons in the the simulation. As can be seen, each epsilon find the optimal arms
(3 and 18) fairly quick. However, the epsilon of 0.03 finds the optimal arms much faster. This then shows that there is an optimal
ratio of exploration to exploitation.
</p>

<p align=center>
	<img src="Figures/Average_Reward_c.png" width="1000"/>
</p>

<p>
	The graph above shows the difference between the optimal epsilon value and the thompson sampling method. As can be 
	seen, the Thompson sampling method converges much slower than the optimal epsilon. This is because the Thompson
	method uses beta distributions which cause quench its exploration as it goes. This means the thompson method has the
	potential to have a higher win rate than the optimal epsilon but will take much longer to get there as seen by the graph.
</p>

<img src="Figures/Q_Graph_0.030_c.png" width="500"/>
<img src="Figures/Q_Graph_Thompson_c.png" width="500"/>

<p>
Like the epsilon of 0.4, the thompson sampling method pulls uniformly toward the beginning of the simulation which causes it to
lag behind the winning rate of the optimal epsilon. This is because the optimal epsilon leverages its information much sooner in
the simulation.
</p>

## Problem 2

For this section, the normal distribution (mean) which outputs the reward for each arm slowly decreases over each time step.
In addition, at a time 3000 random arms get a sudden increase in reward (mean value).

<p align=center>
	<img src="Figures/Average_Reward_Drift_a.png" width="1000"/>
</p>

<p>
	The graph above shows the result of using the predefined epsilon values as outlined in the assignment. The slow decrease
	in reward output is quite obvious as the win rate for all epsilons slowly decreases over time. In addition the small bump
	at time 3000 shows the benefit of slightly bigger epsilons. Meaning a slightly bigger epsilon allowed the algorithm to
	identify the new optimal arm after the sudden increase. As a result of being more adaptable, the higher values of epsilon
	overtake the win rate of epsilon = 0.01.
</p>

<img src="Figures/Q_Graph_0.010_Drift_a.png" width="500"/>
<img src="Figures/Q_Graph_0.050_Drift_a.png" width="500"/>
<img src="Figures/Q_Graph_0.100_Drift_a.png" width="500"/>
<img src="Figures/Q_Graph_0.400_Drift_a.png" width="500"/>

<p>
The above graph shows the opposite trend of the problem 1. This is due to the epsilon of 0.4 graph which shows it finds the new optimal
arm after the sudden increase. This then shows a higher epsilon is much better to use when sudden changes in reward are to be expected.
</p>

<p align=center>
	<img src="Figures/Average_Reward_Drift_b.png" width="1000"/>
</p>

<p>
	The most interesting conclusion drawn from this graph is that all of the epsilons converge to a common win rate.
	This is likely because that their optimal arm drops below the expectation of another arm that hasn't been pulled in a while.
	As a result, the algorithm wastes time exploiting its out of date knowledge instead of sticking with the optimal arm.
</p>

<img src="Figures/Q_Graph_0.010_Drift_b.png" width="500"/>
<img src="Figures/Q_Graph_0.020_Drift_b.png" width="500"/>
<img src="Figures/Q_Graph_0.030_Drift_b.png" width="500"/>
<img src="Figures/Q_Graph_0.040_Drift_b.png" width="500"/>

<p>
The above graphs echo the results from the average reward graph. It can be seen that all of the values of epsilon present fail to find the
the optimal arm through out the simulation. This is because arm 1 is not pulled enough for the algorithm to realize it is the best,
making it continue to pull the arm it thinks is the best.
</p>

<p align=center>
	<img src="Figures/Average_Reward_Drift_c.png" width="1000"/>
</p>

<p>
	This graph shows the average reward of two optimal epsilons, thompson sampling, and thompson sampling with a restart.
	The graph above shows the conclusion drawn from the previous graph where at the time of 3000 it is better to throw out
	the previous expectation than trying to correct for sudden changes. This is shown by the Thompson sampling w/ restart
	greatly outperforming the other three lines. This is because of the nature of exploiting prior information. In the case
	of the epsilon greedy algorithm, it takes a substantial amount of time to move the average of an arm that has 3000 samples.
	In the case of thompson sampling, it takes a significant of losses to reduce the pull frequency of an arm with 3000 wins.
	The cause of epsilon greedy and regular thompson sampling failing in this scenario is because the foundation of both
	assumes that the win rate will converge to some constant. However, in this scenario, the probabilities are always moving
	and fluctuating, which does not allow these these methods to act optimally.

</p>

<img src="Figures/Q_Graph_0.020_Drift_c.png" width="500"/>
<img src="Figures/Q_Graph_0.075_Drift_c.png" width="500"/>
<img src="Figures/Q_Graph_Thompson_Drift.png" width="500"/>
<img src="Figures/Q_Graph_ThompsonRestart_Drift.png" width="500"/>

<p>
The graphs above show that throwing out data after a significant shift in conditions is the best way to ensure optimality.
This is shown through the graph of the Thompson Sampling /w a restart where it immediately finds the new optimal arm and 
stops checking the previously optimal arms. This then means that throwing out the data (or only taking part of it) is a much
better strategy for finding the optimal arm than trying to fix outdated data.
</p>