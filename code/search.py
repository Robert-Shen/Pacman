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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # store each node as (curState, actionsPath, visitedStates)
    # actionsPath record the actions to the current state
    # visitedStates is a list recorded all states that have been visited on current path, used for path-checking
    start = (problem.getStartState(), [], [problem.getStartState()])
    frontier = util.Stack()
    frontier.push(start)

    while not frontier.isEmpty():
        curr = frontier.pop()
        if problem.isGoalState(curr[0]):
            return curr[1]

        for successor in problem.getSuccessors(curr[0]):
            # sample successors list: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
            if successor[0] not in curr[2]: # path-checking
                succ = (successor[0], curr[1][:]+[successor[1]], curr[2][:]+[successor[0]])
                frontier.push(succ)

    return [] # no path found

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # store each node as (curState, actionsPath)
    start = (problem.getStartState(), [])
    frontier = util.Queue()
    frontier.push(start)
    visited = [start[0]]

    while not frontier.isEmpty():
        curr = frontier.pop()
        if problem.isGoalState(curr[0]):
            return curr[1]

        for successor in problem.getSuccessors(curr[0]):
            if successor[0] not in visited: # cycle-checking
                succ = (successor[0], curr[1][:]+[successor[1]])
                frontier.push(succ)
                visited.append(successor[0])

    return [] # no path found

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    seen = {} # store optimal cost of each visited node
    path = {} # store optimal path of each visited node

    start = problem.getStartState()
    frontier.push(start, 0)
    seen[start] = 0
    path[start] = []

    while not frontier.isEmpty():
        curr = frontier.pop()

        if problem.isGoalState(curr):
            return path[curr]

        for successor in problem.getSuccessors(curr): # cycle-checking
            succCost = seen[curr] + successor[2]

            if successor[0] not in seen or succCost < seen[successor[0]]:
                seen[successor[0]] = succCost
                path[successor[0]] = path[curr][:] + [successor[1]]
                frontier.update(successor[0], succCost)

    return [] # no path found

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    seen = {} # store optimal cost of each visited node
    path = {} # store optimal path of each visited node

    start = problem.getStartState()
    start_g = 0
    start_h = heuristic(start, problem)
    start_f = start_g + start_h
    frontier.push(start, start_f)
    seen[start] = start_g
    path[start] = []

    while not frontier.isEmpty():
        curr = frontier.pop()

        if problem.isGoalState(curr):
            return path[curr]

        for successor in problem.getSuccessors(curr): # cycle-checking
            succ_g = seen[curr] + successor[2]
            succ_h = heuristic(successor[0], problem)
            succ_f = succ_g + succ_h

            if successor[0] not in seen or succ_g < seen[successor[0]]:
                seen[successor[0]] = succ_g
                path[successor[0]] = path[curr][:] + [successor[1]]
                frontier.update(successor[0], succ_f)

    return [] # no path found

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
