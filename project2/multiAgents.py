# Name : Anil Kumar,    Roll no: 2003105 

# Name : Mahesh Meena,  Roll no: 2003120 



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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        distance = []    # list to srote distance of food from pacman position..

        foods = currentGameState.getFood().asList()   # for food position in current and proposed successor state

        pacman_position = list(successorGameState.getPacmanPosition())  #for pacman position in current and proposed successor state

        for Ghost_State in newGhostStates:
            if Ghost_State.getPosition() == tuple(pacman_position) and Ghost_State.scaredTimer is 0:
                return -float("inf")

        #For loop to find distanc bitween the pacman agent and the food location for urrent and proposed successor state

        for food in foods:
            distance1 = -1 * abs(food[0] - pacman_position[0])
            distance2 = -1 * abs(food[1] - pacman_position[1])
            distance.append(distance1+distance2)

        return max(distance)   # to take max distance from list....


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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #list of posible leagel actions
        legal_actions = gameState.getLegalActions(0)

        # list of successor states
        successor_states = [gameState.generateSuccessor(0, action) for action in legal_actions]

        Max_Value = -float('inf')   # assumeing max_value to be - infinity...
        index = 0    # to find the index of required action....

        for num in range(len(successor_states)):
            value = self.value(successor_states[num], 1, 0)
            if value > Max_Value:
                Max_Value = value
                index = num

        return legal_actions[index]

    #defining Max_Value function which will take the action with Maximum outcome/reward    
    def Max_Value(self, gameState, agentIndex, depth):

        #list of posible leagel actions
        legal_actions = gameState.getLegalActions(agentIndex)

        # list of successor states
        successor_states = [gameState.generateSuccessor(agentIndex, action) for action in legal_actions]

        # To find max value, Initially assuming it to be - infinity......
        Max = -float('inf')

        # for loop to find the Max value.....
        for state in successor_states:
            Max = max(Max, self.value(state, 1, depth))
        return Max

    # defining Min_value function which will take the action with minimum outcome/reward    
    def Min_Value(self, gameState, agentIndex, depth):

        #list of posible leagel actions
        legal_actions = gameState.getLegalActions(agentIndex)

        # list of successor states
        successor_states = [gameState.generateSuccessor(agentIndex, action) for action in legal_actions]

        # To find Min value, initially assuming to be + infinity .....
        Min = +float('inf')

        # for loop to find the Min value.....
        for state in successor_states:
            if agentIndex + 1 == gameState.getNumAgents():
                Min = min(Min, self.value(state, 0, depth + 1))
            else:
                Min = min(Min, self.value(state, agentIndex + 1, depth))
        return Min
        
        
    def value(self, gameState, agentIndex, depth):
        
        # If all required searches are can be completed then perform evaluation function
        if depth == self.depth or gameState.isWin() or gameState.isLose(): return self.evaluationFunction(gameState)

        # If Agent Index is 0 than perform MAX agent.....
        elif agentIndex == 0:   return self.Max_Value(gameState, agentIndex, depth)

        # If Agent Index > 0 (ghosts) than perform MIN agent....
        else:   return self.Min_Value(gameState, agentIndex, depth)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(agent, depth, game_state, alpha, beta):  # maximizer function
            temp_max = float("-inf")
            for newstate in game_state.getLegalActions(agent):
                #calculate temp max value
                temp_max = max(temp_max, alphabetaprun(1, depth, game_state.generateSuccessor(agent, newstate), alpha, beta))
                if temp_max > beta:
                    return temp_max    #if temp max value more than beta then it will return value
                alpha = max(alpha, temp_max)
            return temp_max                 #return max value

        def minimizer(agent, depth, game_state, alpha, beta):  # minimizer function
            temp_min = float("inf")                                                   #temp_min is initial value of minimizer function
             # calculate the next agent and increase depth accordingly.
            next_agent = agent + 1 
            if game_state.getNumAgents() == next_agent:
                next_agent = 0
            if next_agent == 0:
                depth += 1                     #go for next depth value

            for newstate in game_state.getLegalActions(agent):
                temp_min = min(temp_min, alphabetaprun(next_agent, depth, game_state.generateSuccessor(agent, newstate), alpha, beta))
                #if this temp_min value is most leser in this node then its return
                if temp_min < alpha:                    
                    return temp_min             
                beta = min(beta, temp_min)
            return temp_min                   #return value of min 


        #this is our main function
        def alphabetaprun(agent, depth, game_state, alpha, beta):
            # return the utility in case the defined depth is reached or the game is won/lost.
            if game_state.isLose() or game_state.isWin() or depth == self.depth:  
                return self.evaluationFunction(game_state)

            if agent == 0:                           # maximize for pacman here
                return maximizer(agent, depth, game_state, alpha, beta)
            else:                                    # minimize for ghosts here
                return minimizer(agent, depth, game_state, alpha, beta)

        #Performing maximizer function to the root node i.e. pacman using alpha-beta pruning
        utility = float("-inf")                #define utility value 
        action = Directions.WEST
        alpha = float("-inf")                  #define alpha initial value we define lesser becuse we compare by this our new alpha value which we want higher
        beta = float("inf")                         #define beta initial value

        #first we go for root node
        for agentState in gameState.getLegalActions(0):
            #count value for ghost
            ghostvalue = alphabetaprun(1, 0, gameState.generateSuccessor(0, agentState), alpha, beta)
            if ghostvalue > utility:          
                utility = ghostvalue
                action = agentState
            #we compare utility with beta 
            if utility > beta:
                return utility
            alpha = max(alpha, utility)
              #return best move or action
        return action


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
        def expectmaxfunc(agent, depth, gameState):
            #comnditions for win and lost
            if gameState.isLose() or gameState.isWin() or depth == self.depth:  
                 #if we not reach at win or lose then its return and we need to do by eveluation function 
                return self.evaluationFunction(gameState)    

            if agent == 0:  # maximizing for pacman
                return max(expectmaxfunc(1, depth, gameState.generateSuccessor(agent, newstate)) for newstate in gameState.getLegalActions(agent))
             # performing expectmaxfunc action for ghosts/chance nodes.
            else:  
                newAgent = agent + 1     
                # calculate the next agent and increase depth accordingly.
                if gameState.getNumAgents() == newAgent:
                    newAgent = 0
                if newAgent == 0:
                    #increseing depth
                    depth += 1
                return sum(expectmaxfunc(newAgent, depth, gameState.generateSuccessor(agent, newstate)) 
                for newstate in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))

        #Performing maximizing task for the root node i.e. pacman
        maximumValue = float("-inf")       #assing most less value
        action = Directions.WEST
        for agentState in gameState.getLegalActions(0):
            utility = expectmaxfunc(1, 0, gameState.generateSuccessor(0, agentState)) #count utility by expectmex function
            #campare value of utility and maximumValue function and updating values
            if utility > maximumValue or maximumValue == float("-inf"):        
                maximumValue = utility                #updating maximumValue ne value
                action = agentState
        return action                 #return best move or action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # List of all remaining foods
    foods = currentGameState.getFood().asList()

    # for pacman position in current game state
    pacman_position = currentGameState.getPacmanPosition()

    # ghosts in current state   
    ghosts = currentGameState.getGhostStates()
    active_ghosts = [] # active ghosts who can eat pacman
    scared_ghosts = [] # scared ghosts....pacman can eat these for extra points

    # To keep track of total capsules
    capsules = len(currentGameState.getCapsules())
    # To keep track of total remaining food
    total_food = len(foods)


    # This loop will check ghosts and categrise the to scared ghosts or active ghosts
    for ghost in ghosts:
        if ghost.scaredTimer:   scared_ghosts.append(ghost)  # if its a scared ghost
        else:                   active_ghosts.append(ghost)  # if its a active ghost

    # To keep treak of distances from food, active and scared ghosts
    food_distances = []
    scared_ghosts_distances = []
    active_ghosts_distances = []

    # To find distance  of different items.... 
    for food in foods:
        food_distances.append(manhattanDistance(pacman_position,food))

    for ghost in active_ghosts:
        active_ghosts_distances.append(manhattanDistance(pacman_position,ghost.getPosition()))

    for ghost in scared_ghosts:
        scared_ghosts_distances.append(manhattanDistance(pacman_position,ghost.getPosition()))

    #To calculate total score
    score = 0

    # Score for different actions or states or items....
    score += 1.5 * currentGameState.getScore()
    score += -10 * total_food        # for eating a food.....
    score += -30 * capsules          # for eating a capsule....

    # Score based on food distances....
    for distance in food_distances:              
        if distance < 3:    score +=   -1 * distance
        if distance < 7:    score += -0.5 * distance
        else:               score += -0.2 * distance
    
    for distance in scared_ghosts_distances:      # Score based on scared ghosts distances
        if distance < 3:    score += -30 * distance
        else:               score += -20 * distance

    for distance in active_ghosts_distances:      # score base on active ghosts distances
        if   distance < 3:    score +=   3 * distance
        elif distance < 7:    score +=   2 * distance
        else:                 score += 0.5 * distance

    return score


# Abbreviation
better = betterEvaluationFunction
