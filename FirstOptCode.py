# -*- coding: utf-8 -*-

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)
import pandas as pd

def generate_instance_data(instance_type):
    """
    Devuelve (n, m, p, w, d) para instancias 2, 3, 5.
    El resto se deja comentado.
    """

    if instance_type == 2:
        # Instancia 2 (Hospital rural con 1 quirófano, 8 cirugías)
        n = 8
        m = 1
        p = [90]*8
        w = [2]*8
        d = [780]*8  # Deadline ejemplo 13:00
        return n, m, p, w, d

    elif instance_type == 3:
        # Instancia 3 (Centro oftalmológico con 3 quirófanos, 15 cirugías)
        n = 15
        m = 3
        p = [60]*15
        w = [1]*15
        d = [600]*15  # 10:00 AM
        return n, m, p, w, d

    elif instance_type == 5:
        # Instancia 5 (Región Extrema, 1 quirófano, 10 cirugías)
        n = 10
        m = 1
        p = [150]*5 + [60]*5
        w = [2]*5 + [1]*5
        d = [840]*10  # 14:00
        return n, m, p, w, d

    # Instancias comentadas:

    # elif instance_type == 1:
    #     # Instancia 1
    #     ...
    # elif instance_type == 4:
    #     ...
    # elif instance_type == 6:
    #     ...
    # elif instance_type == 7:
    #     ...
    # elif instance_type == 8:
    #     ...
    # elif instance_type == 9:
    #     ...
    # elif instance_type == 10:
    #     ...
    else:
        raise ValueError("Instancia no definida o comentada. Use 2, 3 o 5.")

def build_model(n, m, p, w, d,
                alpha=0.5, beta=1.0, gamma=0.5,
                bigM=10000):
    """
    Construye el modelo MIP con disyuntiva lineal para secuenciación.
    """

    prob = LpProblem("Programacion_Cirugias_Lineal", LpMinimize)

    S = range(n)
    O = range(m)

    # x[i][o], z[i][j][o] en {0,1}
    x = LpVariable.dicts("x", (S,O), 0, 1, cat=LpInteger)
    z = LpVariable.dicts("z", (S,S,O), 0, 1, cat=LpInteger)

    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    u   = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    O_total = LpVariable("OciosidadTotal", 0)

    H = sum(p) + 100

    # Función objetivo
    prob += (
        alpha*lpSum(w[i]*C_i[i] for i in S) +
        gamma*lpSum(u[i] for i in S) +
        beta*O_total
    ), "Obj"

    # 1) Asignación única
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1

    # 2) C_i = S_i + p_i
    for i in S:
        prob += C_i[i] == S_i[i] + p[i]

    # 3) Disyuntiva lineal
    for i in S:
        for j in S:
            if i < j:
                for o in O:
                    prob += z[i][j][o] + z[j][i][o] <= 1
                    prob += z[i][j][o] <= x[i][o]
                    prob += z[i][j][o] <= x[j][o]
                    prob += z[j][i][o] <= x[i][o]
                    prob += z[j][i][o] <= x[j][o]
                    prob += z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] - 1

    # 4) No solapamiento
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += S_i[j] >= C_i[i] - bigM*(1 - z[i][j][o])

    # 5) Retraso
    for i in S:
        prob += u[i] >= C_i[i] - d[i]
        prob += u[i] >= 0

    # 6) Trabajo en quirófano
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o]*p[i] for i in S)

    # 7) Ociosidad total
    prob += O_total == lpSum(H - w_oo[o] for o in O)

    bin_vars = [v for v in prob.variables() if v.cat in ("Integer","Binary")]
    print(f"Número de variables enteras/binarias en el modelo: {len(bin_vars)}")

    return prob, x, z, S_i, C_i, u, O_total

def solve_instance(instance_type, solver_path=None):
    """
    Resuelve instancias 2, 3 o 5.
    """
    n, m, p, w, d = generate_instance_data(instance_type)
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d, alpha=0.5, beta=1.0, gamma=0.5, bigM=10000
    )

    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
    else:
        solver = COIN_CMD(msg=True, timeLimit=120)

    prob.solve(solver)

    status = LpStatus[prob.status]
    obj_value = value(prob.objective)

    x_sol = {(i,o): value(x[i][o]) for i in range(n) for o in range(m)}
    S_sol = {i: value(S_i[i]) for i in range(n)}
    C_sol = {i: value(C_i[i]) for i in range(n)}
    u_sol = {i: value(u[i]) for i in range(n)}
    O_total_sol = value(O_total)

    return status, obj_value, x_sol, S_sol, C_sol, u_sol, O_total_sol, n, m, p, w, d

def main():
    """
    Ejecuta solo las 3 instancias más fáciles: 2, 3 y 5.
    """
    solver_path = None
    results = {}

    for inst_type in [2, 3, 5]:
        print(f"--- Resolviendo instancia {inst_type} ---")
        status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n,m,p,w,d = solve_instance(
            inst_type, solver_path=solver_path
        )
        results[inst_type] = {
            "status": status,
            "obj": obj,
            "x_sol": x_sol,
            "S_sol": S_sol,
            "C_sol": C_sol,
            "u_sol": u_sol,
            "O_total": O_total,
            "n": n,
            "m": m,
            "p": p,
            "w": w,
            "d": d
        }
        print("--- Fin de instancia", inst_type, "---\n")

    # Reporte final
    print("==== RESUMEN DE LAS 3 INSTANCIAS ====\n")
    for inst_type in sorted(results.keys()):
        r = results[inst_type]
        print(f"=== Instancia {inst_type} ===")
        print("Status:", r["status"])
        print("Valor Objetivo:", r["obj"])
        asigs = [(i,o) for (i,o),val in r["x_sol"].items() if val and val>0.9]
        print("\nAsignaciones (cirugía->quirófano):", asigs)

        print("\nDetalles de cada cirugía:")
        for i in range(r["n"]):
            ini = r["S_sol"][i]
            fin = r["C_sol"][i]
            ret = r["u_sol"][i]
            ini_h = f"{int(ini//60):02d}:{int(ini%60):02d}"
            fin_h = f"{int(fin//60):02d}:{int(fin%60):02d}"
            print(f"  Cirugía {i}: {ini_h}-{fin_h}, Retraso={ret}")

        print("\nOciosidad Total:", r["O_total"])
        print("------------------------------------\n")

if __name__=="__main__":
    main()
