# -*- coding: utf-8 -*-

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)
import pandas as pd

def generate_instance_data(instance_type):
    """
    Instancias 2 y 5 con deadlines = 1440 (medianoche) para asegurar factibilidad.
    """
    if instance_type == 2:
        # 8 cirugías de 90 min, 1 quirófano
        n = 8
        m = 1
        p = [90]*8
        w = [2]*8
        d = [1440]*8
    elif instance_type == 5:
        # 10 cirugías: 5 de 150, 5 de 60, 1 quirófano
        n = 10
        m = 1
        p = [150]*5 + [60]*5
        w = [2]*5 + [1]*5
        d = [1440]*10
    else:
        raise ValueError("Instancia no definida. Use 2 o 5.")
    return n, m, p, w, d

def build_model(n, m, p, w, d,
                alpha=0.5, beta=1.0, gamma=0.5,
                bigM=1080):
    """
    Modelo MIP con disyuntiva lineal (sin multiplicar variables).
    """

    prob = LpProblem("Prog_Cirugias_lineal", LpMinimize)

    # Ventana 06:00 (360) a 24:00 (1440)
    START_DAY = 360
    END_DAY = 1440

    S = range(n)
    O = range(m)

    # x[i][o], z[i][j][o] en {0,1} (enteros con bounds [0,1])
    x = LpVariable.dicts("x", (S, O), 0, 1, cat=LpInteger)
    z = LpVariable.dicts("z", (S, S, O), 0, 1, cat=LpInteger)

    # Tiempos y retraso
    S_i = LpVariable.dicts("Start", S, lowBound=START_DAY, upBound=END_DAY, cat=LpContinuous)
    C_i = LpVariable.dicts("Completion", S, lowBound=START_DAY, upBound=END_DAY, cat=LpContinuous)
    u = LpVariable.dicts("Delay", S, lowBound=0, cat=LpContinuous)

    # Trabajo quirófano y ociosidad
    w_oo = LpVariable.dicts("Work_O", O, lowBound=0, cat=LpContinuous)
    O_total = LpVariable("OciosidadTotal", lowBound=0, cat=LpContinuous)

    H = sum(p) + 100

    # Función objetivo
    prob += (
        alpha * lpSum(w[i] * C_i[i] for i in S) +
        gamma * lpSum(u[i] for i in S) +
        beta * O_total
    ), "Obj"

    # 1. Asignación única
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1, f"AsigUnica_{i}"

    # 2. Tiempo de finalización
    for i in S:
        prob += C_i[i] == S_i[i] + p[i], f"TiempoFin_{i}"

    # 3. Disyuntiva lineal (sin multiplicar variables)
    #    Para i<j, en cada quirófano o:
    #    Queremos EXACTAMENTE uno de z[i][j][o], z[j][i][o] =1 si x[i][o]=x[j][o]=1
    #    y 0 en caso contrario.
    for i in S:
        for j in S:
            if i < j:
                for o in O:
                    # z[i][j][o] + z[j][i][o] <= 1
                    prob += z[i][j][o] + z[j][i][o] <= 1, f"Disy_leq_1_{i}_{j}_{o}"

                    # z[i][j][o] <= x[i][o], z[i][j][o] <= x[j][o]
                    prob += z[i][j][o] <= x[i][o], f"Disy_zij_leq_xi_{i}_{j}_{o}"
                    prob += z[i][j][o] <= x[j][o], f"Disy_zij_leq_xj_{i}_{j}_{o}"

                    # z[j][i][o] <= x[i][o], z[j][i][o] <= x[j][o]
                    prob += z[j][i][o] <= x[i][o], f"Disy_zji_leq_xi_{i}_{j}_{o}"
                    prob += z[j][i][o] <= x[j][o], f"Disy_zji_leq_xj_{i}_{j}_{o}"

                    # z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] - 1
                    # => si x[i][o]=x[j][o]=1 => sum z=1; en caso distinto => sum z <=1 sin forzar.
                    prob += z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] - 1, f"Disy_min_{i}_{j}_{o}"

    # 4. No solapamiento
    #    si z[i][j][o] =1 => S_j >= C_i
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += (
                        S_i[j] >= C_i[i] - bigM*(1 - z[i][j][o]),
                        f"NoSolape_{i}_{j}_{o}"
                    )

    # 5. Retraso
    for i in S:
        prob += u[i] >= C_i[i] - d[i], f"DelayPos_{i}"
        prob += u[i] >= 0, f"DelayNoNeg_{i}"

    # 6. Trabajo
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o] * p[i] for i in S), f"WorkQ_{o}"

    # 7. Ociosidad total
    prob += O_total == lpSum(H - w_oo[o] for o in O), "OciTotal"

    # Verificación
    bin_vars = [v for v in prob.variables() if v.cat in ("Integer", "Binary")]
    print(f"Número de variables enteras/binarias en el modelo: {len(bin_vars)}")

    return prob, x, z, S_i, C_i, u, O_total

def solve_instance(instance_type, solver_path=None):
    """
    Resuelve la instancia (2 o 5).
    """
    n, m, p, w, d = generate_instance_data(instance_type)

    # Construir modelo con disyuntiva lineal
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d,
        alpha=0.5, beta=1.0, gamma=0.5,
        bigM=1080
    )

    int_vars = [v for v in prob.variables() if v.cat in ("Integer", "Binary")]
    print(f"Total de variables enteras/binarias: {len(int_vars)}")

    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
    else:
        solver = COIN_CMD(msg=True, timeLimit=120)

    prob.solve(solver)

    status = LpStatus[prob.status]
    obj_value = value(prob.objective)

    # Extraer soluciones
    x_sol = {(i, o): value(x[i][o]) for i in range(n) for o in range(m)}
    S_sol = {i: value(S_i[i]) for i in range(n)}
    C_sol = {i: value(C_i[i]) for i in range(n)}
    u_sol = {i: value(u[i]) for i in range(n)}
    O_total_sol = value(O_total)

    return status, obj_value, x_sol, S_sol, C_sol, u_sol, O_total_sol, n, m, p, w, d

def main():
    """
    Ejecuta las instancias 2 y 5 con la disyuntiva lineal.
    """
    solver_path = None  # Ajusta si tienes CBC en una ruta distinta

    for inst_type in [2, 5]:
        print(f"--- Resolviendo instancia {inst_type} ---")
        status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n, m, p, w, d = solve_instance(
            inst_type, solver_path=solver_path
        )

        print("Status:", status)
        print("Valor Objetivo:", obj)

        # Asignaciones (donde x_sol ~ 1)
        asignaciones = [(i, o) for (i,o) in x_sol if x_sol[i,o] and x_sol[i,o]>0.9]
        print("Asignaciones (cirugía->quirófano):", asignaciones)

        # Detalles
        for i in range(n):
            ini = S_sol[i]
            fin = C_sol[i]
            ret = u_sol[i]
            ini_hhmm = f"{int(ini//60):02d}:{int(ini%60):02d}"
            fin_hhmm = f"{int(fin//60):02d}:{int(fin%60):02d}"
            print(f"  Cirugía {i}: {ini_hhmm}-{fin_hhmm}, Retraso={ret}")

        print("-"*50)
        print()

    print("=== Fin ===")

if __name__ == "__main__":
    main()
