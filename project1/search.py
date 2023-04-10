# 
#                                                   group no -9
#                            1.       anil kumar                   2003105
#                            2.       mahesh meena                 2003120

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # create dfs_stack to store nodes
    dfs_stack = util.Stack()  
    #create a list for visited nodes  
    visited_node = []               
    # push starting node into the satck and also mark it visited
    dfs_stack.push((problem.getStartState(), [], 1))  
     #run loop till stack is empty

    while not dfs_stack.isEmpty():                       
        node = dfs_stack.pop()
        state = node[0]          # visited node
        actions = node[1]

        # To terminate and return path if we reach the goal state...
        if problem.isGoalState(state):     
            return actions
        # if persent state is not equal to goal then continue for sub node
        if state not in visited_node:   
             #append new node in visited list 
            visited_node.append(state)   
            successors = problem.getSuccessors(state) # visit child nodes

            # store state, action and cost = 1
            for sub_node in successors:          
                sub_node_state = sub_node[0]
                sub_node_action = sub_node[1]
                if sub_node_state not in visited_node:      # add sub nodes
                    sub_node_action = actions + [sub_node_action]
                    dfs_stack.push((sub_node_state, sub_node_action, 1))   #here we go for cheaking conditions of child node
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue   # importing queue

    bfs_queue = Queue()

    # lists to keep traack of visited states and path from start
    visited_states = []
    path = []

    # To check wheather initial state is goal state 
    # If so function will stop search and returns empty path...
    if problem.isGoalState(problem.getStartState()):
        return []

    # Start searching
    bfs_queue.push((problem.getStartState(),[]))

    # while loop to impliment bfs....
    while(True):

        # to terminate and return empty path if we can't find any solutions...
        if bfs_queue.isEmpty():
            return []

        # To get position and path of current state from bfs_queue...
        position,path = bfs_queue.pop()
        #to appand position of current state to visited states
        visited_states.append(position)

        # To terminate and return path if we reach the goal state...
        if problem.isGoalState(position):
            return path

        #for successors state
        successor_state = problem.getSuccessors(position)
        # adding new states in the queue....
        if successor_state:
            for item in successor_state:
                if item[0] not in visited_states and item[0] not in (state[0] for state in bfs_queue.list):
                    new_path = path + [item[1]] #new path
                    bfs_queue.push((item[0],new_path))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue   # importing priority queue

    ucf_queue = PriorityQueue()

    # lists to keep traack of visited states and path from start
    visited_states = []
    path = []

    # To check wheather initial state is goal state 
    # If so function will stop search and returns empty path...
    if problem.isGoalState(problem.getStartState()):
        return []

    # Start searching from the beginning and find a solution
    ucf_queue.push((problem.getStartState(),[]),0)

    # while loop to impliment ucf....
    while(True):

        # to terminate and return empty path if we can't find any solutions...
        if ucf_queue.isEmpty():
            return []

        # To get position and path of current state from bfs_queue...
        xy,path = ucf_queue.pop()
        #to appand position of current state to visited states
        visited_states.append(xy)

        # To terminate and return path if we reach the goal state...
        if problem.isGoalState(xy):
            return path

        #for successors state
        successor = problem.getSuccessors(xy)
        if successor:
            for item in successor:
                if item[0] not in visited_states and (item[0] not in (state[2][0] for state in ucf_queue.heap)):
                    new_path = path + [item[1]]
                    priority = problem.getCostOfActions(new_path)
                    ucf_queue.push((item[0],new_path),priority)

                # To check if current path is cheaper from the previous one
                elif item[0] not in visited_states and (item[0] in (state[2][0] for state in ucf_queue.heap)):
                    for state in ucf_queue.heap:
                        if state[2][0] == item[0]:
                            old_priority = problem.getCostOfActions(state[2][1])

                    new_priority = problem.getCostOfActions(path + [item[1]])

                    # if the new priority is cheaper than the old one then update previous state.
                    if old_priority > new_priority:
                        new_path = path + [item[1]]
                        ucf_queue.update((item[0],new_path),new_priority)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # track visited nodes
    astar_queue = util.PriorityQueue()    
    visited_states = []

     # push initial state to astar_queue
    astar_queue.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))  
    while not astar_queue.isEmpty():
        node = astar_queue.pop()
        state = node[0]
        actions = node[1]

         # To terminate and return path if we reach the goal state...
        if problem.isGoalState(state):    
            return actions

         # visit child nodes
        if state not in visited_states:            
            visited_states.append(state)
            successors = problem.getSuccessors(state)
             # store state, action and cost = 1
            for child in successors:       
                sub_node_state = child[0]
                sub_node_action = child[1]            #steps for sub node successor

                # add child nodes and cheaking total cost
                if sub_node_state not in visited_states:               
                    sub_node_action = actions + [sub_node_action]
                    cost = problem.getCostOfActions(sub_node_action)  

                    #calculating coast of child state and comparing
                    astar_queue.push((sub_node_state, sub_node_action, 0), cost + heuristic(sub_node_state, problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
