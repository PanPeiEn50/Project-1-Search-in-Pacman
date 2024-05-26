# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack1 = util.Stack()
    stack2 = util.Stack()
    visited = []
    startState = problem.getStartState()
    startAction = []

    stack1.push(startState)
    stack2.push(startAction)


    while stack1:
        actions = stack2.pop()
        currentState = stack1.pop()
        if currentState not in visited:
            visited.append(currentState)    # check if the current is visited

            if problem.isGoalState(currentState):
                return actions
            else:
                successors = problem.getSuccessors(currentState)    # get the successor of the current state
                
                for successor, action, step_cost in successors:      # push successor to stack
                    newAction = actions + [action]
                    newState = successor
                    stack1.push(newState)
                    stack2.push(newAction)

    return actions  

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue1 = util.Queue()
    queue2 = util.Queue()
    visited = []
    startState = problem.getStartState()
    startAction = []

    queue1.push(startState)
    queue2.push(startAction)

    while queue1:
        actions = queue2.pop()
        currentState = queue1.pop()

        if currentState not in visited:
            visited.append(currentState)    # check if the current is visited

            if problem.isGoalState(currentState):
                return actions
            else:
                successors = problem.getSuccessors(currentState)    # get the successor of the current state
                
                for successor, action, step_cost in successors:      # push successor to stack
                    newAction = actions + [action]
                    newState = successor
                    queue1.push(newState)
                    queue2.push(newAction)

    return actions  

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pqueue1 = util.PriorityQueue()
    pqueue2 = util.PriorityQueue()
    pqueue3 = util.PriorityQueue()

    visited = []
    startState = problem.getStartState()
    startAction = []
    startCost = 0

    pqueue1.push(startState,0)
    pqueue2.push(startAction,0)
    pqueue3.push(startCost,0)

    while pqueue1:
        currentState = pqueue1.pop()
        actions = pqueue2.pop()
        cost = pqueue3.pop()

        if currentState not in visited:
            visited.append(currentState)  # check if the current state is visited

            if problem.isGoalState(currentState):
                return actions 

            for successor, action, step_cost in problem.getSuccessors(currentState):
                newActions = actions + [action]
                newCost = cost + step_cost
                if successor not in visited:
                    pqueue1.push(successor, newCost)
                    pqueue2.push(newActions, newCost)
                    pqueue3.push(newCost, newCost)

    return actions

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pqueue1 = util.PriorityQueue()
    pqueue2 = util.PriorityQueue()
    pqueue3 = util.PriorityQueue()

    # Set for holding explored states to improve lookup times
    visited = []

    # Initial state, actions, and cost
    startState = problem.getStartState()
    startAction = []
    startCost = 0

    # Push the start node with priority 0 (cost + heuristic)
    pqueue1.push(startState, heuristic(startState, problem))
    pqueue2.push(startAction, heuristic(startState, problem))
    pqueue3.push(startCost, heuristic(startState, problem))

    while pqueue1:
        currentState = pqueue1.pop()
        actions = pqueue2.pop()
        cost = pqueue3.pop()

        # If the goal is reached, return the actions to get there
        if problem.isGoalState(currentState):
            return actions

        # Add currentState to explored if it's not already there
        if currentState not in visited:
            visited.append(currentState)

            # Explore successors
            for successor, action, step_cost in problem.getSuccessors(currentState):
                newActions = actions + [action]
                newCost = cost + step_cost

                # If succState is not explored or can be reached with a lower cost, explore it
                if successor not in visited:
                    pqueue1.push(successor,  newCost + heuristic(successor, problem))
                    pqueue2.push(newActions, newCost + heuristic(successor, problem))
                    pqueue3.push(newCost, newCost + heuristic(successor, problem))

    # Return an empty list if no path is found
    return actions 


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
