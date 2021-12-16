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

def printSolution(exp, values, solution):
    variableValues = values + [not values[i] for i in range(len(values))]
    print("Solution is " + (" True " if solution else "False"))
    if solution:
        print("Variables = " + ''.join(["T " if values[i] else "F " for i in 

range(len(values))]))
        print("Clauses ")
        for clause in exp:
            print('(' + ''.join(["T " if variableValues[var] else "F " for var in 
clause]) + ')')

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


def evalExp0(exp, values):
    # append the negated variables at the end
    variableValues = values + [not values[i] for i in range(len(values))]
    solution = True
    for j in range(len(exp)):
        solution = solution and evalClause(exp[j], variableValues)
    return solution

def solveExp0(exp, n, values=[]):
    # modified to return both the solution (true or false) and the variable assignments
    if n == 0:
        return (evalExp0(exp, values), values)
    (solT, valuesT) = solveExp0(exp, n - 1, [True] + values)
    (solF, valuesF) = solveExp0(exp, n - 1, [False] + values)
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

def  leastUnSat(exp, values):
    return 0


# n = 8 #always make the number of clauses 4.5* the number of variables

# code provided for initial testing
def initialTest(n):
    for i in range(100):
        exp = makeExp(n)
        (solution, values) = solveExp(exp, n, values=[])
        printSolution(exp, values, solution)

# first time study no improvements
def algorithm0(n):
    exp = makeExp(n)
    (solution, values) = solveExp0(exp, n, values=[])
    # printSolution(exp, values, solution)
    if solution: print(values)

# single short circuit improvement
def algorithm1(n):
    # alg0 -> alg1 uncomment evalExp short circuit
    exp = makeExp(n)
    (solution, values) = solveExp(exp, n, values=[])
    # printSolution(exp, values, solution)
    if solution: print(values)

# additional short circuit in solveExp
def algorithm2(n):
    # alg1 -> alg2 uncomment solveExp short circuit
    exp = makeExp(n)
    (solution, values) = solveExp(exp, n, values=[])
    # printSolution(exp, values, solution)
    if solution: print(values)


def algorithm3(n):
    global terminal
    # alg1 -> alg2 uncomment solveExp short circuit
    exp = makeExp(n)
    terminal = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (exp[j, 0]<i and exp[j,1]<i and exp[j,2]<i):
                terminal[i].append(j)

    (solution, values) = solveExp(exp, n, values=[])
    if solution: print(values)

def compare03(n):
    global terminal
    exp = makeExp(n)
    # get solutions for algorithm 0
    (solution0, values0) = solveExp0(exp, n, values=[])

    # create the termination dictionary
    terminal = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (exp[j][0]<n-i-1 and exp[j][1]<n-i-1 and exp[j][2]<n-i-1):
                terminal[i].append(j)

    # get solutions for algorithm3
    (solution3, values3) = solveExp(exp, n, values=[])

    # print the results
    if (solution3 == solution0):
        print("success")
    else: 
        print("Soltion0: " + values0)
        print("Solution3: " + values3)


# compare03(8)
# compare03(9)
# compare03(10)
# compare03(11)


# colors = ['magenta', 'cyan', 'lawngreen', 'red', 'black']
# experiments = [i for i in range(12, 23)]
# algorithm = [algorithm0, algorithm1, algorithm2, algorithm3]
# for i in range(3):
#     tf(algorithm[i], experiments, colors[i])

# bg()

# print(randomValues(5))