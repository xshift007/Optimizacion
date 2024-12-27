from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpBinary, COIN_CMD, LpStatus, value

prob = LpProblem("Test_Bin", LpMinimize)

# Variable binaria
x = LpVariable("x", cat=LpBinary)
# Forzamos el valor de x entre 0 y 1 (normalmente no hace falta, pero para descartar)
prob += x >= 0, "LowerBound"
prob += x <= 1, "UpperBound"

# Minimizamos x
prob += x, "Objective"

print("Categoría de x definida en Python:", x.cat)

solver = COIN_CMD(msg=True, timeLimit=120)
prob.solve(solver)

print("Solver status:", LpStatus[prob.status])
print("x =", x.varValue)
