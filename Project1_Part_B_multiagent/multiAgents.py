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

        
        return successorGameState.getScore()

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

        self.curr_level = 0

    def shouldEval(self, curr_level, gameState):
        if curr_level != 0:
            if gameState.isWin() or gameState.isLose() or curr_level%(self.depth*gameState.getNumAgents())==0:
                return True
        return False

    def whoAmI(self, curr_level, gameState):
        return curr_level % gameState.getNumAgents() 

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 1)
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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def recursive_down(curr_level, gameState):
            curr_state = gameState 
            if self.shouldEval(curr_level, gameState) == True: # time to evaluate the state
                return self.evaluationFunction(gameState)
            Iam = self.whoAmI(curr_level, gameState) # get the index of current agent
            # print 'I am:', Iam
            legalActions = curr_state.getLegalActions(Iam) # get a list a actions
            if Iam == 0:
                successors_score = []
                for action in legalActions:
                    # if action == 'Stop':
                    #     successors_score.append(recursive_down(curr_level+1, curr_state))
                    successor = gameState.generateSuccessor(Iam, action)
                    successors_score.append(recursive_down(curr_level+1, successor))
                return max(successors_score)
            else:
                successors_score = []
                for action in legalActions:
                    # if action == 'Stop':
                    #     successors_score.append(recursive_down(curr_level+1, curr_state))
                    successor = gameState.generateSuccessor(Iam, action)
                    successors_score.append(recursive_down(curr_level+1, successor))
                return min(successors_score)

        tmp_lv = self.curr_level
        #pacman_score = recursive_down(tmp_lv, gameState)
        legalActions = gameState.getLegalActions(0)
        successors_score = []
        for action in legalActions:
            successors_score.append(recursive_down(tmp_lv+1, gameState.generateSuccessor(0, action)))
        bestIndices = [index for index in range(len(successors_score)) if successors_score[index] == max(successors_score)]
        chosenIndex = random.choice(bestIndices)

        # self.curr_level += (self.depth*gameState.getNumAgents())
        return legalActions[chosenIndex] 

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 2)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -999999
        beta = 999999

        def recursive_down(curr_level, gameState, alpha_in, beta_in):
            alpha = alpha_in
            beta = beta_in
            curr_state = gameState 
            if self.shouldEval(curr_level, gameState) == True: # time to evaluate the state
                return self.evaluationFunction(gameState), None
            Iam = self.whoAmI(curr_level, gameState) # get the index of current agent
            # print 'I am:', Iam
            legalActions = curr_state.getLegalActions(Iam) # get a list a actions
            if Iam == 0: # it is a max node
                value = -999999
                for action in legalActions:
                    successor = gameState.generateSuccessor(Iam, action)
                    re_value, _ = recursive_down(curr_level+1, successor, alpha, beta)
                    old_value = value
                    value = max(value, re_value)
                    if value > old_value:
                        best_move = action
                    if value > beta:
                        return value, best_move
                    alpha = max(alpha, value)
                return value, best_move
            else: # it is a min node 
                value = 999999
                for action in legalActions:
                    successor = gameState.generateSuccessor(Iam, action)
                    re_value, _ = recursive_down(curr_level+1, successor, alpha, beta)
                    old_value = value
                    value = min(value, re_value)
                    if value < old_value:
                        best_move = action
                    if value < alpha:
                        return value, best_move
                    beta = min(beta, value)
                return value, best_move

        # tmp_lv = self.curr_level
        # #pacman_score = recursive_down(tmp_lv, gameState)
        # legalActions = gameState.getLegalActions(0)
        # successors_score = []
        # for action in legalActions:
        #     successors_score.append(recursive_down(tmp_lv+1, gameState.generateSuccessor(0, action), alpha, beta))
        # bestIndices = [index for index in range(len(successors_score)) if successors_score[index] == max(successors_score)]
        # # chosenIndex = random.choice(bestIndices)
        # chosenIndex = bestIndices[0]

        # self.curr_level += (self.depth*gameState.getNumAgents())
        # return legalActions[chosenIndex] 

        tmp_lv = self.curr_level
        _, action = recursive_down(tmp_lv, gameState, alpha, beta)
        # self.curr_level += (self.depth*gameState.getNumAgents())
        return action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def recursive_down(curr_level, gameState):
            curr_state = gameState 
            if self.shouldEval(curr_level, gameState) == True: # time to evaluate the state
                return self.evaluationFunction(gameState)
            Iam = self.whoAmI(curr_level, gameState) # get the index of current agent
            # print 'I am:', Iam
            legalActions = curr_state.getLegalActions(Iam) # get a list a actions
            if Iam == 0:
                successors_score = []
                for action in legalActions:
                    # if action == 'Stop':
                    #     successors_score.append(recursive_down(curr_level+1, curr_state))
                    successor = gameState.generateSuccessor(Iam, action)
                    successors_score.append(recursive_down(curr_level+1, successor))
                return max(successors_score)
            else:
                successors_score = []
                for action in legalActions:
                    # if action == 'Stop':
                    #     successors_score.append(recursive_down(curr_level+1, curr_state))
                    successor = gameState.generateSuccessor(Iam, action)
                    successors_score.append(float(recursive_down(curr_level+1, successor)))
                return float(sum(successors_score))/float(len(successors_score))

        tmp_lv = self.curr_level
        #pacman_score = recursive_down(tmp_lv, gameState)
        legalActions = gameState.getLegalActions(0)
        successors_score = []
        for action in legalActions:
            successors_score.append(recursive_down(tmp_lv+1, gameState.generateSuccessor(0, action)))
        bestIndices = [index for index in range(len(successors_score)) if successors_score[index] == max(successors_score)]
        chosenIndex = random.choice(bestIndices)

        # self.curr_level += (self.depth*gameState.getNumAgents())
        return legalActions[chosenIndex] 
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 4).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    weight_stateScore = 0.6
    stateScore = currentGameState.getScore()

    weight_foodScore = 0.2
    newFood_list = newFood.asList()
    nearest_food_dis = 9999
    for food_pos in newFood_list:
        nearest_food_dis = min(nearest_food_dis, manhattanDistance(newPos, food_pos))
    foodScore = 30/nearest_food_dis

    weight_ghostScore = 0.2
    ghostScore = 0
    for scaredTime in newScaredTimes:
        if scaredTime > 0:
            ghostScore += (scaredTime/2)
        else:
            ghostScore -= 2

    weighted_value = weight_stateScore*stateScore + weight_foodScore*foodScore + weight_ghostScore*ghostScore

    return weighted_value


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

