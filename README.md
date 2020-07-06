# mc21
mc21 is designed to simulate, test, and analyze strategies for 21 (Blackjack).
A Monte Carlo simulation creates many iterations of a random event to predict trends for random events.

## Baseline Findings
A simple strategy to hit until 17 or greater without splits or doubles results in the following:

[![baseline-img]]
exp return: -7.78 +/- 4.776 %

There is much room for improvement.

## Quickstart
Assuming git installed:

'''bash
$ git clone htps://github.com/John-L-Jones-IV/mc21.git
$ python3 mc21
'''

Now that you have sucessfuly cloned and ran the simulations, you are can play with the code and make it your own!


### The code 
This repo depends on Python 3 and common Python modules such as matplotlib, numpy, and random.
The original development environment is just vim and Ubuntu 18.04.

Script outline.

mc21.py - the simulation environment<br />
blackjack.py - a collection of classes and functions used in mc21<br />
Players.py - a collection of special subclasses of Players<br />
strategy.py - functions and structures useful for statiscial strategy<br />


[baseline-img]: ./img/baseline-img.png
