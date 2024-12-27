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
            "cirugias_ejemplo": [
                "Colecistectomía", "Herniorrafia Inguinal", "Amigdalectomía",
                "Cirugía de Cataratas", "Reemplazo de Cadera"
            ],
            "duracion_min": "120 - 240",
            "peso_prioridad": "Según lista de espera y gravedad",
            "deadline": "Variable",
            "desafios": [
                "Alta demanda",
                "Lista de espera extensa",
                "Falta de camas"
            ]
        },
        {
            "hospital": "Hospital Regional de Concepción (Concepción)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 300,
            "n_quirofanos": 12,
            "cirugias_ejemplo": [
                "Artroscopía de Rodilla", "Cirugía de Cataratas", "Histerectomía",
                "Bypass Gástrico", "Craniectomía"
            ],
            "duracion_min": "90 - 300",
            "peso_prioridad": "Según lista de espera y gravedad",
            "deadline": "Variable",
            "desafios": [
                "Falta de personal especializado",
                "Disponibilidad de camas",
                "Coordinación entre servicios"
            ]
        },
        {
            "hospital": "Hospital Gustavo Fricke (Viña del Mar)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 280,
            "n_quirofanos": 9,
            "cirugias_ejemplo": [
                "Cirugía de Varices", "Safenectomía", "Septoplastia",
                "Cirugía de Reflujo Gastroesofágico", "Cirugía de la Mano"
            ],
            "duracion_min": "60 - 180",
            "peso_prioridad": "Según lista de espera",
            "deadline": "Variable",
            "desafios": [
                "Equipamiento médico con fallas",
                "Retrasos en la entrega de insumos",
                "Sistema de información deficiente"
            ]
        },
        {
            "hospital": "Hospital Carlos Van Buren (Valparaíso)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 320,
            "n_quirofanos": 11,
            "cirugias_ejemplo": [
                "Mastectomía", "Cirugía de Hernia Discal", "Prostatectomía",
                "Cirugía de Tiroides", "Nefrectomía"
            ],
            "duracion_min": "180 - 360",
            "peso_prioridad": "Según lista de espera y comorbilidades",
            "deadline": "Variable",
            "desafios": [
                "Coordinación entre servicios",
                "Sistema de información obsoleto",
                "Falta de personal de apoyo"
            ]
        },
        {
            "hospital": "Hospital Regional de Antofagasta (Antofagasta)",
            "tipo": "Alta Complejidad",
            "n_cirugias_mes": 200,
            "n_quirofanos": 8,
            "cirugias_ejemplo": [
                "Cirugía de Vesícula", "Reparación de Manguito Rotador",
                "Cirugía de Tiroides", "Cirugía de Colon", "Cirugía Plástica Reconstructiva"
            ],
            "duracion_min": "120 - 240",
            "peso_prioridad": "Según lista de espera y riesgo quirúrgico",
            "deadline": "Variable",
            "desafios": [
                "Centralización de recursos en la capital regional",
                "Dificultad para atraer especialistas"
            ]
        },
        {
            "hospital": "Hospital de La Serena (La Serena)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 150,
            "n_quirofanos": 6,
            "cirugias_ejemplo": [
                "Cirugía de Fimosis", "Extracción de Lipomas", "Cirugía de Juanetes",
                "Herniorrafia Umbilical", "Cirugía de Quistes Ováricos"
            ],
            "duracion_min": "60 - 150",
            "peso_prioridad": "Según lista de espera",
            "deadline": "Variable",
            "desafios": [
                "Dificultad para atraer/retener especialistas",
                "Infraestructura limitada"
            ]
        },
        {
            "hospital": "Hospital de Talca (Talca)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 180,
            "n_quirofanos": 7,
            "cirugias_ejemplo": [
                "Cirugía de Ovario", "Vasectomía", "Blefaroplastia",
                "Cirugía de Hemorroides", "Cirugía de la Vesícula Biliar"
            ],
            "duracion_min": "90 - 210",
            "peso_prioridad": "Según lista de espera",
            "deadline": "Variable",
            "desafios": [
                "Infraestructura limitada",
                "Falta de camas",
                "Escasa inversión en tecnología"
            ]
        },
        {
            "hospital": "Hospital de Chillán (Chillán)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 160,
            "n_quirofanos": 5,
            "cirugias_ejemplo": [
                "Cirugía de Próstata", "Cirugía de Hernias", "Cirugía de Mano",
                "Cirugía de Rodilla", "Cirugía de Tobillo"
            ],
            "duracion_min": "120 - 300",
            "peso_prioridad": "Según lista de espera y complejidad",
            "deadline": "Variable",
            "desafios": [
                "Escasa inversión en tecnología médica",
                "Falta de capacitación para el personal"
            ]
        },
        {
            "hospital": "Hospital de Puerto Montt (Puerto Montt)",
            "tipo": "Mediana Complejidad",
            "n_cirugias_mes": 120,
            "n_quirofanos": 4,
            "cirugias_ejemplo": [
                "Cirugía de Amígdalas", "Cirugía de Adenoides",
                "Implantes Dentales", "Cirugía de Cataratas", "Meniscectomía"
            ],
            "duracion_min": "60 - 240",
            "peso_prioridad": "Según lista de espera",
            "deadline": "Variable",
            "desafios": [
                "Condiciones climáticas adversas",
                "Aislamiento geográfico"
            ]
        },
        {
            "hospital": "Hospital de Castro (Chiloé)",
            "tipo": "Baja Complejidad",
            "n_cirugias_mes": 80,
            "n_quirofanos": 3,
            "cirugias_ejemplo": [
                "Cirugía Menor", "Biopsias", "Retiro de puntos",
                "Drenado de Abscesos", "Extracción de Uñas"
            ],
            "duracion_min": "30 - 120",
            "peso_prioridad": "Según urgencia",
            "deadline": "Variable",
            "desafios": [
                "Aislamiento geográfico",
                "Falta de especialistas",
                "Recursos limitados"
            ]
        }
    ]
    return hospital_data


def build_model_lineal(n, m, p, w, d,
                       alpha=0.5, beta=1.0, gamma=0.5, bigM=1080):
    """
    Construye un modelo de Programación Entera Mixta para la asignación de cirugías
    (x[i][o], z[i][j][o], S_i, C_i, u_i), usando disyuntiva lineal.

    Variables:
        x[i][o] en {0,1}  - asignación de cirugía i a quirófano o
        z[i][j][o] en {0,1} - precedencia si ambas están asignadas al mismo quirófano
        S_i, C_i en continuo
        u_i en continuo (retraso)

    bigM ~ 1080 asumiendo ventana 06:00-24:00.
    """
    prob = LpProblem("Prog_Cirugias_Lineal", LpMinimize)

    START_DAY = 360   # 06:00
    END_DAY = 1440    # 24:00

    S = range(n)
    O = range(m)

    # Definimos variables de asignación y precedencia
    x = LpVariable.dicts("x", (S, O), 0, 1, cat=LpInteger)
    z = LpVariable.dicts("z", (S, S, O), 0, 1, cat=LpInteger)

    # Tiempos
    S_i = LpVariable.dicts("Start", S, lowBound=START_DAY, upBound=END_DAY, cat=LpContinuous)
    C_i = LpVariable.dicts("Completion", S, lowBound=START_DAY, upBound=END_DAY, cat=LpContinuous)
    u = LpVariable.dicts("Delay", S, lowBound=0, cat=LpContinuous)

    # Ociosidad
    w_oo = LpVariable.dicts("Work_O", O, lowBound=0, cat=LpContinuous)
    O_total = LpVariable("OciosidadTotal", lowBound=0, cat=LpContinuous)

    # H para calcular ociosidad
    H = sum(p) + 100

    # Función objetivo
    prob += (
        alpha * lpSum(w[i]*C_i[i] for i in S) +
        gamma * lpSum(u[i] for i in S) +
        beta * O_total
    ), "FuncionObjetivo"

    # Restricciones

    # 1) Asignación única
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1, f"AsigUnica_{i}"

    # 2) C_i = S_i + p_i
    for i in S:
        prob += C_i[i] == S_i[i] + p[i], f"TiempoFin_{i}"

    # 3) Disyuntiva lineal en vez de multiplicar x[i][o]*x[j][o]
    for i in S:
        for j in S:
            if i < j:
                for o in O:
                    # No pueden ser 1 ambas z's
                    prob += z[i][j][o] + z[j][i][o] <= 1, f"Disy_leq1_{i}_{j}_{o}"
                    prob += z[i][j][o] <= x[i][o], f"z_ij_leq_xi_{i}_{j}_{o}"
                    prob += z[i][j][o] <= x[j][o], f"z_ij_leq_xj_{i}_{j}_{o}"
                    prob += z[j][i][o] <= x[i][o], f"z_ji_leq_xi_{i}_{j}_{o}"
                    prob += z[j][i][o] <= x[j][o], f"z_ji_leq_xj_{i}_{j}_{o}"
                    prob += z[i][j][o] + z[j][i][o] >= x[i][o] + x[j][o] - 1, f"Disy_min_{i}_{j}_{o}"

    # 4) No solapamiento: si z[i][j][o] = 1 => S_j >= C_i
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += (
                        S_i[j] >= C_i[i] - bigM*(1 - z[i][j][o]),
                        f"NoSolape_{i}_{j}_{o}"
                    )

    # 5) Retraso
    for i in S:
        prob += u[i] >= C_i[i] - d[i], f"RetrasoPos_{i}"
        prob += u[i] >= 0, f"RetrasoNoNeg_{i}"

    # 6) Trabajo de quirófano
    for o in O:
        prob += w_oo[o] == lpSum(x[i][o]*p[i] for i in S), f"TrabajoQ_{o}"

    # 7) Ociosidad total
    prob += O_total == lpSum(H - w_oo[o] for o in O), "SumaOciosidad"

    return prob, x, z, S_i, C_i, u, O_total


def solve_instance(n, m, p, w, d,
                   alpha=0.5, beta=1.0, gamma=0.5,
                   bigM=1080, solver_path=None, timeLimit=60):
    """
    Construye el modelo con disyuntiva lineal y lo resuelve.
    Retorna un dict con los resultados (Status, Obj, Asignaciones, etc.)
    """
    prob, x, z, S_i, C_i, u, O_total = build_model_lineal(
        n, m, p, w, d,
        alpha=alpha, beta=beta, gamma=gamma, bigM=bigM
    )

    if solver_path:
        solver = COIN_CMD(path=solver_path, msg=True, timeLimit=timeLimit)
    else:
        solver = COIN_CMD(msg=True, timeLimit=timeLimit)

    prob.solve(solver)

    status = LpStatus[prob.status]
    obj_value = value(prob.objective)
    x_sol = {(i,o): value(x[i][o]) for i in range(n) for o in range(m)}
    S_sol = {i: value(S_i[i]) for i in range(n)}
    C_sol = {i: value(C_i[i]) for i in range(n)}
    u_sol = {i: value(u[i]) for i in range(n)}
    O_total_sol = value(O_total)

    return {
        "Status": status,
        "Valor Objetivo": obj_value,
        "Asignaciones": x_sol,
        "Inicios": S_sol,
        "Finales": C_sol,
        "Retrasos": u_sol,
        "Ociosidad": O_total_sol
    }


def main():
    """
    Usa SOLO las 10 instancias del informe. A cada hospital se le crea
    una instancia (n, m, p, w, d) con un ejemplo de mapeo simplificado:
      n = n_cirugias_mes
      m = n_quirofanos
      p: se asigna un valor "promedio" derivado de la cadena "duracion_min"
      w: se asume [1]*n
      d: se asume 720 (12:00 PM) como deadline
    Llama solve_instance(...) para cada caso y muestra resultados.
    """
    solver_path = None  # Ajustar si se requiere la ruta exacta de CBC
    hospital_data = get_hospital_instances_from_report()

    resultados = {}

    for info in hospital_data:
        hosp_name = info["hospital"]
        print(f"--- Instancia: {hosp_name} ---")

        # 1) n, m
        n = info["n_cirugias_mes"]
        m = info["n_quirofanos"]

        # 2) Obtenemos la duración media de la cadena "duracion_min"
        dur_range = info["duracion_min"].split("-")
        low = int(dur_range[0].strip())
        high = int(dur_range[1].strip())
        avg_dur = (low + high)//2

        # Creamos p repitiendo avg_dur n veces
        p = [avg_dur]*n

        # 3) w => [1]*n (ejemplo)
        w = [1]*n

        # 4) d => [720]*n (ejemplo)
        d = [720]*n

        # 5) Resolvemos
        res = solve_instance(
            n, m, p, w, d,
            alpha=0.5, beta=1.0, gamma=0.5,
            bigM=1080, solver_path=solver_path, timeLimit=10  # 10s de ejemplo
        )

        resultados[hosp_name] = res

        print(f"Status: {res['Status']}")
        print(f"Valor Objetivo: {res['Valor Objetivo']}\n")

    # Imprimir reporte final
    print("\n========== REPORTE FINAL ==========\n")
    for hosp, res in resultados.items():
        print(f"--- {hosp} ---")
        print(f"Status: {res['Status']}")
        print(f"Valor Objetivo: {res['Valor Objetivo']}")

        # Extraer asignaciones
        x_sol = res["Asignaciones"]
        asign_list = [(i,o) for (i,o),val in x_sol.items() if val and val>0.9]

        print("\nAsignaciones (Cirugía->Quirófano):")
        for (i,o) in asign_list:
            print(f"  Cirugía {i} -> Quirófano {o}")

        S_sol = res["Inicios"]
        C_sol = res["Finales"]
        u_sol = res["Retrasos"]

        print("\nDetalles de cada cirugía:")
        for i in range(len(S_sol)):
            st = S_sol[i]
            en = C_sol[i]
            ret = u_sol[i]
            if st is not None:
                hh_s = int(st//60)
                mm_s = int(st%60)
                hh_e = int(en//60)
                mm_e = int(en%60)
                print(f"  Cirugía {i}: {hh_s:02d}:{mm_s:02d} - {hh_e:02d}:{mm_e:02d}, Retraso={ret}")
            else:
                print(f"  Cirugía {i}: (no asignada)")

        print(f"\nOciosidad Total: {res['Ociosidad']}")
        print("====================================\n")


if __name__ == "__main__":
    main()
