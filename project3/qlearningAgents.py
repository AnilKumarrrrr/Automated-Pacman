'''                          group no : 9
                        name : anil kumar     2003105
                        name : mahesh meena   2003120
'''


# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # retrning Q-value...
        return self.values[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        
        actions = self.getLegalActions(state)    # To get all possible actions for the state....

        if len(actions) == 0:   return 0   # value for terminal state is zero....
        else:   return max([self.getQValue(state, action) for action in actions])  #value for a non-terminal states is max of the qvalues of the state

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        legal_actions = self.getLegalActions(state)   # To get all possible legal actions for the state....

        action_QValue = []   # to store action and Q_values for action in legal actions for given state...

        if not legal_actions:  return None   # for terminal state....if there is no action in legal_action

        for action in legal_actions:
            # fingind q value for each legal action and append (action Q_value) pair in list..
            action_QValue.append((action, self.getQValue(state, action)))

        best_action = max(action_QValue, key=lambda x: x[1])   # to select (action, Q_value) pair with max Qvalue..

        return best_action[0]   # returning action with max Q_value..

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        #legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        legal_actions = self.getLegalActions(state)  # all legal actions...

        random_action = util.flipCoin(self.epsilon)  # random action...

        if not legal_actions:    return None   # for terminal state....if there is no action in legal_action

        elif random_action:    return random.choice(legal_actions)  # taking a random action..
        
        else:   return self.getPolicy(state)   # taking the best policy action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # updating Q_values...
        curr_Q_value = self.getQValue(state,action)    # current state Q_Value...
        next_Q_value = self.computeValueFromQValues(nextState)   # next state Q_Value...
        self.values[(state,action)] = curr_Q_value + self.alpha*(reward + self.discount* next_Q_value - curr_Q_value)
    

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * feature_vector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        #creating feature vector
        feature_vector = self.featExtractor.getFeatures(state,action)  
        q_value = 0
        #find k in feture vector
        for k in feature_vector.keys():     
          #count q values
          q_value = q_value + self.weights[k] * feature_vector[k]
        return q_value
        #return q value

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # diff = (r + gamma * max_a'  Q(s', a')) - Q(s, a)
        #counting by above formula
        diff = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        #create feture vector
        feature_vector = self.featExtractor.getFeatures(state, action)   
       #find feature in vector
        for feature in feature_vector:
            self.weights[feature] += self.alpha * diff * feature_vector[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
