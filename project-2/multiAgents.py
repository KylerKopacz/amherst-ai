# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # if there is a ghost, dodge it
        # THIS WORKS SO DON"T CHANGE IT
        ghostDists = [manhattanDistance(ghostState.getPosition(), newPos) for ghostState in newGhostStates]
        for dist in ghostDists:
          if dist <= 1:
            return -1


        # get the distances to the foods
        foodDists = [manhattanDistance(foodPos, newPos) for foodPos in newFood.asList()]
        # if the new position has food, then go to it
        if currentGameState.hasFood(newPos[0], newPos[1]):
          return 1
        else:
          return 1.0 / min(foodDists)



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        """My Approach is to first create a function which gets scores by
        recuring down, and then matching those scores with the related actions at the top level.
        This is because I intialy tried to pass tuples of (score,state,action) up and down the tree,
        but it would sometimes get that jumbled up."""


        def minmaxvalue(gameState,turnIndex,depth):
            #Terminal test-- are we at the goal state?

            agentOn=turnIndex%gameState.getNumAgents()

            if (gameState.isLose() or gameState.isWin()):
                # Return the eval function of the given state( a number)
                return self.evaluationFunction(gameState)
            # Cuttoff Test -- have we gone too deep?
            if (depth ==0): # gone to max depth
                return self.evaluationFunction(gameState)

            #generate possible actions
            possibleactions=gameState.getLegalActions(agentOn)

            #Now we want to find the max or min score (depending on who  is the agent) from the set of all possible actions
            resultant_minimaxs=[]
            for action in possibleactions:
                resultant_minimaxs.append(minmaxvalue(gameState.generateSuccessor(agentOn,action), agentOn+1,depth-1))
            if(agentOn>0):
                return min(resultant_minimaxs)
            else:
                return max(resultant_minimaxs)


        # Now we call the minmaxvalue function on all possible sucessor states & take the best one
        potentialactions=[]
        for action in gameState.getLegalActions(0):
            # create a tuple of form (action,score)
            potentialactions.append((action,minmaxvalue(gameState.generateSuccessor(0,action),1,self.depth*gameState.getNumAgents()-1)))
        #return the max score of these possible actions
        return max(potentialactions,key=lambda item:item[1])[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """ we're gonna use the same Approach as our normal MinimaxAgent,
        but implement Alpha Beta pruning.
        Alpha Beta pruning will just eliminate possible actions
        as we recur through the list in our minimaxvalues function"""


        def abminmaxvalue(gameState,turnIndex,depth, alpha,beta):
            #Terminal test-- are we at the goal state?
            agentOn=turnIndex%gameState.getNumAgents()

            if (gameState.isLose() or gameState.isWin()):
                # Return the eval function of the given state( a number)
                return self.evaluationFunction(gameState)
            # Cuttoff Test -- have we gone too deep?
            if (depth ==0): # gone to max depth
                return self.evaluationFunction(gameState)

            #generate possible actions
            possibleactions=gameState.getLegalActions(agentOn)
            #Now we want to find the max or min score (depending on who  is the agent) from the set of all possible actions
            if(agentOn==0):
                #here's where the alpha & beta come in-- pacman version
                #Note that this comes traight from the psuedocode
                v=-99999 # set v to be neg infinity
                for action in possibleactions:
                    v=max(v,abminmaxvalue(gameState.generateSuccessor(agentOn,action), agentOn+1,depth-1,alpha,beta)) #take the bigger of these two values
                    if(v>beta): # if v is bigger than beta, then we don't need to search anymore
                        return v
                    if(v>alpha):# replace alpha if v is larger
                        alpha=v
                return v
            else:
                # just flip everything around for the ghosts
                v=99999 # set v to be infinity
                for action in possibleactions:
                    v=min(v,abminmaxvalue(gameState.generateSuccessor(agentOn,action), agentOn+1,depth-1,alpha,beta)) #take the bigger of these two values
                    if(v<alpha): # if v is smaller than alpha, then we don't need to search anymore
                        return v
                    if(v<beta):# replace beta if v is smaller
                        beta=v
                return v
        # again, we run the same things as minimaxagent but with initalized
        #alpha= -neginf
        #beta = posinf
        #The issue this presents is that we need to account for ab pruning at the top of the tree so to speak-- so we treat it like a max lol
        bigv=-99999
        alpha=-99999
        beta=99999
        savedaction=Directions.STOP
        for action in gameState.getLegalActions(0):
            # create a tuple of form (action,score)
            potentialaction=(action,abminmaxvalue(gameState.generateSuccessor(0,action),1,self.depth*gameState.getNumAgents()-1,alpha,beta))
            if(potentialaction[1]>bigv):
                bigv=potentialaction[1]
                savedaction=potentialaction[0]
            if(bigv>beta):
                return savedaction
            if(bigv>alpha):
                alpha=bigv
        return savedaction
        #return the alpha beta pruned max score of these possible actions

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        """Our new returned value is no longer the max, but """

        def uniformExpectedValue(list):
            total=float(0)
            for element in list:
                total+=element
            return total/float(len(list))

        def minmaxvalue(gameState,turnIndex,depth):
            #Terminal test-- are we at the goal state?

            agentOn=turnIndex%gameState.getNumAgents()

            if (gameState.isLose() or gameState.isWin()):
                # Return the eval function of the given state( a number)
                return self.evaluationFunction(gameState)
            # Cuttoff Test -- have we gone too deep?
            if (depth ==0): # gone to max depth
                return self.evaluationFunction(gameState)

            #generate possible actions
            possibleactions=gameState.getLegalActions(agentOn)

            #Now we want to find the max or min score (depending on who  is the agent) from the set of all possible actions
            resultant_minimaxs=[]
            for action in possibleactions:
                resultant_minimaxs.append(minmaxvalue(gameState.generateSuccessor(agentOn,action), agentOn+1,depth-1))
            if(agentOn==0): # we keep this the same, because we only care about expectation for adversaries
                return max(resultant_minimaxs)
            else:
                # here's the location of our expected
                #print('E[' + str(uniformExpectedValue(resultant_minimaxs))+ ']')
                return uniformExpectedValue(resultant_minimaxs)


        # Now we call the minmaxvalue function on all possible sucessor states & take the best one
        potentialactions=[]
        for action in gameState.getLegalActions(0):
            # create a tuple of form (action,score)
            potentialactions.append((action,minmaxvalue(gameState.generateSuccessor(0,action),1,self.depth*gameState.getNumAgents()-1)))
        #return the max score of these possible actions
        return max(potentialactions,key=lambda item:item[1])[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <just check out the comments lol>
    """

    '''Alright so here we go. We have to evaluate a state that we are in, rather
    than an action that we are going to take. So what makes a good state?
    We can make it so that a state that is closer to the goal is a good state.
    What is the goal? All of the food is eaten and pacman hasn't died. So maybe
    we can pathfind to all of the foods, but when we are close to a ghost we run away.
    If the ghosts have a scared timer, then we can maybe seek out the ghosts. But mostly,
    the value of a state is going to be how much food is left I would have to say.
    '''

    # lets get some useful information from the current game state
    foods = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    pacmanPos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    capsulesLeft = len(capsules)
    foodLeft = len(foods)

    # we are going to keep the total score of the state in this
    stateScore = 0

    # so there are some things that affect the score greatly
    #   1. The actual score of the game should be taken into account
    #   2. The total number of food. The score should grow as the number of food decreases
    #   5. Capsules, like food, are really important. If there is not a lot of capsules, that is good.
    #   3. The distances from the ghosts. If they are not scared, then they should be far away
    #   4. Eating scared ghosts is really good for the score. We should take this into account
    #   6. The overall distances to foods is also important. If food is close, then it needs to be eaten

    # First is the score of the game. This should be taken into account
    # because we don't want to lose the game. The losing score is super low,
    # and that's all we really care about because the bulk of the evaluation
    # is going to come from foods and ghosts and stuff. So let's have a pretty
    # low weight for this
    stateScore += 3 * currentGameState.getScore()

    # Next is food. Having a lot of food is bad for the score, so it would make
    # sense to have the score decrease for the amount of food that is left. This
    # should be kinda significant, so give a decent weight.
    stateScore += -50 * foodLeft

    # Next is the capsules. They allow us to eat the ghosts, so they should be
    # of higher importance than the food was. So if there are a lot of capsules left,
    # then that should result in a lower state score
    stateScore += -10000 * capsulesLeft

    # Alright this second part uses distances to in-game things as a measurement of score
    # let's get them all right now
    distFoods = [manhattanDistance(food, pacmanPos) for food in foods]
    distGhosts = [manhattanDistance(ghost.getPosition(), pacmanPos) for ghost in ghosts]
    distCapsules = [manhattanDistance(capsule, pacmanPos) for capsule in capsules]

    #Turns out, if you just use the closest food,
    # pacman will want to go towards the food
    if(len(distFoods) > 0):
        closestFood = min(distFoods)
        stateScore += -2 * closestFood
        
    # Now we go and work with the ghosts. We want to try and keep away from the ghosts
    # if that is possible. This shouldn't matter THAT much, otherwise pacman will just avoid
    # the ghosts and not go for any of the food, so this shouldn't be that high of a weight.
    for dist in distGhosts:
        # if the ghost is close, then that is really bad
        if dist < 3:
            stateScore += 6 * dist
        else:
            stateScore += 1 * dist

    # But if there are scared ghosts, we should seek out and destroy them for maximum score.
    # Basically we should do the above in reverse, and if there is a scared ghost then destroy it.
    distScaredGhosts = []
    for ghost in ghosts:
        if ghost.scaredTimer:
            # SEEK AND DESTORY THAT DUDE
            distScaredGhosts.append(manhattanDistance(ghost.getPosition(), pacmanPos))

    # the number of scared ghosts should be a really big negative so we seek and destroy the ghost
    if len(distScaredGhosts) > 0:
        for dist in distScaredGhosts:
            stateScore += -500 * dist


    # Finally, return the score of the state
    return stateScore

# Abbreviation
better = betterEvaluationFunction
