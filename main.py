from timing import timeFunction as tf
from timing import buildGraph as bg
import random
import numpy as np

global terminal



def makeExp(n):
    # n variables (use 0 ... n-1 for variables, and n .. 2n-1 for their negation
    # we always generate 4.3 * n clauses because for some reason, this ratio
    # generates the hardest problems!
    return [[random.randint(0, 2 * n - 1) for _ in range(3)] for _ in 
range(int(4.3*n))]


def evalExp(exp, values):
    # append the negated variables at the end
    variableValues = values + [not values[i] for i in range(len(values))]
    solution = True
    for j in range(len(exp)):
        solution = solution and evalClause(exp[j], variableValues)
        if not solution: #short circuit evaluation
            break
    return solution

def evalClause(clause, variableValues):
    return variableValues[clause[0]] or variableValues[clause[1]] or variableValues[clause[2]]

def solveExp(exp, n, values=[]):
    global terminal
    # modified to return both the solution (true or false) and the variable assignments
    if n == 0:
        return (evalExp(exp, values), values)
    # Early termination strategy
    if len(terminal[n-1]) > 0:
        for i in range(len(terminal[n-1])):
            print("values: " + str(values))
            print(exp[terminal[n-1][i]])
            if not evalClause(exp[terminal[n-1][i]], values):
                return False
    # check if the partial assignment leads to any false clauses
    (solT, valuesT) = solveExp(exp, n - 1, [True] + values)
    if solT: # short circuit evaluation
        return (solT, valuesT)
    (solF, valuesF) = solveExp(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)

def walkSat(exp, n, p, maxFlips):
    # exp is the expression, n is how many variables, p is a probability usually set to 0.5,
    # maxFlips is an int
    values = randomValues(n) #generate a list of random Boolean values
    for i in range(0, maxFlips): #number of attempts at finding a solution
        if evalExp(exp, values): #found a solution
            return (True, values)
        clause = selectRandomClause(exp, values) #randomly select unsatisfied clause
        if random.random() < p: #with probability p
            # flip the value of a randomly chosen variable in clause
            index =  clause[random.randint(0, 3)]
            values[index] != values[index] 
        # else:
        #     values = #for each variable in clause, flip it and count the number of unsatisfied clauses
        #              #select the variable flip that leads to the minimum number of unsatisfied clauses
    return (False, [])

def randomValues(n):
    bitValues = [random.getrandbits(1) for _ in range(n)]
    return [True if bitValues[i] == 1 else False for i in range(n)]

def selectRandomClause(exp, values):
    clause = True
    while clause:
        index = random.randint(0, len(exp) - 1)
        newExp =  exp[index]
        clause = values[newExp[0]] or values[newExp[1]] or values[newExp[2]]
    return index

def  countUnSatis(exp, values, clause):
    newVa, newVb, newVc = values

    newVa[clause[0]] = not clause[0]
    newVb[clause[1]] = not clause[1]
    newVc[clause[2]] = not clause[2]

    op0 = checkAllExp(exp, newVa)
    op1 = checkAllExp(exp, newVb)
    op2 = checkAllExp(exp, newVc)
    result = min(op0, op1, op2)

    if result == op0:
        return 0
    elif result == op1:
        return 1
    return 2

def checkAllExp(exp, values):
    counter = 0
    for i in range(len(exp)):
        if not (values[exp[i][0]] or values[exp[i][1]] or values[exp[i][2]]):
            counter += 1
    return counter
