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
    DFS_fringe = util.Stack()
    trace_list = []
    history_node = set()
    start = (problem.getStartState(), trace_list)
    #print "Start:", start[0]
    #print "Start's successors:", problem.getSuccessors(start[0])
    DFS_fringe.push(start)
    while True:
        if DFS_fringe.isEmpty():
            print "Fringe is empty!:("
            break
        (node, current_trace) = DFS_fringe.pop()
        if problem.isGoalState(node):
            #print "Final trace:", current_trace
            return current_trace                                 #exit and return result
        else:
            if node in history_node:
                pass
            else:
                for successor_node, successor_direction, _ in problem.getSuccessors(node):
                    new_trace = list(current_trace)               #deep-copy the trace for new node
                    new_trace.append(successor_direction)
                    DFS_fringe.push((successor_node, new_trace)) #push to fringe
                history_node.add(node)                          #graph search

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    BFS_fringe = util.Queue()
    trace_list = []
    history_node = set()
    start = (problem.getStartState(), trace_list)
    #print "Start:", start[0]
    #print "Start's successors:", problem.getSuccessors(start[0])
    BFS_fringe.push(start)
    while True:
        if BFS_fringe.isEmpty():
            print "Fringe is empty!:("
            break
        (node, current_trace) = BFS_fringe.pop()
        if problem.isGoalState(node):
            #print "Final trace:", current_trace
            return current_trace                                 #exit and return result
        else:
            if node in history_node:
                pass
            else:
                for successor_node, successor_direction, _ in problem.getSuccessors(node):
                    new_trace = list(current_trace)               #deep-copy the trace for new node
                    new_trace.append(successor_direction)
                    BFS_fringe.push((successor_node, new_trace)) #push to fringe
                history_node.add(node)                          #graph search
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    UCS_fringe = util.PriorityQueue()
    trace_list = []
    history_node = set()
    start = (problem.getStartState(), trace_list, 0)
    #print "Start:", start[0]
    #print "Start's successors:", problem.getSuccessors(start[0])
    UCS_fringe.push(start, 0)                                   # priority(cost) = 0 at beginning
    while True:
        if UCS_fringe.isEmpty():
            print "Fringe is empty!:("
            break
        (node, current_trace, priority) = UCS_fringe.pop()      # get a node from black-box-PriorityQueue
        if problem.isGoalState(node):
            #print "Final trace:", current_trace
            return current_trace                                # exit and return result
        else:
            if node in history_node:
                pass
            else:
                for successor_node, successor_direction, successor_priority in problem.getSuccessors(node):
                    new_trace = list(current_trace)              #deep-copy the trace for new node
                    new_trace.append(successor_direction)
                    new_priority = priority + successor_priority
                    UCS_fringe.push((successor_node, new_trace, new_priority), new_priority) #push to fringe
                history_node.add(node)                           #graph search
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    aStar_fringe = util.PriorityQueue()
    trace_list = []
    history_node = set()
    start = (problem.getStartState(), trace_list, 0)
    #print "Start:", start[0]
    #print "Start's successors:", problem.getSuccessors(start[0])
    aStar_cost = 0 + heuristic(problem.getStartState(), problem)    # f = g + h
    aStar_fringe.push(start, aStar_cost)                            # priority(cost) = 0 at beginning
    while True:
        if aStar_fringe.isEmpty():
            print "Fringe is empty!:("
            break
        (node, current_trace, priority) = aStar_fringe.pop()        # get a node from black-box-PriorityQueue
        if problem.isGoalState(node):
            #print "Final trace:", current_trace
            return current_trace                                    # exit and return result
        else:
            if node in history_node:
                pass
            else:
                for successor_node, successor_direction, successor_priority in problem.getSuccessors(node):
                    new_trace = list(current_trace)                 #deep-copy the trace for new node
                    new_trace.append(successor_direction)
                    new_priority = priority + successor_priority
                    new_state = (successor_node, new_trace, new_priority)
                    new_aStar = new_priority + heuristic(successor_node, problem)
                    aStar_fringe.push(new_state, new_aStar)         #push to fringe
                history_node.add(node)                              #graph search
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
