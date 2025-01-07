# -*- coding: utf-8 -*-

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)

def generate_instance_data(instance_type):
    """
    Devuelve (n, m, p, w, d, procedure_names) para 10 instancias diferentes,
    más la estructura del ejemplo de tabla de procedimientos:
    
    Procedimiento                         | Duración (min)   | Prioridad
    -------------------------------------------------------------------
    Colecistectomía laparoscópica (CL)    | 60-90            | 2
    Apendicectomía clásica (AC)           | 60-120           | 1
    Hernioplastía (H)                     | ~60              | 2
    Apendicectomía laparoscópica (AL)     | ~60              | 1
    Colecistectomía clásica (CC)          | ~60              | 2
    Colectomía (Co)                       | >90              | 2
    Tiroidectomía-paratiroidectomía (T)   | 90-120           | 2
    Accesos vasculares (AV)               | 30-60            | 3
    Toracotomía-VATS-esternotomía (TVE)   | 90-180           | 2
    Cirugía mamaria (CM)                  | 60-120           | 2
    """

    # -------------------------------------------------------------------------
    # Tabla base (procedimientos) para uso genérico: (nombre, duracion, prioridad)
    # -------------------------------------------------------------------------
    # NOTA: Puedes variar los valores fijos según tu criterio (ejemplo, usar 75 en CL).
    full_table = [
        ("CL",  75, 2),   # Colecistectomía laparoscópica
        ("AC",  90, 1),   # Apendicectomía clásica
        ("H",   60, 2),   # Hernioplastía
        ("AL",  60, 1),   # Apendicectomía laparoscópica
        ("CC",  60, 2),   # Colecistectomía clásica
        ("Co", 120, 2),   # Colectomía
        ("T",  105, 2),   # Tiroidectomía-paratiroidectomía
        ("AV",  45, 3),   # Accesos vasculares
        ("TVE",135, 2),   # Toracotomía-VATS-esternotomía
        ("CM",  90, 2),   # Cirugía mamaria
    ]
    # Para generar combinaciones, iremos tomando sub-conjuntos o repeticiones
    # según lo requiera cada instancia.

    # -------------------------------------------------------------------------
    # Instancia 1
    # -------------------------------------------------------------------------
    if instance_type == 1:
        # Ejemplo: n=8, m=1
        # Distribuimos manualmente 8 cirugías tomando algunas de la tabla:
        procedures_data = [
            ("CL",  75, 2),
            ("AC",  90, 1),
            ("H",   60, 2),
            ("AL",  60, 1),
            ("CC",  60, 2),
            ("AV",  45, 3),
            ("TVE",135, 2),
            ("CM",  90, 2),
        ]
        n = len(procedures_data)
        m = 1  # 1 quirófano
        # Deadline genérico (ej. 600 min = 10h)
        d = [600]*n

    # -------------------------------------------------------------------------
    # Instancia 2
    # -------------------------------------------------------------------------
    elif instance_type == 2:
        # Ejemplo: n=12, m=2
        # Hacemos una pequeña aproximación de 12 cirugías a partir de la tabla.
        procedures_data = [
            ("CL",  75, 2),
            ("CL",  75, 2),  # repetimos
            ("AC",  90, 1),
            ("AC",  90, 1),
            ("H",   60, 2),
            ("AL",  60, 1),
            ("CC",  60, 2),
            ("Co", 120, 2),
            ("T",  105, 2),
            ("AV",  45, 3),
            ("TVE",135, 2),
            ("CM",  90, 2),
        ]
        n = len(procedures_data)
        m = 2
        d = [720]*n  # 12h

    # -------------------------------------------------------------------------
    # Instancia 3
    # -------------------------------------------------------------------------
    elif instance_type == 3:
        # Ejemplo: n=15, m=3
        # Sumamos 15 cirugías.
        procedures_data = [
            ("CL",  75, 2),
            ("CL",  75, 2),
            ("CL",  75, 2),
            ("AC",  90, 1),
            ("AC",  90, 1),
            ("AL",  60, 1),
            ("H",   60, 2),
            ("H",   60, 2),
            ("CC",  60, 2),
            ("Co", 120, 2),
            ("T",  105, 2),
            ("AV",  45, 3),
            ("TVE",135, 2),
            ("CM",  90, 2),
            ("AC",  90, 1),
        ]
        n = len(procedures_data)
        m = 3
        d = [960]*n  # 16h

    # -------------------------------------------------------------------------
    # Instancia 4
    # -------------------------------------------------------------------------
    elif instance_type == 4:
        # Ejemplo: n=10, m=2
        # Tomamos 10, con otras combinaciones.
        procedures_data = [
            ("CL",  75, 2),
            ("AC",  90, 1),
            ("H",   60, 2),
            ("AL",  60, 1),
            ("CC",  60, 2),
            ("Co", 120, 2),
            ("T",  105, 2),
            ("TVE",135, 2),
            ("AV",  45, 3),
            ("CM",  90, 2),
        ]
        n = len(procedures_data)
        m = 2
        d = [480]*n  # 8h

    # -------------------------------------------------------------------------
    # Instancia 5
    # -------------------------------------------------------------------------
    elif instance_type == 5:
        # Ejemplo: n=20, m=3
        # Para un escenario más grande. Repetimos varios procedimientos.
        procedures_data = [
            ("CL",  75, 2),
            ("CL",  75, 2),
            ("CL",  75, 2),
            ("AC",  90, 1),
            ("AC",  90, 1),
            ("AC",  90, 1),
            ("AL",  60, 1),
            ("AL",  60, 1),
            ("H",   60, 2),
            ("H",   60, 2),
            ("CC",  60, 2),
            ("CC",  60, 2),
            ("Co", 120, 2),
            ("T",  105, 2),
            ("T",  105, 2),
            ("AV",  45, 3),
            ("TVE",135, 2),
            ("CM",  90, 2),
            ("CM",  90, 2),
            ("CL",  75, 2),
        ]
        n = len(procedures_data)
        m = 3
        d = [720]*n  # 12h

    # -------------------------------------------------------------------------
    # Instancia 6
    # -------------------------------------------------------------------------
    elif instance_type == 6:
        # Ejemplo: n=8, m=2
        # Otra instancia pequeña (usando la misma "id 6" del ejemplo original).
        procedures_data = [
            ("CL",  75, 2),
            ("AC",  90, 1),
            ("AC",  90, 1),
            ("AL",  60, 1),
            ("H",   60, 2),
            ("CC",  60, 2),
            ("AV",  45, 3),
            ("CM",  90, 2),
        ]
        n = len(procedures_data)
        m = 2
        d = [600]*n  # 10h

    # -------------------------------------------------------------------------
    # Instancia 7
    # -------------------------------------------------------------------------
    elif instance_type == 7:
        # Ejemplo: n=25, m=4
        # Un caso grande, repitiendo muchos procedimientos.
        procedures_data = [
            ("CL",  75, 2),  ("CL",  75, 2),  ("CL",  75, 2),  ("CL",  75, 2),
            ("AC",  90, 1),  ("AC",  90, 1),  ("AC",  90, 1),  ("AC",  90, 1),
            ("AL",  60, 1),  ("AL",  60, 1),  ("H",   60, 2),  ("H",   60, 2),
            ("CC",  60, 2),  ("CC",  60, 2),  ("CC",  60, 2),
            ("Co", 120, 2),  ("Co", 120, 2),
            ("T",  105, 2),  ("T",  105, 2),
            ("AV",  45, 3),  ("TVE",135, 2),
            ("CM",  90, 2),  ("CM",  90, 2),
            ("CL",  75, 2),  ("AC",  90, 1),
        ]
        n = len(procedures_data)
        m = 4
        d = [1440]*n  # 24h

    # -------------------------------------------------------------------------
    # Instancia 8
    # -------------------------------------------------------------------------
    elif instance_type == 8:
        # Ejemplo: n=9, m=1
        # Instancia muy pequeña con 1 quirófano.
        procedures_data = [
            ("CL",  75, 2),
            ("AC",  90, 1),
            ("AL",  60, 1),
            ("H",   60, 2),
            ("CC",  60, 2),
            ("T",  105,2),
            ("AV",  45, 3),
            ("TVE",135,2),
            ("CM",  90, 2),
        ]
        n = len(procedures_data)
        m = 1
        d = [540]*n  # 9h

    # -------------------------------------------------------------------------
    # Instancia 9
    # -------------------------------------------------------------------------
    elif instance_type == 9:
        # Ejemplo: n=16, m=2
        procedures_data = [
            ("CL",  75, 2),  ("CL",  75, 2),
            ("AC",  90, 1),  ("AC",  90, 1),
            ("AL",  60, 1),  ("AL",  60, 1),
            ("H",   60, 2),  ("H",   60, 2),
            ("CC",  60, 2),  ("T",  105,2),
            ("Co", 120, 2),  ("Co", 120,2),
            ("AV",  45, 3),  ("CM",  90, 2),
            ("TVE",135, 2),  ("CL",  75, 2),
        ]
        n = len(procedures_data)
        m = 2
        d = [600]*n  # 10h

    # -------------------------------------------------------------------------
    # Instancia 10
    # -------------------------------------------------------------------------
    elif instance_type == 10:
        # Ejemplo: n=12, m=3
        procedures_data = [
            ("CL",  75, 2),  ("CL",  75, 2),
            ("AC",  90, 1),  ("AC",  90, 1),
            ("AL",  60, 1),  ("H",   60, 2),
            ("CC",  60, 2),  ("CC",  60, 2),
            ("T",  105,2),   ("TVE",135,2),
            ("AV",  45, 3),  ("CM",  90, 2),
        ]
        n = len(procedures_data)
        m = 3
        d = [720]*n  # 12h

    else:
        raise ValueError("Instancia no definida. Use un entero entre 1 y 10.")

    # Extraemos p, w, nombres
    p = [proc[1] for proc in procedures_data]
    w = [proc[2] for proc in procedures_data]
    procedure_names = [proc[0] for proc in procedures_data]

    return n, m, p, w, d, procedure_names


def build_model(n, m, p, w, d,
                alpha=0.5, beta=1.0, gamma=0.5,
                bigM=10000):
    """
    Construye el modelo MIP con una formulación de secuenciación (disyuntiva lineal).
    """

    # Definimos el problema
    prob = LpProblem("Programacion_Cirugias_Lineal", LpMinimize)

    S = range(n)  # conjunto de cirugías
    O = range(m)  # conjunto de quirófanos

    # Variables binarias: x[i][o], z[i][j][o]
    x = LpVariable.dicts("x", (S, O), 0, 1, cat=LpInteger)
    z = LpVariable.dicts("z", (S, S, O), 0, 1, cat=LpInteger)

    # Variables continuas de tiempo
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    u   = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    # Ociosidad
    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    O_total = LpVariable("OciosidadTotal", 0)

    # Estimamos un "horizonte" H = suma duraciones + un margen
    H = sum(p) + 100

    # -------------------------------------------------------------------------
    # Función objetivo
    # -------------------------------------------------------------------------
    # Minimizar: (1) sum w_i * C_i + (2) sum de retrasos + (3) ociosidad total
    prob += (
        alpha * lpSum(w[i] * C_i[i] for i in S) +
        gamma * lpSum(u[i] for i in S) +
        beta  * O_total
    ), "Obj"

    # -------------------------------------------------------------------------
    # Restricciones
    # -------------------------------------------------------------------------

    # (1) Asignación única de cada cirugía a exactamente 1 quirófano
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1

    # (2) Relación entre tiempos Start y Completion
    for i in S:
        prob += C_i[i] == S_i[i] + p[i]

    # (3) Disyuntiva lineal para secuenciación en cada quirófano
    for i in S:
        for j in S:
            if i < j:
                for o in O:
                    # i precede a j, o j precede a i
                    prob += z[i][j][o] + z[j][i][o] <= 1
                    # No puedes preceder si al menos uno no está en el quirófano o
                    prob += z[i][j][o] <= x[i][o]
                    prob += z[i][j][o] <= x[j][o]
                    prob += z[j][i][o] <= x[i][o]
                    prob += z[j][i][o] <= x[j][o]
                    # Al menos una precedencia si los dos están en quirófano o
                    prob += z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] - 1

    # (4) No solapamiento: si i precede a j en o, el start de j >= completion de i
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += S_i[j] >= C_i[i] - bigM * (1 - z[i][j][o])

    # (5) Retraso respecto al deadline: u[i] >= C_i[i] - d[i]
    for i in S:
        prob += u[i] >= C_i[i] - d[i]
        prob += u[i] >= 0

    # (6) Trabajo en quirófano o
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o] * p[i] for i in S)

    # (7) Ociosidad total: (H - tiempo_usado) en cada quirófano
    prob += O_total == lpSum(H - w_oo[o] for o in O)

    # Cantidad de variables binarias
    bin_vars = [v for v in prob.variables() if v.cat in ("Integer", "Binary")]
    print(f"Número de variables enteras/binarias en el modelo: {len(bin_vars)}")

    return prob, x, z, S_i, C_i, u, O_total


def solve_instance(instance_type, solver_path=None):
    """
    Construye y resuelve una instancia dada por instance_type (1..10).
    Retorna la información relevante: status, valor objetivo, soluciones, etc.
    """
    n, m, p, w, d, procedure_names = generate_instance_data(instance_type)
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d,
        alpha=0.5, beta=1.0, gamma=0.5, bigM=10000
    )

    # Configuramos el solver (CBC por defecto)
    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
    else:
        solver = COIN_CMD(msg=True, timeLimit=120)

    prob.solve(solver)

    status = LpStatus[prob.status]
    obj_value = value(prob.objective)

    # Extraemos soluciones
    x_sol = {(i, o): value(x[i][o]) for i in range(n) for o in range(m)}
    S_sol = {i: value(S_i[i]) for i in range(n)}
    C_sol = {i: value(C_i[i]) for i in range(n)}
    u_sol = {i: value(u[i]) for i in range(n)}
    O_total_sol = value(O_total)

    return (status, obj_value, x_sol, S_sol, C_sol, u_sol,
            O_total_sol, n, m, p, w, d, procedure_names)


def main():
    """
    Resuelve las 10 instancias definidas en la función generate_instance_data.
    """
    solver_path = None
    results = {}

    # Lista de 1 a 10
    instancias = list(range(1, 11))

    for inst_type in instancias:
        print(f"--- Resolviendo instancia {inst_type} ---")
        (status, obj, x_sol, S_sol, C_sol, u_sol, O_total, 
         n, m, p, w, d, procedure_names) = solve_instance(
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
            "d": d,
            "procedure_names": procedure_names
        }
        print(f"--- Fin de instancia {inst_type} ---\n")

    # Reporte final
    print("==== RESUMEN DE LAS 10 INSTANCIAS ====\n")
    for inst_type in sorted(results.keys()):
        r = results[inst_type]
        print(f"=== Instancia {inst_type} ===")
        print("Status:", r["status"])
        print("Valor Objetivo:", r["obj"])
        asigs = [(i, o) for (i, o), val in r["x_sol"].items() if val and val > 0.9]
        print("\nAsignaciones (cirugía->quirófano):", asigs)

        print("\nDetalles de cada cirugía:")
        for i in range(r["n"]):
            ini = r["S_sol"][i]
            fin = r["C_sol"][i]
            ret = r["u_sol"][i]
            # Convertimos a formato Horas:Min
            ini_h = f"{int(ini // 60):02d}:{int(ini % 60):02d}"
            fin_h = f"{int(fin // 60):02d}:{int(fin % 60):02d}"
            procedure_name = r["procedure_names"][i]
            print(f"  Cirugía {i} ({procedure_name}): {ini_h}-{fin_h}, Retraso={ret:.2f}")

        print("\nOciosidad Total:", r["O_total"])
        print("------------------------------------\n")


if __name__ == "__main__":
    main()
