# Problem 1

For this problem I used the vanilla stopping rule of forming an expectation from 0 to stop number and then stopping
the search when the current number exceeded the expectation. The slight twist I added was the addition of what I call
a 'buffer' which contains 5 candidates. Using this buffer I can control where the candidate that exceeded the expectation
is. For example, (1, 2, Choice, 4, 5) means that the algorithm looked 2 additional candidates more than the candidate
that exceeded the expectation.

## Run the Code

To run this code, all that needs to be done is run the python with the prefix Problem_1 the following should be outputted:

* Graph with rejection rate of 50%
* Best buffer, 