# -*- coding: utf-8 -*-

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)

#   {"nombre": "CL", "duracion": (180, 270),  "prioridad": 2},   # Colecistectomía laparoscópica (TRIPLE DURACIÓN)
#   {"nombre": "AC", "duracion": (180, 360),  "prioridad": 1},   # Apendicectomía clásica (TRIPLE DURACIÓN)
#   {"nombre": "H",  "duracion": (180, 180),  "prioridad": 2},   # Hernioplastía (TRIPLE DURACIÓN)
#   {"nombre": "AL", "duracion": (180, 180),  "prioridad": 1},   # Apendicectomía laparoscópica (TRIPLE DURACIÓN)
#   {"nombre": "CC", "duracion": (180, 180),  "prioridad": 2},   # Colecistectomía clásica (TRIPLE DURACIÓN)
#   {"nombre": "Co", "duracion": (270, 540),  "prioridad": 2},   # Colectomía (TRIPLE DURACIÓN)
#   {"nombre": "T",  "duracion": (270, 360),  "prioridad": 2},   # Tiroidectomía-paratiroidectomía (TRIPLE DURACIÓN)
#   {"nombre": "AV", "duracion": (90, 180),   "prioridad": 3},   # Accesos vasculares (TRIPLE DURACIÓN)
#   {"nombre": "TVE","duracion": (270, 540),  "prioridad": 2},   # Toracotomía-VATS-esternotomía (TRIPLE DURACIÓN)
#   {"nombre": "CM", "duracion": (180, 360),  "prioridad": 2},   # Cirugía mamaria (TRIPLE DURACIÓN)

def generate_instance_data(instance_type):
    """
    Devuelve:
      - n, m: número de cirugías (n) y quirófanos (m)
      - p: lista con duraciones de cada cirugía (min)
      - w: lista con prioridades
      - d: lista con deadlines (en min desde medianoche)
      - procedure_names: nombres de las cirugías
      - init: hora de inicio (en min desde medianoche)
      - H: horizonte diario (min) para cada quirófano
    """

    if instance_type == 1:
        # Instancia 1
        # m=11 quirófanos
        # H=540 => 9h de jornada (para evitar grandes ociosidades)
        m = 11
        H = 540
        init = 7*60  # 7:00 AM
        procedures_data = [
            ("CL",  225, 2, init + 6*60),
            ("AC",  270, 1, init + 9*60),
            ("H",   180, 2, init + 9*60),
            ("AL",  180, 1, init + 6*60),
            ("CC",  180, 2, init + 12*60),
            ("AV",  135, 3, init + 6*60),
            ("TVE", 405, 2, init + 15*60),
            ("CM",  270, 2, init + 12*60),
            ("CL2", 225, 2, init + 9*60),
            ("AC2", 270, 1, init + 12*60),
            ("H2",  180, 2, init + 9*60),
            ("AL2", 180, 1, init + 6*60),
            ("CC2", 180, 2, init + 12*60),
            ("AV2", 135, 3, init + 9*60),
            ("TVE2",405,2, init + 15*60),
            ("CM2", 270,2, init + 12*60),
            ("CL3", 225, 2, init + 6*60),
            ("AC3", 270, 1, init + 9*60),
            ("H3",  180, 2, init + 9*60),
            ("AL3", 180, 1, init + 6*60),
            ("CC3", 180, 2, init + 12*60),
            ("AV3", 135, 3, init + 9*60),
        ]
        n = len(procedures_data)

    elif instance_type == 2:
        # Instancia 2
        # m=6 quirófanos
        # H=480 => 8h de jornada
        m = 6
        H = 660
        init = 7*60
        procedures_data = [
            ("CL",  225, 2, init + 6*60),
            ("CL2", 225, 2, init + 6*60),
            ("AC",  270, 1, init + 9*60),
            ("AC2", 270, 1, init + 9*60),
            ("H",   180, 2, init + 9*60),
            ("AL",  180, 1, init + 6*60),
            ("CC",  180, 2, init + 12*60),
            ("Co",  360, 2, init + 15*60),
            ("T",   315, 2, init + 12*60),
            ("AV",  135, 3, init + 6*60),
            ("TVE", 405, 2, init + 15*60),
            ("CM",  270, 2, init + 9*60),
            ("CL3", 225, 2, init + 6*60),
            ("AC3", 270, 1, init + 9*60),
        ]
        n = len(procedures_data)

    elif instance_type == 3:
        # Instancia 3
        # m=10, H=500 => 8.3h
        m = 10
        H = 500 #600
        init = 8*60
        procedures_data = [
            ("CL",  225, 2, init + 12*60),
            ("CL",  225, 2, init + 15*60),
            ("CL",  225, 2, init + 18*60),
            ("AC",  270, 1, init + 9*60),
            ("AC",  270, 1, init + 12*60),
            ("AL",  180, 1, init + 6*60),
            ("H",   180, 2, init + 12*60),
            ("H",   180, 2, init + 9*60),
            ("CC",  180, 2, init + 6*60),
            ("Co",  360, 2, init + 18*60),
            ("T",   315, 2, init + 15*60),
            ("AV",  135, 3, init + 9*60),
            ("TVE", 405, 2, init + 21*60),
            ("CM",  270, 2, init + 15*60),
            ("AC",  270, 1, init + 18*60),
        ]
        n = len(procedures_data)

    elif instance_type == 4:
        # Instancia 4
        # m=12, H=600 => 10h
        m = 12
        H = 600
        init = 8*60
        procedures_data = [
            ("CL",   225, 2, init + 6*60),
            ("AC",   270, 1, init + 9*60),
            ("H",    180, 2, init + 9*60),
            ("AL",   180, 1, init + 6*60),
            ("CC",   180, 2, init + 9*60),
            ("Co",   360, 2, init + 15*60),
            ("T",    315, 2, init + 12*60),
            ("AV",   135, 3, init + 6*60),
            ("TVE",  405, 2, init + 15*60),
            ("CM",   270, 2, init + 9*60),
            ("CL2",  225, 2, init + 6*60),
            ("AC2",  270, 1, init + 9*60),
            ("H2",   180, 2, init + 6*60),
            ("AL2",  180, 1, init + 6*60),
            ("CC2",  180, 2, init + 9*60),
            ("Co2",  360, 2, init + 12*60),
            ("T2",   315, 2, init + 12*60),
            ("AV2",  135, 3, init + 6*60),
            ("TVE2", 405, 2, init + 15*60),
            ("CM2",  270, 2, init + 9*60),
            ("CL3",  225, 2, init + 6*60),
            ("AC3",  270, 1, init + 9*60),
            ("H3",   180, 2, init + 6*60),
            ("AL3",  180, 1, init + 6*60),
        ]
        n = len(procedures_data)

    elif instance_type == 5:
        # Instancia 5
        # m=12, H=540 => 9h
        m = 12
        H = 540
        init = 9*60
        procedures_data = [
            ("CL",   225, 2, init + 6*60),
            ("CL2",  225, 2, init + 9*60),
            ("CL3",  225, 2, init + 6*60),
            ("AC",   270, 1, init + 6*60),
            ("AC2",  270, 1, init + 9*60),
            ("AC3",  270, 1, init + 6*60),
            ("AL",   180, 1, init + 6*60),
            ("AL2",  180, 1, init + 6*60),
            ("H",    180, 2, init + 9*60),
            ("H2",   180, 2, init + 9*60),
            ("CC",   180, 2, init + 9*60),
            ("CC2",  180, 2, init + 12*60),
            ("Co",   360, 2, init + 15*60),
            ("T",    315, 2, init + 12*60),
            ("T2",   315, 2, init + 12*60),
            ("AV",   135, 3, init + 6*60),
            ("TVE",  405, 2, init + 15*60),
            ("CM",   270, 2, init + 9*60),
            ("CM2",  270, 2, init + 12*60),
            ("CL4",  225, 2, init + 6*60),
            ("AC4",  270, 1, init + 9*60),
            ("H3",   180, 2, init + 6*60),
            ("AL3",  180, 1, init + 6*60),
            ("CC3",  180, 2, init + 9*60),
        ]
        n = len(procedures_data)

    elif instance_type == 6:
        # Instancia 6
        # m=16, H=500 => 8.3h
        m = 5
        H = 500 #420
        init = 7*60
        procedures_data = [
            ("CL",  225, 2, init + 15*60),
            ("AC",  270, 1, init + 9*60),
            ("AC",  270, 1, init + 12*60),
            ("AL",  180, 1, init + 6*60),
            ("H",   180, 2, init + 9*60),
            ("CC",  180, 2, init + 15*60),
            ("AV",  135, 3, init + 6*60),
            ("CM",  270, 2, init + 12*60),
        ]
        n = len(procedures_data)

    elif instance_type == 7:
        # Instancia 7
        # m=8, H=540 => 9h
        m = 8
        H = 540
        init = 6*60
        procedures_data = [
            ("CL1",225,2, init + 6*60),
            ("AC1",270,1, init + 6*60),
            ("H1",180,2, init + 6*60),
            ("AL1",180,1, init + 6*60),
            ("CC1",180,2, init + 9*60),
            ("AV1",135,3, init + 6*60),
            ("TVE1",405,2,init + 15*60),
            ("CM1",270,2, init + 9*60),

            ("CL2",225,2, init + 6*60),
            ("AC2",270,1, init + 9*60),
            ("H2",180,2, init + 6*60),
            ("AL2",180,1, init + 6*60),
            ("CC2",180,2, init + 9*60),
            ("AV2",135,3, init + 6*60),
            ("TVE2",405,2,init + 12*60),
            ("CM2",270,2, init + 9*60),
        ]
        n = len(procedures_data)

    elif instance_type == 8:
        # Instancia 8
        # m=8, H=480 => 9.3h
        m = 8
        H = 560 
        init = 9*60
        procedures_data = [
            ("CL1",225,2, init + 6*60),
            ("AC1",270,1, init + 6*60),
            ("AL1",180,1, init + 6*60),
            ("H1",180,2, init + 9*60),
            ("CC1",180,2, init + 9*60),
            ("T1",315,2, init + 12*60),
            ("AV1",135,3,init + 6*60),
            ("TVE1",405,2,init + 15*60),

            ("CM1",270,2, init + 9*60),
            ("CL2",225,2, init + 6*60),
            ("AC2",270,1, init + 9*60),
            ("AL2",180,1, init + 6*60),
            ("H2",180,2, init + 9*60),
            ("CC2",180,2, init + 12*60),
            ("T2",315,2, init + 12*60),
            ("AV2",135,3,init + 6*60),
        ]
        n = len(procedures_data)

    elif instance_type == 9:
        # Instancia 9
        # m=6, H=540 => 9h
        m = 6
        H = 600 #540
        init = 7*60
        procedures_data = [
            ("CL1",225,2, init + 6*60),
            ("CL2",225,2, init + 6*60),
            ("AC1",270,1, init + 9*60),
            ("AC2",270,1, init + 9*60),
            ("AL1",180,1, init + 6*60),
            ("AL2",180,1, init + 6*60),
            ("H1",180,2, init + 9*60),
            ("H2",180,2, init + 9*60),
            ("CC1",180,2, init + 9*60),
            ("T1",315,2, init + 12*60),
            ("Co1",360,2,init + 15*60),
            ("Co2",360,2,init + 12*60),
        ]
        n = len(procedures_data)

    elif instance_type == 10:
        # Instancia 10
        # m=6, H=600 => 10h
        m = 6
        H = 600
        init = 8*60
        procedures_data = [
            ("CL1",225,2, init + 6*60),
            ("CL2",225,2, init + 9*60),
            ("AC1",270,1, init + 6*60),
            ("AC2",270,1, init + 9*60),
            ("AL1",180,1, init + 6*60),
            ("H1",180,2, init + 6*60),
            ("CC1",180,2, init + 9*60),
            ("CC2",180,2, init + 9*60),
            ("T1",315,2, init + 12*60),
            ("TVE1",405,2,init + 15*60),
            ("AV1",135,3, init + 6*60),
            ("CM1",270,2, init + 9*60),
        ]
        n = len(procedures_data)

    else:
        raise ValueError("Instancia no definida. Use un entero entre 1 y 10.")

    # Extraemos p, w, d y nombres
    p = [r[1] for r in procedures_data]
    w = [r[2] for r in procedures_data]
    d = [r[3] for r in procedures_data]
    procedure_names = [r[0] for r in procedures_data]

    return n, m, p, w, d, procedure_names, init, H


def build_model(n, m, p, w, d, procedure_names, init, H,
                alpha=0.5, beta=1.0, gamma=0.5,
                bigM=10000):

    from pulp import LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger, lpSum

    prob = LpProblem("Programacion_Cirugias_Lineal", LpMinimize)

    S = range(n)
    O = range(m)

    x = LpVariable.dicts("x", (S, O), 0, 1, cat=LpInteger)
    z = LpVariable.dicts("z", (S, S, O), 0, 1, cat=LpInteger)
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    u   = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    O_total = LpVariable("OciosidadTotal", 0)

    # -------------------------------------------------------------------------
    # Función objetivo
    # -------------------------------------------------------------------------
    prob += (
        alpha * lpSum(w[i] * C_i[i] for i in S) + 
        beta  * O_total +
        gamma * lpSum(u[i] for i in S)
    ), "Obj"

    # -------------------------------------------------------------------------
    # Restricciones
    # -------------------------------------------------------------------------

    # (1) Cada cirugía a un quirófano
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1

    # (2) C_i = S_i + p_i
    for i in S:
        prob += C_i[i] == S_i[i] + p[i]

    # (3) Secuenciación disyuntiva
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

    # (4) No solapamiento
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += S_i[j] >= C_i[i] - bigM * (1 - z[i][j][o])

    # (5) Retraso
    for i in S:
        prob += u[i] >= C_i[i] - d[i]
        prob += u[i] >= 0

    # (6) Trabajo en quirófano o
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o]*p[i] for i in S)

    # (7) Ociosidad total
    prob += O_total == lpSum(H - w_oo[o] for o in O)

    # (8) No iniciar antes de init
    for i in S:
        prob += S_i[i] >= init

    bin_vars = [v for v in prob.variables() if v.cat in ("Integer", "Binary")]
    print(f"Número de variables binarias/enteras: {len(bin_vars)}")

    return prob, x, z, S_i, C_i, u, O_total


def solve_instance(instance_type, solver_path=None):
    """
    Construye y resuelve la instancia (1..10).
    Retorna la info necesaria: status, valor objetivo, soluciones, etc.
    """
    from pulp import LpStatus, value

    n, m, p, w, d, procedure_names, init, H = generate_instance_data(instance_type)
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d, procedure_names, init, H,
        alpha=0.5, beta=1.0, gamma=0.5, bigM=10000
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

    return (status, obj_value, x_sol, S_sol, C_sol, u_sol,
            O_total_sol, n, m, p, w, d, procedure_names, init, H)


def main():
    """
    Resuelve todas las instancias (1..10) en serie e imprime resultados.
    Ajustamos H para que la ociosidad sea más baja (en torno a <1000).
    """
    for inst_type in range(1, 11):
        (status, obj, x_sol, S_sol, C_sol, u_sol,
         O_total, n, m, p, w, d, procedure_names, init, H) = solve_instance(inst_type)

        print(f"\n=== Resultados - Instancia {inst_type} ===")
        print(f"Status: {status}")
        print(f"Valor Objetivo: {obj:.2f}")
        print(f"n={n}, m={m}, init={init}, H={H}\n")

        # Asignaciones
        asigs = [(i, o) for (i, o), val in x_sol.items() if val and val>0.9]
        print("Asignaciones (cirugía->quirófano):", asigs)

        print("\nDetalles de cada cirugía:")
        for i in range(n):
            ini = S_sol[i]
            fin = C_sol[i]
            ret = u_sol[i]
            ini_h = f"{int(ini//60):02d}:{int(ini%60):02d}"
            fin_h = f"{int(fin//60):02d}:{int(fin%60):02d}"
            dd_h  = f"{int(d[i]//60):02d}:{int(d[i]%60):02d}"
            print(f"  Cirugía {i} ({procedure_names[i]}):")
            print(f"    Duración={p[i]} min")
            print(f"    Inicio={ini_h}, Fin={fin_h}, Deadline={dd_h}, Retraso={ret:.2f}")

        print(f"\nOciosidad Total: {O_total:.2f}")
        print("====================================")


if __name__ == "__main__":
    main()

