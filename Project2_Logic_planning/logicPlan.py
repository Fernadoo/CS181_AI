# logicPlan.py
# ------------
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


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    r1 = logic.disjoin(A,B)
    r2 = (~A) % logic.disjoin(~B, C)
    r3 = logic.disjoin(~A, ~B, C)
    return logic.conjoin(r1, r2, r3)
    util.raiseNotDefined()

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    r1 = C % logic.disjoin(B, D)
    r2 = A >> logic.conjoin(~B, ~D)
    r3 = ~(logic.conjoin(B, ~C)) >> A
    r4 = ~D >> C
    # print logic.pycoSAT(logic.to_cnf(logic.conjoin(r1, r2, r3)))
    return logic.conjoin(r1, r2, r3, r4)
    util.raiseNotDefined()

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    wAlive_0 = logic.PropSymbolExpr('WumpusAlive', 0)
    wAlive_1 = logic.PropSymbolExpr('WumpusAlive', 1)
    wBorn_0 = logic.PropSymbolExpr('WumpusBorn', 0)
    wKilled_0 = logic.PropSymbolExpr('WumpusKilled', 0)
    r1 = wAlive_1 % logic.disjoin(logic.conjoin(wAlive_0, ~wKilled_0), logic.conjoin(~wAlive_0, wBorn_0))
    r2 = ~logic.conjoin(wAlive_0, wBorn_0)
    r3 = wBorn_0
    # print logic.pycoSAT(logic.to_cnf(logic.conjoin(r1, r2, r3)))
    return logic.conjoin(r1, r2, r3)

    util.raiseNotDefined()

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    assign = logic.pycoSAT(cnf)
    if assign == False:
        return False
    return assign
    util.raiseNotDefined()

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)
    util.raiseNotDefined()


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    conjunctions = []
    for i in range(len(literals)):
        for j in range(i+1, len(literals)):
            disjunction = logic.disjoin(~literals[i], ~literals[j])
            conjunctions.append(disjunction)
    return logic.conjoin(conjunctions)
    util.raiseNotDefined()


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    conjunctions = []
    for i in range(len(literals)):
        for j in range(i+1, len(literals)):
            disjunction = logic.disjoin(~literals[i], ~literals[j])
            conjunctions.append(disjunction)
    conjunctions.append(logic.disjoin(literals))
    return logic.conjoin(conjunctions)

    # return atLeastOne(literals) & atMostOne(literals)

    util.raiseNotDefined()


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    move_list = []
    for key in model.keys():
        if model[key] == True:
            ex_info = logic.PropSymbolExpr.parseExpr(key)
            # print ex_info
            if ex_info[0] in actions:
                move_list.append(ex_info) 
    # print move_list
    plan = map(lambda x: x[0], sorted(move_list, key= lambda move: eval(move[1])))
    return plan
    util.raiseNotDefined()


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    curr_state = logic.PropSymbolExpr('P', x, y, t)

    prev_disjunctions = []
    if not walls_grid[x-1][y]:
        # move eastward
        prev_state = logic.PropSymbolExpr('P', x-1, y, t-1)
        action = logic.PropSymbolExpr('East', t-1)
        prev_disjunctions.append(logic.conjoin(prev_state, action))
    if not walls_grid[x][y-1]:
        # move northward
        prev_state = logic.PropSymbolExpr('P', x, y-1, t-1)
        action = logic.PropSymbolExpr('North', t-1)
        prev_disjunctions.append(logic.conjoin(prev_state, action))
    if not walls_grid[x+1][y]:
        # move westward
        prev_state = logic.PropSymbolExpr('P', x+1, y, t-1)
        action = logic.PropSymbolExpr('West', t-1)
        prev_disjunctions.append(logic.conjoin(prev_state, action))
    if not walls_grid[x][y+1]:
        # move southward
        prev_state = logic.PropSymbolExpr('P', x, y+1, t-1)
        action = logic.PropSymbolExpr('South', t-1)
        prev_disjunctions.append(logic.conjoin(prev_state, action))

    prev_state_and_actions = logic.disjoin(prev_disjunctions)
    axiom = curr_state % prev_state_and_actions
    
    return axiom 


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_position = problem.getStartState() # return (2,2)
    goal_position = problem.getGoalState() # returrn(1,1)
    actions = ['East', 'North', 'South', 'West']

    # start at ONE position
    # whole_start_state = []
    # for i in range(1, width+1):
    #     for j in range(1, height+1):
    #         whole_start_state.append(logic.PropSymbolExpr('P', i, j, 0))
    # start_state = exactlyOne(whole_start_state) & logic.PropSymbolExpr('P', start_position[0], start_position[1], 0)

    # start at ONE position
    whole_start_state = []
    for x in range(1, width+1) :
        for y in range(1, height+1) :
            if (x, y) == start_position:
                if whole_start_state:
                    whole_start_state[0] = logic.conjoin(whole_start_state[0], logic.PropSymbolExpr("P", x, y, 0))
                else:
                    whole_start_state.append(logic.PropSymbolExpr("P", x, y, 0))
            else:
                if whole_start_state:
                    whole_start_state[0] = logic.conjoin(whole_start_state[0], ~logic.PropSymbolExpr("P", x, y, 0))
                else:
                    whole_start_state.append(logic.Expr("~", logic.PropSymbolExpr("P", x, y, 0)))
    start_state = whole_start_state[0]

    action_state_list = []
    successor_state_list = []
    for t in range(51):
        # create an action logic expr at each time point, only one action at a time
        # print t
        tmp = []
        for action in actions:
            tmp.append(logic.PropSymbolExpr(action, t))
        action_state_list.append(exactlyOne(tmp))
        
        # create a successor state for next t
        suc = []
        for x in range(1, width+1):
            for y in range(1, height+1):
                if (x, y) not in walls.asList():
                    suc.append(pacmanSuccessorStateAxioms(x, y, t+1, walls))
        suc = logic.conjoin(suc)
        if len(successor_state_list) == 0:
            successor_state_so_far = suc
        else:
            successor_state_so_far = logic.conjoin(suc, logic.conjoin(successor_state_list))

        # goal test
        # # goal_state = logic.conjoin(logic.PropSymbolExpr('P', goal_position[0], goal_position[1]), pacmanSuccessorStateAxioms(goal_position[0], goal_position[1], t+1, walls))
        # whole_goal_state = []
        # for i in range(1, width+1):
        #     for j in range(1, height+1):
        #         whole_goal_state.append(logic.PropSymbolExpr('P', i, j, t+1))
        # goal_state = exactlyOne(whole_goal_state) & logic.PropSymbolExpr('P', goal_position[0], goal_position[1], t+1)
        
        whole_goal_state = []
        for x in range(1, width+1) :
            for y in range(1, height+1) :
                if (x, y) == goal_position:
                    if whole_goal_state:
                        whole_goal_state[0] = logic.conjoin(whole_goal_state[0], logic.PropSymbolExpr("P", x, y, t+1))
                    else:
                        whole_goal_state.append(logic.PropSymbolExpr("P", x, y, t+1))
                else:
                    if whole_goal_state:
                        whole_goal_state[0] = logic.conjoin(whole_goal_state[0], ~logic.PropSymbolExpr("P", x, y, t+1))
                    else:
                        whole_goal_state.append(logic.Expr("~", logic.PropSymbolExpr("P", x, y, t+1)))
        goal_state = whole_goal_state[0]

        # find a solution
        tmp = []
        tmp.append(logic.conjoin(action_state_list))
        tmp.append(successor_state_so_far)
        tmp.append(goal_state)
        tmp.append(start_state)
        solution = findModel(logic.conjoin(tmp))
        # solution = findModel(logic.conjoin(start_state, goal_state, logic.conjoin(action_state_list), logic.conjoin(successor_state_list)))
        if solution != False:
            return extractActionSequence(solution, actions)
        
        successor_state_list.append(suc)

    print problem.getStartState()
    print problem.getGoalState()
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_position = problem.getStartState()[0]
    fool_list = problem.getStartState()[1].asList()
    actions = ['East', 'North', 'South', 'West']

    # start at ONE position
    whole_start_state = []
    for i in range(1, width+1):
        for j in range(1, height+1):
            whole_start_state.append(logic.PropSymbolExpr('P', i, j, 0))
    start_state = exactlyOne(whole_start_state) & logic.PropSymbolExpr('P', start_position[0], start_position[1], 0)

    action_state_list = []
    successor_state_list = []
    for t in range(51):
        # create an action logic expr at each time point, only one action at a time
        # print t
        tmp = []
        for action in actions:
            tmp.append(logic.PropSymbolExpr(action, t))
        action_state_list.append(exactlyOne(tmp))
        # create a successor state for next t
        for x in range(1, width+1):
            for y in range(1, height+1):
                if (x, y) not in walls.asList():
                    successor_state_list.append(pacmanSuccessorStateAxioms(x, y, t+1, walls)) # no logic operation yet
        # food state
        food_visited = []
        for food in fool_list:
            disjunction = []
            for t_ in range(t+2):   
                disjunction.append(logic.PropSymbolExpr('P', food[0], food[1], t_))
            food_visited.append(logic.disjoin(disjunction))

        # find a solution
        tmp = action_state_list + successor_state_list + food_visited
        tmp.append(start_state)
        solution = findModel(logic.conjoin(tmp))
        if solution != False:
            return extractActionSequence(solution, actions)

    print problem.getStartState()[0]
    print problem.getStartState()[1].asList()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    