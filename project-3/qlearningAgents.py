# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        "*** YOUR CODE HERE ***"

        self.qValues= util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        stringconcat= str(state)+str(action)
        return self.qValues[stringconcat]

        util.raiseNotDefined()
    def setQValue(self,state,action,value):
        """
            sets the Q value for a given state, action pair. used in the update equation
        """
        stringconcat= str(state)+str(action)
        self.qValues[stringconcat]=value

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        qValuesList=[]
        legalActions=self.getLegalActions(state)
        if(len(legalActions)==0):
            return 0.0
        for action in legalActions:
            qValuesList.append(self.getQValue(state,action))
        return max(qValuesList)

        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        if(len(legalActions)==0):
            return None
        #Compute HighestAction, tiebreak randomly
        hiQ=-99999
        highaction=[]
        for action in legalActions:
            presentq=self.getQValue(state,action)
            if(presentq>hiQ):
                highaction=[action]
                hiQ=presentq
            if(presentq==hiQ):
                highaction.append(action)
        return random.choice(highaction)


        util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if(len(legalActions)<1):
            return None
        #Flip a coin with probability epsilon, do some random action if it comes up true
        if(util.flipCoin(self.epsilon)):
            return random.choice(legalActions)
        #else return the action with the highest q value
        return self.computeActionFromQValues(state)



        util.raiseNotDefined()

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #Update function:
        #Q(s,a)= Q(s,a) + alpha(R(S) + gamma(max(Q(s',a') - Q(s,a))))

        oldQ = self.getQValue(state,action)
        bestQAtNextState= self.computeValueFromQValues(nextState)
        a=self.alpha
        gamma=self.discount
        newQ= oldQ + (a * (reward + (gamma*bestQAtNextState) - oldQ) )
        self.setQValue(state,action,newQ)
        return newQ

        util.raiseNotDefined()



    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        # get the features and weights
        features = self.featExtractor.getFeatures(state, action)
        weights = self.getWeights()
        # do the approximate q function
        q = 0
        for feat, value in features.iteritems():
            q += weights[feat]*value
        # return that
        return q

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        # get the features and weights
        feats = self.featExtractor.getFeatures(state, action)
        weights = self.getWeights()
        # difference term here for cleanliness
        diff = (reward+self.discount*self.computeValueFromQValues(nextState)-self.getQValue(state, action))
        # update all the values
        for feat, value in feats.iteritems():
            weights[feat] += self.alpha*diff*feats[feat]
    
    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            pass
