'''                          group no : 9
                        name : anil kumar     2003105
                        name : mahesh meena   2003120
'''


# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    '''  when we put value of  noise value is zero then we got that
     the agent will always end up in the intented successor
     state, 
     thereby it will reach the optimal policy will cross
     the bridge and it will always move in the direction of maximizing 
     expected rewards  ''' 
    answerNoise = 0
    return answerDiscount, answerNoise

def question3a():
    '''  if we want the agent to move quicky to a exit
    then the reward is kept negative so that he tries to exit as soon as possible  '''
    answerDiscount = 1
    answerNoise = 0.2
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    # We want to agent to go to exit +1 but here we choose longer way. 
    answerDiscount = 0.3
    answerNoise = 0.3
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    # we want to agent to live enough so he exits at +10 by taking risk. the reward for should be less negative than for 3(a)  
    answerDiscount = 1
    answerNoise = 0.2
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    # if the agent do not want to risk and want the exit 10 then the reward is less negative than 3(c)  
    answerDiscount = 1
    answerNoise = 0.2
    answerLivingReward = -0.03
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    # make the reward much higher than max exit reward  that way he will never exit.
    answerDiscount = 1
    answerNoise = 0.2
    answerLivingReward = 1000
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    return 'NOT POSSIBLE'
    #here this condition is not possible coz to find optimal path it needs more episods.
    answerEpsilon = None
    answerLearningRate = None
    #return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
