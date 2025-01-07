# -*- coding: utf-8 -*-
"""
Código completo que usa SOLO las 10 instancias del informe
'Desafíos en la Asignación y Programación de Cirugías Electivas No GES
en Hospitales Públicos de Chile'.

Requisitos:
    pip install pulp pandas
Recomendado usar Python >= 3.10 con PuLP para el manejo correcto de variables enteras.
"""

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpContinuous, LpInteger,
    lpSum, LpStatus, value, COIN_CMD
)
import random
import pandas as pd

def get_hospital_instances_from_report():
    """
    Devuelve una lista de diccionarios, cada uno representando un hospital
    extraído del informe (10 hospitales).
    """
    hospital_data = [
        {
            "hospital": "Hospital Dr. Sótero del Río (Santiago)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 250,
            "n_quirofanos": 10,
            "duracion_min": (120, 240),  # Rango de duración
            "deadline": 600  # 10 horas en minutos
        },
        {
            "hospital": "Hospital Regional de Concepción (Concepción)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 300,
            "n_quirofanos": 12,
            "duracion_min": (90, 300),
            "deadline": 720  # 12 horas
        },
        {
            "hospital": "Hospital Gustavo Fricke (Viña del Mar)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 280,
            "n_quirofanos": 9,
            "duracion_min": (60, 180),
            "deadline": 960  # 16 horas
        },
        {
            "hospital": "Hospital Carlos Van Buren (Valparaíso)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 320,
            "n_quirofanos": 11,
            "duracion_min": (180, 360),
            "deadline": 480  # 8 horas
        },
        {
            "hospital": "Hospital Regional de Antofagasta (Antofagasta)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 200,
            "n_quirofanos": 8,
            "duracion_min": (120, 240),
            "deadline": 720  # 12 horas
        },
        {
            "hospital": "Hospital de La Serena (La Serena)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 150,
            "n_quirofanos": 6,
            "duracion_min": (60, 150),
            "deadline": 600  # 10 horas
        },
        {
            "hospital": "Hospital de Talca (Talca)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 180,
            "n_quirofanos": 7,
            "duracion_min": (90, 210),
            "deadline": 1440  # 24 horas
        },
        {
            "hospital": "Hospital de Chillán (Chillán)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 160,
            "n_quirofanos": 5,
            "duracion_min": (120, 300),
            "deadline": 540  # 9 horas
        },
        {
            "hospital": "Hospital de Puerto Montt (Puerto Montt)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 120,
            "n_quirofanos": 4,
            "duracion_min": (60, 240),
            "deadline": 600  # 10 horas
        },
        {
            "hospital": "Hospital de Castro (Chiloé)",
            "tipo": "Baja Complejidad",
            "n_cirugias_mes": 80,
            "n_quirofanos": 3,
            "duracion_min": (30, 120),
            "deadline": 720  # 12 horas
        }
    ]
    return hospital_data

def generate_procedure_selection():
    """
    Genera la selección de procedimientos basada en los porcentajes proporcionados.
    Retorna una lista de dicciones con nombre, rango de duración y prioridad.
    """
    # Definición de los procedimientos con sus rangos de duración y prioridades
    procedures = [
        {"nombre": "CL", "duracion": (60, 90), "prioridad": 2},    # Colecistectomía laparoscópica
        {"nombre": "AC", "duracion": (60, 120), "prioridad": 1},   # Apendicectomía clásica
        {"nombre": "H",  "duracion": (60, 60), "prioridad": 2},    # Hernioplastía
        {"nombre": "AL", "duracion": (60, 60), "prioridad": 1},    # Apendicectomía laparoscópica
        {"nombre": "CC", "duracion": (60, 60), "prioridad": 2},    # Colecistectomía clásica
        {"nombre": "Co", "duracion": (90, 180), "prioridad": 2},   # Colectomía
        {"nombre": "T",  "duracion": (90, 120), "prioridad": 2},   # Tiroidectomía-paratiroidectomía
        {"nombre": "AV", "duracion": (30, 60), "prioridad": 3},    # Accesos vasculares
        {"nombre": "TVE","duracion": (90, 180), "prioridad": 2},   # Toracotomía-VATS-esternotomía
        {"nombre": "CM", "duracion": (60, 120), "prioridad": 2}     # Cirugía mamaria
    ]
    return procedures

def generate_instance_data(instance_type, hospital_data, procedures, procedure_percentages):
    """
    Genera los datos de una instancia basada en el tipo de hospital.
    Utiliza la distribución porcentual de procedimientos con algo de ruido en duraciones.

    Args:
        instance_type (int): Número de instancia (1 a 10).
        hospital_data (list): Lista de diccionarios con datos de hospitales.
        procedures (list): Lista de diccionarios de procedimientos.
        procedure_percentages (dict): Diccionario con porcentajes de cada procedimiento.

    Returns:
        tuple: (n, m, p, w, d, procedure_names)
    """
    if instance_type < 1 or instance_type > 10:
        raise ValueError("Instancia no definida. Use un entero entre 1 y 10.")

    # Obtener datos del hospital
    hospital_info = hospital_data[instance_type - 1]  # Índice 0-9

    m = hospital_info["n_quirofanos"]  # Número de quirófanos
    n = 3 * m  # 3 cirugías por quirófano

    # Crear lista de nombres y pesos para selección ponderada
    nombres = [proc["nombre"] for proc in procedures]
    pesos = [procedure_percentages[proc["nombre"]] for proc in procedures]

    # Seleccionar n procedimientos basados en las probabilidades
    selected_procedures = random.choices(
        procedures,
        weights=pesos,
        k=n
    )

    # Asignar duraciones con ruido dentro del rango
    p = [random.randint(proc["duracion"][0], proc["duracion"][1]) if proc["duracion"][0] != proc["duracion"][1] else proc["duracion"][0] for proc in selected_procedures]

    # Asignar prioridades
    w = [proc["prioridad"] for proc in selected_procedures]

    # Asignar nombres de procedimientos
    procedure_names = [proc["nombre"] for proc in selected_procedures]

    # Asignar deadlines según la instancia
    deadline = hospital_info["deadline"]
    d = [deadline] * n

    return n, m, p, w, d, procedure_names

def build_model(n, m, p, w, d,
               alpha=0.5, beta=1.0, gamma=0.5,
               bigM=10000):
    """
    Construye el modelo MIP con una formulación de secuenciación (disyuntiva lineal).
    """

    # Definimos el problema
    prob = LpProblem("Programacion_Cirugias_Lineal", LpMinimize)

    S = range(n)  # Conjunto de cirugías
    O = range(m)  # Conjunto de quirófanos

    # Variables binarias: x[i][o], z[i][j][o]
    x = LpVariable.dicts("x", (S, O), 0, 1, cat=LpBinary)
    z = LpVariable.dicts("z", (S, S, O), 0, 1, cat=LpBinary)

    # Variables continuas de tiempo
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    u   = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    # Ociosidad
    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    O_total = LpVariable("OciosidadTotal", 0, None, LpContinuous)

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
    ), "Objetivo"

    # -------------------------------------------------------------------------
    # Restricciones
    # -------------------------------------------------------------------------

    # (1) Asignación única de cada cirugía a exactamente 1 quirófano
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1, f"AsigUnica_{i}"

    # (2) Relación entre tiempos Start y Completion
    for i in S:
        prob += C_i[i] == S_i[i] + p[i], f"TiempoFin_{i}"

    # (3) Disyuntiva lineal para secuenciación en cada quirófano
    for o in O:
        for i in S:
            for j in S:
                if i < j:
                    # i precede a j
                    prob += S_i[j] >= C_i[i] - bigM * (1 - z[i][j][o]), f"NoSolape_{i}_{j}_Q{o}"
                    # j precede a i
                    prob += S_i[i] >= C_i[j] - bigM * (1 - z[j][i][o]), f"NoSolape_{j}_{i}_Q{o}"
                    # Solo una precedencia puede ser activa
                    prob += z[i][j][o] + z[j][i][o] <= 1, f"Precedence_{i}_{j}_Q{o}"
    
    # (4) Ociosidad total: (H - tiempo_usado) en cada quirófano
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o] * p[i] for i in S), f"TrabajoQ_{o}"

    prob += O_total == lpSum(H - w_oo[o] for o in O), "SumaOciosidad"

    return prob, x, z, S_i, C_i, u, O_total

def solve_instance(instance_type, solver_path=None):
    """
    Construye y resuelve una instancia dada por instance_type (1..10).
    Retorna la información relevante: status, valor objetivo, soluciones, etc.
    """
    # Obtener datos de hospitales
    hospital_data = get_hospital_instances_from_report()

    # Definir procedimiento y porcentajes
    procedures = generate_procedure_selection()
    procedure_percentages = {
        "CL": 24,
        "AC": 19,
        "H":  9,
        "AL": 7,
        "CC": 5,
        "Co": 2,
        "T":  2,
        "AV": 2,
        "TVE":1,
        "CM":1
    }

    # Generar datos de la instancia
    n, m, p, w, d, procedure_names = generate_instance_data(
        instance_type, hospital_data, procedures, procedure_percentages
    )

    # Construir modelo
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d,
        alpha=0.5, beta=1.0, gamma=0.5, bigM=10000
    )

    # Configurar el solver (CBC por defecto)
    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
    else:
        solver = COIN_CMD(msg=True, timeLimit=120)

    # Resolver el modelo
    prob.solve(solver)

    # Obtener estado y valor objetivo
    status = LpStatus[prob.status]
    obj_value = value(prob.objective)

    # Extraer soluciones
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

def build_model(n, m, p, w, d,
               alpha=0.5, beta=1.0, gamma=0.5,
               bigM=10000):
    """
    Construye el modelo MIP con una formulación de secuenciación (disyuntiva lineal).
    """

    # Definimos el problema
    prob = LpProblem("Programacion_Cirugias_Lineal", LpMinimize)

    S = range(n)  # Conjunto de cirugías
    O = range(m)  # Conjunto de quirófanos

    # Variables binarias: x[i][o], z[i][j][o]
    x = LpVariable.dicts("x", (S, O), 0, 1, cat=LpBinary)
    z = LpVariable.dicts("z", (S, S, O), 0, 1, cat=LpBinary)

    # Variables continuas de tiempo
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    u   = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    # Ociosidad
    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    O_total = LpVariable("OciosidadTotal", 0, None, LpContinuous)

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
    ), "Objetivo"

    # -------------------------------------------------------------------------
    # Restricciones
    # -------------------------------------------------------------------------

    # (1) Asignación única de cada cirugía a exactamente 1 quirófano
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1, f"AsigUnica_{i}"

    # (2) Relación entre tiempos Start y Completion
    for i in S:
        prob += C_i[i] == S_i[i] + p[i], f"TiempoFin_{i}"

    # (3) Disyuntiva lineal para secuenciación en cada quirófano
    for o in O:
        for i in S:
            for j in S:
                if i < j:
                    # i precede a j
                    prob += S_i[j] >= C_i[i] - bigM * (1 - z[i][j][o]), f"NoSolape_{i}_{j}_Q{o}"
                    # j precede a i
                    prob += S_i[i] >= C_i[j] - bigM * (1 - z[j][i][o]), f"NoSolape_{j}_{i}_Q{o}"
                    # Solo una precedencia puede ser activa
                    prob += z[i][j][o] + z[j][i][o] <= 1, f"Precedence_{i}_{j}_Q{o}"

    # (4) Trabajo en quirófano o
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o] * p[i] for i in S), f"TrabajoQ_{o}"

    # (5) Ociosidad total: (H - tiempo_usado) en cada quirófano
    prob += O_total == lpSum(H - w_oo[o] for o in O), "SumaOciosidad"

    return prob, x, z, S_i, C_i, u, O_total

def solve_instance(instance_type, solver_path=None):
    """
    Construye y resuelve una instancia dada por instance_type (1..10).
    Retorna la información relevante: status, valor objetivo, soluciones, etc.
    """
    # Obtener datos de hospitales
    hospital_data = get_hospital_instances_from_report()

    # Definir procedimiento y porcentajes
    procedures = generate_procedure_selection()
    procedure_percentages = {
        "CL": 24,
        "AC": 19,
        "H":  9,
        "AL": 7,
        "CC": 5,
        "Co": 2,
        "T":  2,
        "AV": 2,
        "TVE":1,
        "CM":1
    }

    # Generar datos de la instancia
    n, m, p, w, d, procedure_names = generate_instance_data(
        instance_type, hospital_data, procedures, procedure_percentages
    )

    # Construir modelo
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d,
        alpha=0.5, beta=1.0, gamma=0.5, bigM=10000
    )

    # Configurar el solver (CBC por defecto)
    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
    else:
        solver = COIN_CMD(msg=True, timeLimit=120)

    # Resolver el modelo
    prob.solve(solver)

    # Obtener estado y valor objetivo
    status = LpStatus[prob.status]
    obj_value = value(prob.objective)

    # Extraer soluciones
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
