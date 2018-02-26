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

        "*** YOUR CODE HERE ***"


        def Average(list):
            sum = 0
            for item in list:
                sum += item
            return sum / len(list)

        def reciprocal(x):
            x = float(x)
            return 1.0 / x

        food_reward = 0.0
        ghost_penalize = 0.0
        FoodDistance = [manhattanDistance(newPos, x) for x in newFood.asList()]
        if len(FoodDistance) > 0:
            if min(FoodDistance) != 0 and Average(FoodDistance) != 0:
                food_reward = 5.0 * reciprocal(Average(FoodDistance)) + reciprocal(min(FoodDistance))


        GhostPosList = [x.getPosition() for x in newGhostStates]
        GhostDistance = [manhattanDistance(newPos, x) for x in GhostPosList]
        if len(GhostDistance) > 0:
            if min(GhostDistance) != 0:
                ghost_penalize =  reciprocal(min(GhostDistance))
                #ghost_penalize = -min(distanceToGhosts)

        return scoreEvaluationFunction(successorGameState)- 2 * ghost_penalize + food_reward
        #return successorGameState.getScore()

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
        try:
            tuple = self.MINMAX(gameState, treedepth = 0, depth = 0)
            return tuple[0]
        except:
            print "expt"
            return Directions.STOP


    def MINMAX(self, gameState, treedepth, depth):

        Nextdepth = depth
        currentAgentIndex = treedepth % gameState.getNumAgents()
        if currentAgentIndex == 0:
            Nextdepth += 1

        if Nextdepth > self.depth:  # search limit reached, next action is unknown(random)
            return ('Random', self.evaluationFunction(gameState))

        if gameState.getLegalActions(currentAgentIndex):  # Not a leaf node
            if currentAgentIndex == 0:  # This is pacman (MAX node)
                t = ("Random", -1 * float("inf"))  # initial tuple for actions and its value
            else:
                t = ("Random", float("inf"))
            for action in gameState.getLegalActions(currentAgentIndex):
                tuple = self.MINMAX(gameState.generateSuccessor(currentAgentIndex, action), treedepth + 1, Nextdepth)
                if currentAgentIndex == 0:
                    if tuple[1] > t[1]:
                        t = (action, tuple[1])
                else:
                    if tuple[1] < t[1]:
                        t = (action, tuple[1])
            return t
        else:
            return (Directions.STOP, self.evaluationFunction(gameState))  # leaf node


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        try:
            tuple = self.MINMAX_prun(gameState, treedepth=0, depth=0, alpha = -1*float("inf"), beta = float("inf"))
            return tuple[0]                                  #tuple[0] is action, tuple[1] is state value
        except:
            print "expt"
            return Directions.STOP

    def MINMAX_prun(self, gameState, treedepth, depth, alpha, beta):

        Nextdepth = depth
        currentAgentIndex = treedepth % gameState.getNumAgents()
        if currentAgentIndex == 0:
            Nextdepth += 1

        if Nextdepth > self.depth:  # search limit reached, next action is unknown(random)
            return ('Random', self.evaluationFunction(gameState))

        if gameState.getLegalActions(currentAgentIndex):  # Not a leaf node
            if currentAgentIndex == 0:  # This is pacman (MAX node)
                t = ("Random", -1 * float("inf"))  # initial tuple for actions and its value
            else:
                t = ("Random", float("inf"))
            for action in gameState.getLegalActions(currentAgentIndex):
                tuple = self.MINMAX_prun(gameState.generateSuccessor(currentAgentIndex, action), treedepth + 1, Nextdepth, alpha, beta)
                if currentAgentIndex == 0:                              #pacman agent
                    if tuple[1] > t[1]:
                        t = (action, tuple[1])
                    if t[1] > beta:                                     # "You must not prune on equality"
                        return t
                    if t[1] >= alpha:
                        alpha = t[1]
                else:
                    if tuple[1] < t[1]:
                        t = (action, tuple[1])
                    if t[1] < alpha:                                    # "You must not prune on equality"
                        return t
                    if t[1] <= beta:
                        beta = t[1]
            return t
        else:
            return (Directions.STOP, self.evaluationFunction(gameState))  # leaf node


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
        try:
            tuple = self.ExpectimMax(gameState, treedepth = 0, depth = 0)
            return tuple[0]
        except:
            print "expt"
            return Directions.STOP

    def ExpectimMax(self, gameState, treedepth, depth):

        Nextdepth = depth
        currentAgentIndex = treedepth % gameState.getNumAgents()
        if currentAgentIndex == 0:
            Nextdepth += 1

        if Nextdepth > self.depth:  # search limit reached, next action is unknown(random)
            return ('Random', self.evaluationFunction(gameState))

        if gameState.getLegalActions(currentAgentIndex):  # Not a leaf node
            if currentAgentIndex == 0:  # This is pacman (MAX node)
                t = ("Random", -1 * float("inf"))  # initial tuple for actions and its value
            else:
                t = ("Random", 0.0)
                prob = 1.0 / float(len(gameState.getLegalActions(currentAgentIndex)))           #uniform random
                expectation = 0.0

            for action in gameState.getLegalActions(currentAgentIndex):
                tuple = self.ExpectimMax(gameState.generateSuccessor(currentAgentIndex, action), treedepth + 1, Nextdepth)
                if currentAgentIndex == 0:
                    if tuple[1] > t[1]:
                        t = (action, tuple[1])
                else:
                    expectation += prob * tuple[1]
                    t = ("Random", expectation)
            return t
        else:
            return (Directions.STOP, self.evaluationFunction(gameState))  # leaf node


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    def Average(list):
        sum = 0
        for item in list:
            sum += item
        return sum / len(list)

    def reciprocal(x):
        x = float(x)
        return 1.0 / x

    food_reward = 0.0
    ghost_penalize = 0.0
    FoodDistance = [manhattanDistance(Pos, x) for x in Food.asList()]
    if len(FoodDistance) > 0:
        if min(FoodDistance) != 0 and Average(FoodDistance) != 0:
            food_reward = 5.0 * reciprocal(Average(FoodDistance)) + reciprocal(min(FoodDistance))

    GhostPosList = [x.getPosition() for x in GhostStates]
    GhostDistance = [manhattanDistance(Pos, x) for x in GhostPosList]
    if len(GhostDistance) > 0:
        if min(GhostDistance) != 0:
            ghost_penalize = reciprocal(min(GhostDistance))
            # ghost_penalize = -min(distanceToGhosts)

    return scoreEvaluationFunction(currentGameState) - 2 * ghost_penalize + food_reward

# Abbreviation
better = betterEvaluationFunction

