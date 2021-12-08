
import random
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
        # if not solution: #short circuit evaluation
        #     break
    return solution
def evalClause(clause, variableValues):
    return variableValues[clause[0]] or variableValues[clause[1]] or 
variableValues[clause[2]]
def solveExp(exp, n, values=[]):
    # modified to return both the solution (true or false) and the variable 
assignments
    if n == 0:
        return (evalExp(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    (solT, valuesT) = solveExp(exp, n - 1, [True] + values)
    # if solT: short circuit evaluation
    #     return (solT, valuesT)
    (solF, valuesF) = solveExp(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)
# def walkSat(exp, n, p, maxFlips):
#     # exp is the expression, n is how many variables, p is a probability usually 
set to 0.5,
#     # maxFlips is an int
#     values = randomValues(n) #generate a list of random Boolean values
#     for i in range(0, maxFlips): #number of attempts at finding a solution
#         if evalExp(exp, values): #found a solution
#             return (True, values)
#         clause = selectRandomClause(exp, values) #randomly select unsatisfied 
# clause
#         if random.random() < p: #with probability p
#             values = # flip the value of a randomly chosen variable in clause
#         else:
#             values = #for each variable in clause, flip it and count the number 
# of unsatisfied clauses
#                      #select the variable flip that leads to the minimum number 
# of unsatisfied clauses
#     return (False, [])
n = 22 #always make the number of clauses 4.5* the number of variables
for i in range(100):
    exp = makeExp(n)
    (solution, values) = solveExp(exp, n, values=[])
    printSolution(exp, values, solution)
