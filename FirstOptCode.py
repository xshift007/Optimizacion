# -*- coding: utf-8 -*-

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)
import pandas as pd

def generate_instance_data(instance_type):
    """
    Genera datos para las 10 instancias originales (1..10).
    Devuelve (n, m, p, w, d).

    - n: número de cirugías
    - m: número de quirófanos
    - p: lista de duraciones [p1, p2, ...]
    - w: lista de pesos [w1, w2, ...]
    - d: lista de deadlines [d1, d2, ...] en minutos desde medianoche.
    """

    if instance_type == 1:
        # Instancia 1 (Hospital urbano alta complejidad, 20 cirugías, 7 quirófanos)
        n = 20
        m = 7
        # Ejemplo: 5 oftalmo(60min), 10 colecis(150min), 5 artro(180min)
        p = [
            60, 60, 60, 60, 60,
            150, 150, 150, 150, 150, 150, 150, 150, 150, 150,
            180, 180, 180, 180, 180
        ]
        w = [
            1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            5, 5, 5, 5, 5
        ]
        # Deadlines: supongamos 5 a las 10:00 (600), 10 a las 12:00 (720), 5 a las 10:00
        d = [
            600, 600, 600, 600, 600,
            720, 720, 720, 720, 720, 720, 720, 720, 720, 720,
            600, 600, 600, 600, 600
        ]

    elif instance_type == 2:
        # Instancia 2 (Hospital rural con 1 quirófano, 8 cirugías)
        n = 8
        m = 1
        p = [90]*8
        w = [2]*8
        # Deadline ejemplo 13:00 (780)
        d = [780]*8

    elif instance_type == 3:
        # Instancia 3 (Centro oftalmológico con 3 quirófanos, 15 cirugías)
        n = 15
        m = 3
        p = [60]*15
        w = [1]*15
        # Deadline 10:00 (600) para todas
        d = [600]*15

    elif instance_type == 4:
        # Instancia 4 (ejemplo inventado)
        # Digamos: 12 cirugías, 2 quirófanos
        n = 12
        m = 2
        # p: supongamos 6 de 120 min y 6 de 45 min
        p = [120]*6 + [45]*6
        # w: supongamos 6 con peso=3 y 6 con peso=1
        w = [3]*6 + [1]*6
        # deadline: 11:00 (660) para todas, por ejemplo
        d = [660]*12

    elif instance_type == 5:
        # Instancia 5 (Región Extrema, 1 quirófano, 10 cirugías)
        n = 10
        m = 1
        p = [150]*5 + [60]*5
        w = [2]*5 + [1]*5
        # Deadline 14:00 (840) en la versión original, pero lo ajustas si quieres
        d = [840]*10

    elif instance_type == 6:
        # Instancia 6 (ejemplo inventado)
        # 7 cirugías, 3 quirófanos
        n = 7
        m = 3
        # p: 3 de 100 min, 4 de 80 min
        p = [100]*3 + [80]*4
        # w: 3 con peso=2, 4 con peso=1
        w = [2]*3 + [1]*4
        # deadlines: supón 12:00 (720) para todas
        d = [720]*7

    elif instance_type == 7:
        # Instancia 7 (ejemplo inventado)
        # 6 cirugías, 2 quirófanos
        n = 6
        m = 2
        # p: 6 de 90 min
        p = [90]*6
        # w: 2,2,2,1,1,1
        w = [2,2,2,1,1,1]
        # deadlines: 11:00(660) para todas
        d = [660]*6

    elif instance_type == 8:
        # Instancia 8 (ejemplo inventado)
        # 10 cirugías, 2 quirófanos
        n = 10
        m = 2
        # p: supón 5 de 120 min, 5 de 60 min
        p = [120]*5 + [60]*5
        # w: 3,3,3,3,3,1,1,1,1,1
        w = [3]*5 + [1]*5
        # deadlines: 13:00(780) para todas
        d = [780]*10

    elif instance_type == 9:
        # Instancia 9 (ejemplo inventado)
        # 10 cirugías, 3 quirófanos
        n = 10
        m = 3
        # p: supón 10 de 60 min
        p = [60]*10
        # w: 5 con peso=2, 5 con peso=1
        w = [2]*5 + [1]*5
        # deadlines: 09:00(540) para todas (bastante exigente)
        d = [540]*10

    elif instance_type == 10:
        # Instancia 10 (ejemplo inventado)
        # 10 cirugías, 2 quirófanos
        n = 10
        m = 2
        # p: 5 de 120 min, 5 de 90 min
        p = [120]*5 + [90]*5
        # w: 3,3,3,3,3,2,2,2,2,2
        w = [3]*5 + [2]*5
        # deadlines: 16:00(960)
        d = [960]*10

    else:
        raise ValueError("Instancia no definida. Use 1..10.")

    return n, m, p, w, d


def build_model(n, m, p, w, d,
                alpha=0.5, beta=1.0, gamma=0.5,
                bigM=10000):
    """
    Construye un modelo MIP con la disyuntiva lineal (sin multiplicar variables).
    Permite que se usen instancias con p, w, d definidas.
    """

    from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpContinuous, lpSum

    prob = LpProblem("Programacion_Cirugias_Lineal", LpMinimize)

    # Puedes ajustar la ventana de tiempo si lo deseas. Ej: 06:00=360, 24:00=1440
    # Aquí lo dejamos sin bound estricto en Start/Completion para no forzar la inviabilidad.
    # Si deseas acotar, haz: lowBound=360, upBound=1440
    S = range(n)
    O = range(m)

    # x[i][o], z[i][j][o] en {0,1} (enteros en [0,1])
    x = LpVariable.dicts("x", (S,O), 0, 1, LpInteger)
    z = LpVariable.dicts("z", (S,S,O), 0, 1, LpInteger)

    # Tiempos y retraso
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    u   = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    # (Opcional) Ociosidad
    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    O_total = LpVariable("OciosidadTotal", 0)

    # H para ociosidad
    H = sum(p) + 100

    # Función objetivo
    prob += (
        alpha * lpSum(w[i] * C_i[i] for i in S) +
        gamma * lpSum(u[i] for i in S) +
        beta   * O_total
    ), "Obj"

    # Restricciones

    # 1) Asignación única
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1, f"AsigUnica_{i}"

    # 2) Completion: C_i = S_i + p_i
    for i in S:
        prob += C_i[i] == S_i[i] + p[i], f"TiempoFin_{i}"

    # 3) Disyuntiva lineal
    #    z[i][j][o] + z[j][i][o] = 1 si x[i][o]=x[j][o]=1, 0 si no están juntas.
    #    Lo haremos sin multiplicar variables, usando restricciones clásicas:
    for i in S:
        for j in S:
            if i < j:
                for o in O:
                    # No pueden precederse mutuamente en el mismo quirófano
                    prob += z[i][j][o] + z[j][i][o] <= 1, f"Disy_leq_1_{i}_{j}_{o}"

                    # z[i][j][o] = 0 si i o j no están en quirófano o
                    prob += z[i][j][o] <= x[i][o], f"Disy_zij_leq_xi_{i}_{j}_{o}"
                    prob += z[i][j][o] <= x[j][o], f"Disy_zij_leq_xj_{i}_{j}_{o}"

                    prob += z[j][i][o] <= x[i][o], f"Disy_zji_leq_xi_{i}_{j}_{o}"
                    prob += z[j][i][o] <= x[j][o], f"Disy_zji_leq_xj_{i}_{j}_{o}"

                    # Si x[i][o] = x[j][o] = 1 => sum z=1
                    # => z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] -1
                    prob += z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] - 1, f"Disy_min_{i}_{j}_{o}"

    # 4) No solapamiento
    #    si z[i][j][o] =1 => S_j >= C_i
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += S_i[j] >= C_i[i] - bigM * (1 - z[i][j][o]), f"NoSolape_{i}_{j}_{o}"

    # 5) Retraso
    for i in S:
        prob += u[i] >= C_i[i] - d[i], f"DelayPos_{i}"
        prob += u[i] >= 0,             f"DelayNoNeg_{i}"

    # 6) Trabajo en quirófano
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o] * p[i] for i in S), f"WorkQ_{o}"

    # 7) Ociosidad total
    prob += O_total == lpSum(H - w_oo[o] for o in O), "OciTotal"

    # Verificación
    bin_vars = [v for v in prob.variables() if v.cat in ("Integer","Binary")]
    print(f"Número de variables enteras/binarias en el modelo: {len(bin_vars)}")

    return prob, x, z, S_i, C_i, u, O_total


def solve_instance(instance_type, solver_path=None):
    """
    Resuelve la instancia dada (1..10), y devuelve (status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n,m,p,w,d).
    """
    # Generar datos
    n, m, p, w, d = generate_instance_data(instance_type)

    # Construir modelo con bigM=10000 (u otro)
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d,
        alpha=0.5, beta=1.0, gamma=0.5, bigM=10000
    )

    # Podemos usar CBC
    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
    else:
        solver = COIN_CMD(msg=True, timeLimit=120)

    prob.solve(solver)

    status = LpStatus[prob.status]
    obj_value = value(prob.objective)

    # Extraer soluciones
    x_sol = {(i,o): value(x[i][o]) for i in range(n) for o in range(m)}
    S_sol = {i: value(S_i[i]) for i in range(n)}
    C_sol = {i: value(C_i[i]) for i in range(n)}
    u_sol = {i: value(u[i]) for i in range(n)}
    O_total_sol = value(O_total)

    return status, obj_value, x_sol, S_sol, C_sol, u_sol, O_total_sol, n, m, p, w, d


def main():
    """
    Resuelve instancias 1..10, almacena y muestra resultados finales.
    """
    solver_path = None  # Ajustar si CBC está en otra ruta
    resultados = {}

    # Recorremos 1..10
    for inst_type in [1,2,3,4,5,6,7,8,9,10]:
        print(f"--- Resolviendo instancia {inst_type} ---")
        status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n,m,p,w,d = solve_instance(
            inst_type, solver_path=solver_path
        )
        print(f"--- Instancia {inst_type} resuelta y almacenada ---\n")

        resultados[inst_type] = {
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

    # Imprimir un resumen general
    print("================= RESULTADOS TOTALES =================\n")
    for inst_type in sorted(resultados.keys()):
        res = resultados[inst_type]
        print(f"=== Instancia {inst_type} ===")
        print(f"Status: {res['status']}")
        print(f"Valor Objetivo: {res['obj']}")

        # Asignaciones
        asigs = [(i,o) for (i,o), val in res["x_sol"].items() if val and val>0.9]
        print("\nAsignaciones (cirugía -> quirófano):")
        for (i, o) in asigs:
            print(f"  Cirugía {i} -> Quirófano {o}")

        print("\nDetalles de cada cirugía:")
        for i in range(res["n"]):
            ini = res["S_sol"][i]
            fin = res["C_sol"][i]
            ret = res["u_sol"][i]
            # Convertimos a HH:MM (si quieres)
            ini_h = f"{int(ini//60):02d}:{int(ini%60):02d}"
            fin_h = f"{int(fin//60):02d}:{int(fin%60):02d}"
            print(f"  Cirugía {i}: {ini_h} - {fin_h}, Retraso={ret}")

        print(f"\nOciosidad Total: {res['O_total']}")
        print("------------------------------------------------------------\n")

    print("=== Fin de todas las soluciones ===")


if __name__ == "__main__":
    main()
