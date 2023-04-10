'''                          group no : 9
                        name : anil kumar     2003105
                        name : mahesh meena   2003120
'''


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

        # for loop for value iterationn.....
        for i in range(self.iterations):
            iterValue = self.values.copy()    # to store iteration value for a state.

            #for loop to look for each state and get iteration value....
            for state in self.mdp.getStates():

                iter_values = [float('-inf')]  

                # For terminal state, has 0 iterValue.....
                if self.mdp.isTerminal(state):  iterValue[state] = 0

                # For non-terminal state, iterValue is maximum of expected sum of rewards of different actions.
                else:
                    actions = self.mdp.getPossibleActions(state)   # for all leagel actions...

                    # this for loop will append possible q values for all leagel actions in list iter_values
                    for action in actions:
                        iter_values.append(self.getQValue(state, action))

                    # To find the max iter_value and update the result as iterValue for the state...
                    iterValue[state] = max(iter_values)

            self.values = iterValue


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
        #computing the transitions states and probability
        possible_State = self.mdp.getTransitionStatesAndProbs(state, action)  # next possible state..
        
        Q_value = 0   # To store the q-value...

        # Q_value is sum of rewards for all possible transitions at a given state.... 
        for tran_state in possible_State:

            # calculating reward for a transition 
            reward = self.mdp.getReward(state, action, tran_state[0])

            Q_value = Q_value + reward + self.discount*(self.values[tran_state[0]]*tran_state[1])

        # returning final Q_value for action at given state.....
        return Q_value
 

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)    # for all leagel actions...

        # for terminal state there is no possible action...means no policy..
        if len(actions) == 0:   
            return None

        qvalues = []   # to store Q-value of all possible leagel actions...

        # this for loop will find Q_value for all leagel actions and appent all to Q_values list..
        for action in actions:
            qvalue = self.getQValue(state, action)
            qvalues.append((action, qvalue))

        # finding best policy with highest Q_value...
        best_policy = max(qvalues, key=lambda x: x[1])[0]

        # returning best policy...
        return best_policy

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

        states_list = self.mdp.getStates() # list of states.....

        # initialize value function for all states to  0.
        for s in states_list :
            self.values[s] = 0

        # for given number(here 1000) of value iterations on states list....
        # means this loop will run for 1000 times and for each iteration it will update the val;ue for one state
        for i in range(self.iterations):
            index = i % (len(states_list))
            s = states_list[index]

            # if the current state is not terminal state.... nothing happens here if its a terminal state.....
            if not self.mdp.isTerminal(s):

                action = self.getAction(s)              # action for next 
                Q_value = self.getQValue(s, action)     # calculating q- value for the iteration...
                self.values[s] = Q_value


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
        mdp_states = self.mdp.getStates()       #getting states
        fring = util.PriorityQueue()            #queue frings decleration
        pred = {}                       #declare predecessor
        #cheaking is s in states 
        for s in mdp_states:
            #assing action if above condition is true
            self.values[s] = 0
            pred[s] = self.get_predecessor(s)

        for s in mdp_states:
            #this is for terminal state
            terminal = self.mdp.isTerminal(s)

            if not terminal:
                #this is for not a terminal state
                current_val_state = self.values[s]                   # here we calculatin current value of state   
                #calculating diffrence in states          
                differnce_state_values = abs(current_val_state - self.max_Qvalue(s))  #calculating diffrence in states
                fring.push(s, -differnce_state_values)  #push values

        for _ in range(self.iterations):
            #if fringe is empty
            if fring.isEmpty():
                return
            #pop in fringe
            s = fring.pop()
            self.values[s] = self.max_Qvalue(s)
            
            for p in pred[s]:
                #calculating diffrence in states
                differnce_state_values = abs(self.values[p] - self.max_Qvalue(p))
                #comparing values
                if differnce_state_values > self.theta:
                    fring.update(p, -differnce_state_values)

    #define a function for use in above part
    def max_Qvalue(self, state):
        return max([self.getQValue(state, a) for a in self.mdp.getPossibleActions(state)])


    # First, we define the predecessor of a state s as all states that have
    # a nonzero probability of reaching s by taking some action a
    # This means no Terminal states and T > 0.
    def get_predecessor(self, state):
        pred_set = set()   #create a set
        mdp_states = self.mdp.getStates()  #define states
        movements = ['north', 'south', 'east', 'west']  #possible actions
         #cheaking conditions

        if not self.mdp.isTerminal(state):
           #cheak p is in states or not 
            for p in mdp_states:
                terminal = self.mdp.isTerminal(p)
                legalactions = self.mdp.getPossibleActions(p)

                if not terminal:
                    #loop for every move
                    for move in movements:
                     #cheak is move is legal or not
                        if move in legalactions:
                            #if move is valid / legal
                            transitions = self.mdp.getTransitionStatesAndProbs(p, move)

                            for s_prime, T in transitions:
                                if (s_prime == state) and (T > 0):
                                    pred_set.add(p)
        return pred_set
