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
import collections

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
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for i in range(self.iterations):
            iter_values = util.Counter()
            for state in states:
                possibleActions = self.mdp.getPossibleActions(state)
                if state == 'TERMINAL_STATE':
                    iter_values[state] = 0
                    continue
                maxQValue = -999999
                for action in possibleActions:
                    tmp_QValue = self.computeQValueFromValues(state, action)
                    if tmp_QValue > maxQValue:
                        maxQValue = tmp_QValue
                iter_values[state] = maxQValue
            self.values = iter_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # print self.mdp.getTransitionStatesAndProbs(state, action)
        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        QValue = 0
        for nextStatePair in transitionStatesAndProbs:
            QValue += nextStatePair[1] * (self.mdp.getReward(state, action, nextStatePair[0]) + self.discount * self.values[nextStatePair[0]])

        return QValue

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
        # print self.values[self.values.argMax()]
        if self.mdp.isTerminal(state) == True:
            return None
        else:
            possibleActions = self.mdp.getPossibleActions(state)
            QValue = -9999
            bestAction = None
            for action in possibleActions:
                tmp_QValue = self.computeQValueFromValues(state, action)
                if tmp_QValue > QValue:
                    QValue = tmp_QValue
                    bestAction = action
            return bestAction

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        iterNum = 0
        loop = 0
        while iterNum < self.iterations:
            state = states[loop]
            if state == 'TERMINAL_STATE':
                loop = (loop + 1) % len(states)
                iterNum += 1
                continue
            possibleActions = self.mdp.getPossibleActions(state)
            maxQValue = -9999
            for action in possibleActions:
                QValue = self.computeQValueFromValues(state, action)
                if QValue > maxQValue:
                    maxQValue = QValue
            self.values[state] = maxQValue
            loop = (loop + 1) % len(states)
            iterNum += 1
            # print iterNum

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # compute the predecessors of all the states
        states = self.mdp.getStates()
        predecessors = {state:set() for state in states}
        for state in states:
            possibleActions = self.mdp.getPossibleActions(state)
            for action in possibleActions:
                transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                for successor,prob in transitionStatesAndProbs:
                    if prob == 0:
                        continue
                    predecessors[successor].add(state)
        # print predecessors

        # initialize the priorityQueue
        minheap = util.PriorityQueue()
        for state in states:
            if state == 'TERMINAL_STATE':
                continue
            curr_value = self.values[state]
            possibleActions = self.mdp.getPossibleActions(state)
            maxQValue = -999999
            for action in possibleActions:
                tmp_QValue = self.computeQValueFromValues(state, action)
                if tmp_QValue > maxQValue:
                    maxQValue = tmp_QValue
            diff = abs(curr_value - maxQValue)
            minheap.update(state, -diff)

        # Do the interations
        for i in range(self.iterations):
            if minheap.isEmpty():
                break
            pop_state = minheap.pop()
            if pop_state == 'TERMINAL_STATE':
                pass
            else:
                possibleActions = self.mdp.getPossibleActions(pop_state)
                maxQValue = -999999
                for action in possibleActions:
                    tmp_QValue = self.computeQValueFromValues(pop_state, action)
                    if tmp_QValue > maxQValue:
                        maxQValue = tmp_QValue
                self.values[pop_state] = maxQValue
            pred = predecessors[pop_state]
            for pred_state in pred:
                curr_value = self.values[pred_state]
                possibleActions = self.mdp.getPossibleActions(pred_state)
                maxQValue = -999999
                for action in possibleActions:
                    tmp_QValue = self.computeQValueFromValues(pred_state, action)
                    if tmp_QValue > maxQValue:
                        maxQValue = tmp_QValue
                diff = abs(curr_value - maxQValue)
                if diff > self.theta:
                    minheap.update(pred_state, -diff)

                    



