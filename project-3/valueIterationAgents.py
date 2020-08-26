# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        #init local variables
        u=0
        uprime=0
        j=0
        while j<iterations:
            oldvalues=self.values.copy()
            u=uprime
            for state in mdp.getStates():
                if not(mdp.isTerminal(state)):
                    #need to calculate the expected values of all states from the present state
                    possibleActions= mdp.getPossibleActions(state)
                    sumlist=[]
                    for a in possibleActions:
                        possibleSuccessorStates= mdp.getTransitionStatesAndProbs(state,a)
                        sum=0
                        for i in possibleSuccessorStates:
                            sum+= i[1]*oldvalues[i[0]]
                        sumlist.append(sum)
                            # uprime = R(s) + y(max(expected results across all possible actions))
                    uprime= mdp.getReward(state,None,None) + (self.discount) * max(sumlist)

                else:
                    uprime =mdp.getReward(state,None,None)
                self.values[state] = uprime
            j=j+1


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values
        """
        "*** YOUR CODE HERE ***"

        #if(action == 'exit'):
            #return self.mdp.getReward(state,'exit',state)

        transFunction = self.mdp.getTransitionStatesAndProbs(state, action)
        sum=0
        for pair in transFunction:
            #utility of the state times the probaility you end up in that state
            sum+= (self.mdp.getReward(state,action,pair[0])+(self.discount)*(self.values[pair[0]])) * pair[1]
        return sum
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actionslist=self.mdp.getPossibleActions(state)
        qvalslist=[]
        for action in actionslist:
            qvalslist.append((self.computeQValueFromValues(state,action),action))

        maxaction='exit'
        max= -999999
        for p in qvalslist:
            if(p[0]>max):
                max=p[0]
                maxaction=p[1]

        #print(str(max) + ',' + str(maxaction))
        return maxaction

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
