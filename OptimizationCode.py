# -*- coding: utf-8 -*-

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)
import pandas as pd

def generate_instance_data(instance_type):
    """
    Genera los datos de entrada para una instancia específica basada en el tipo de hospital.

    Parámetros:
        instance_type (int): Tipo de instancia (1, 2, 3 o 5).

    Retorna:
        tuple: Contiene el número de cirugías (n), número de quirófanos (m),
               lista de duraciones de cirugías (p), pesos/prioridades (w),
               y deadlines (d) para cada cirugía en minutos desde la medianoche.
    """
    if instance_type == 1:
        # Instancia 1: Hospital urbano alta complejidad
        n = 20  # Número total de cirugías
        m = 7   # Número de quirófanos disponibles
        # Detalle de las cirugías:
        # 5 oftalmológicas (60 minutos, peso=1, deadline=10:00 AM)
        # 10 colecistectomías (150 minutos, peso=2, deadline=12:00 PM)
        # 5 artroscopias (180 minutos, peso=5, deadline=10:00 AM)
        p = [60, 60, 60, 60, 60, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 180, 180, 180, 180, 180]
        w = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5]
        d = [600, 600, 600, 600, 600, 720, 720, 720, 720, 720, 720, 720, 720, 720, 720, 600, 600, 600, 600, 600]  # 10:00 AM y 12:00 PM

    elif instance_type == 2:
        # Instancia 2: Hospital rural con 1 quirófano
        n = 8
        m = 1
        p = [90] * 8      # Todas las cirugías duran 90 minutos
        w = [2] * 8       # Peso=2 para todas las cirugías
        d = [780] * 8     # Deadline de 13:00 (780 minutos desde la medianoche)

    elif instance_type == 3:
        # Instancia 3: Centro oftalmológico con 3 quirófanos
        n = 15
        m = 3
        p = [60] * 15     # Todas las cirugías duran 60 minutos
        w = [1] * 15      # Peso=1 para todas las cirugías
        d = [600] * 15    # Deadline de 10:00 AM (600 minutos desde la medianoche)

    elif instance_type == 5:
        # Instancia 5: Región Extrema (Magallanes) con 1 quirófano
        n = 10
        m = 1
        p = [150, 150, 150, 150, 150, 60, 60, 60, 60, 60]  # 5 cirugías de 150 min y 5 de 60 min
        w = [2, 2, 2, 2, 2, 1, 1, 1, 1, 1]                  # 5 cirugías con peso=2 y 5 con peso=1
        d = [840] * 10                                     # Deadline de 14:00 (840 minutos desde la medianoche)
    else:
        raise ValueError("Instancia no definida. Use 1, 2, 3 o 5.")
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

                    # z[j][i][o] <= x[i][o}, z[j][i][o] <= x[j][o]
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
    Resuelve la instancia (1, 2, 3 o 5).
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
        solver = COIN_CMD(path=solver_path, msg=False, timeLimit=120)  # Desactivar mensajes del solver
    else:
        solver = COIN_CMD(msg=False, timeLimit=120)  # Desactivar mensajes del solver

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
    Ejecuta las instancias 1, 2, 3 y 5 con la disyuntiva lineal.
    Almacena las soluciones y las muestra al final.
    """
    solver_path = None  # Ajusta si tienes CBC en una ruta distinta
    instance_types = [1, 2, 3, 5]

    # Lista para almacenar las soluciones
    soluciones = []

    for inst_type in instance_types:
        print(f"--- Resolviendo instancia {inst_type} ---")
        status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n, m, p, w, d = solve_instance(
            inst_type, solver_path=solver_path
        )

        # Almacenar la solución en un diccionario
        solucion = {
            'Instancia': inst_type,
            'Status': status,
            'Valor Objetivo': obj,
            'Asignaciones': [(i, o) for (i, o) in x_sol if x_sol[i, o] and x_sol[i, o] > 0.9],
            'Detalles': [
                {
                    'Cirugía': i,
                    'Inicio': f"{int(S_sol[i]//60):02d}:{int(S_sol[i]%60):02d}",
                    'Fin': f"{int(C_sol[i]//60):02d}:{int(C_sol[i]%60):02d}",
                    'Retraso': u_sol[i]
                }
                for i in range(n)
            ],
            'Ociosidad Total': O_total
        }

        soluciones.append(solucion)
        print(f"--- Instancia {inst_type} resuelta y almacenada ---\n")

    # Mostrar todas las soluciones al final
    print("\n================= RESULTADOS TOTALES =================\n")
    for solucion in soluciones:
        print(f"=== Instancia {solucion['Instancia']} ===")
        print(f"Status: {solucion['Status']}")
        print(f"Valor Objetivo: {solucion['Valor Objetivo']}\n")

        print("Asignaciones (cirugía -> quirófano):")
        for asignacion in solucion['Asignaciones']:
            print(f"  Cirugía {asignacion[0]} -> Quirófano {asignacion[1]}")
        print()

        print("Detalles de cada cirugía:")
        for detalle in solucion['Detalles']:
            print(f"  Cirugía {detalle['Cirugía']}: {detalle['Inicio']} - {detalle['Fin']}, Retraso={detalle['Retraso']}")
        print(f"\nOciosidad Total: {solucion['Ociosidad Total']}")
        print("-" * 60)
        print()

    print("=== Fin de todas las soluciones ===")

if __name__ == "__main__":
    main()
