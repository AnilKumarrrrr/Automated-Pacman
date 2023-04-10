# 
#                                                   group no -9
#                            1.       anil kumar                   2003105
#                            2.       mahesh meena                 2003120





# factorOperations.py
# -------------------
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


from bayesNet import Factor
import operator as op
import util
import functools

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"

    # First of all we will joined catorigise given factors in two lists Cond_Var and Uncond_Var. 
    # Then append conditioned variables and unconditioned variables to their respective lists..
    # The for loop below does the same...

    # defining two lists Cond_Var and Uncond_Var

    Uncond_Var = []
    Cond_Var = [] 
    
    # this list will store all input factors 
    factor_list = [i for i in factors]

    # for loop to catogrise the factors in their respective lists...
    for factor in factor_list:
        # for conditioned variables
        Cond_Var += [i for i in factor.conditionedVariables() if i not in Cond_Var]

        # for Unconditioned variables
        Uncond_Var += [i for i in factor.unconditionedVariables() if i not in Uncond_Var]
 
    # Filters the Cond_Var list...removing any uncondVar from the list...
    for variable in Uncond_Var:
        if variable in Cond_Var:
            Cond_Var.remove(variable)

    # For new joined Factor that has variables and probability entries from the input factors.
    joinedFactor = Factor(Uncond_Var, Cond_Var, factor_list[0].variableDomainsDict())

    # Getting and calculating the probabilities
    for assignment in joinedFactor.getAllPossibleAssignmentDicts():
        probability = 1
        for factor in factor_list:
            probability = probability * factor.getProbability(assignment)

        joinedFactor.setProbability(assignment, probability)
    
    return joinedFactor


def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        # to get the uconditioned variables from the input factor...
        Uncond_Var = factor.unconditionedVariables()
        Uncond_Var.remove(eliminationVariable)   # removing elimination variable fro the factor....

        #defining new reduded factor....
        newFactor = Factor(Uncond_Var, factor.conditionedVariables(), factor.variableDomainsDict())

        # finding probability values for the new redused factor...
        for assignment in newFactor.getAllPossibleAssignmentDicts():

            probability = 0  # initilizing probability...

            # finding probaility...
            for el_variable in factor.variableDomainsDict()[eliminationVariable]:
                fullAssignment = assignment
                fullAssignment[eliminationVariable] = el_variable
                probability = probability + factor.getProbability(fullAssignment)


            newFactor.setProbability(assignment, probability)

        return newFactor

    return eliminate

eliminate = eliminateWithCallTracking()



def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain.  Since there is only one entry in that variable's domain, we 
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables 
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print("Factor failed normalize typecheck: ", factor)
            raise ValueError("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"
    #To get the unconditioned/conditioned variables from the original input factor
    Uncond_Var = list(factor.unconditionedVariables())
    Cond_Var = list(factor.conditionedVariables())

    # generating our new factor....
    # for new Factor conditioned variables...
    newCond_Var = Cond_Var + [i for i in Uncond_Var if len(factor.variableDomainsDict()[i]) == 1]

    # for new Factor conditioned variables...
    newUncond_Var = [i for i in Uncond_Var if i not in newCond_Var]

    # new factor...
    newFactor = Factor(newUncond_Var, newCond_Var,factor.variableDomainsDict())

    # Calculating the total probability for normalization purposes
    total_prob = 0
    for assignment in factor.getAllPossibleAssignmentDicts():
        total_prob = total_prob + factor.getProbability(assignment)
    
    # Generating probabilites for our newFactor
    for assignment in newFactor.getAllPossibleAssignmentDicts():
        prob = factor.getProbability(assignment)
        newFactor.setProbability(assignment, prob / total_prob)
    
    return newFactor

