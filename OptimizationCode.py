from pulp import (
    LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpContinuous,
    LpStatus, value, COIN_CMD, GLPK_CMD
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
        d = [600, 600, 600, 600, 600, 720, 720, 720, 720, 720, 720, 720, 720, 720, 720, 600, 600, 600, 600, 600]  # Deadline en minutos desde la medianoche (10:00 AM = 600, 12:00 PM = 720)

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

def build_model(n, m, p, w, d, alpha=0.5, beta=1, gamma=0.5, bigM=10000):
    """
    Construye el modelo de Programación Entera Mixta para la asignación y programación de cirugías.

    Parámetros:
        n (int): Número de cirugías.
        m (int): Número de quirófanos.
        p (list): Duraciones de las cirugías (en minutos).
        w (list): Pesos/prioridades de las cirugías.
        d (list): Deadlines para cada cirugía (en minutos desde la medianoche).
        alpha (float): Coeficiente para el término de tiempos de finalización ponderados.
        beta (float): Coeficiente para la ociosidad total.
        gamma (float): Coeficiente para los retrasos.
        bigM (int): Constante grande para las restricciones de no solapamiento.

    Retorna:
        tuple: Contiene el modelo (prob) y las variables definidas (x, z, S_i, C_i, u, O_total).
    """
    # Definición del problema de optimización: Minimizar la función objetivo
    prob = LpProblem("Programacion_Cirugias_no_GES", LpMinimize)

    S = range(n)  # Conjunto de cirugías (índices de 0 a n-1)
    O = range(m)  # Conjunto de quirófanos (índices de 0 a m-1)

    # Variables de decisión:
    # x[i][o]: 1 si la cirugía i se asigna al quirófano o, 0 en caso contrario
    x = LpVariable.dicts("x", (S, O), 0, 1, LpBinary)

    # z[i][j][o]: 1 si la cirugía i precede a la cirugía j en el quirófano o, 0 en caso contrario
    z = LpVariable.dicts("z", (S, S, O), 0, 1, LpBinary)

    # S_i: Tiempo de inicio de la cirugía i (en minutos desde la medianoche)
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)

    # C_i: Tiempo de finalización de la cirugía i (en minutos desde la medianoche)
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)

    # u[i]: Retraso de la cirugía i (max(C_i - d_i, 0))
    u = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    # w_oo[o]: Tiempo total de trabajo asignado al quirófano o
    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)

    # O_total: Ociosidad total de todos los quirófanos
    O_total = LpVariable("Ociosidad_Total", 0)

    # H: Constante grande para calcular la ociosidad total de quirófanos
    H = sum(p) + 100  # Suma de todas las duraciones de cirugías más un buffer adicional

    # Definición de la función objetivo:
    # Minimizar una combinación ponderada de:
    # - Tiempos de finalización ponderados por prioridad
    # - Retrasos acumulados
    # - Ociosidad total de quirófanos
    prob += (
        alpha * lpSum(w[i] * C_i[i] for i in S) +  # Tiempos de finalización ponderados
        gamma * lpSum(u[i] for i in S) +           # Retrasos acumulados
        beta * O_total                             # Ociosidad total
    ), "Función_Objetivo"

    # Restricciones

    # 1. Asignación única:
    # Cada cirugía debe ser asignada a exactamente un quirófano.
    for i in S:
        prob += lpSum(x[i][o] for o in O) == 1, f"Asignacion_Unica_{i}"

    # 2. Relación entre tiempos de inicio y finalización:
    # El tiempo de finalización de una cirugía es igual al tiempo de inicio más su duración.
    for i in S:
        prob += C_i[i] == S_i[i] + p[i], f"Completion_Time_{i}"

    # 3. Secuenciación de cirugías en cada quirófano:
    # Asegura que la variable z[i][j][o] solo puede ser 1 si la cirugía i está asignada al quirófano o.
    for i in S:
        for o in O:
            # Restricción para z[i][j][o]
            prob += (
                lpSum(z[i][j][o] for j in S if j != i) <= x[i][o],
                f"Secuenciacion_1_{i}_{o}"
            )
            # Restricción para z[j][i][o]
            prob += (
                lpSum(z[j][i][o] for j in S if j != i) <= x[i][o],
                f"Secuenciacion_2_{i}_{o}"
            )

    # 4. No solapamiento de cirugías:
    # Si z[i][j][o] = 1, entonces la cirugía j debe comenzar después de que la cirugía i termine.
    for i in S:
        for j in S:
            if i != j:
                for o in O:
                    prob += (
                        S_i[j] >= C_i[i] - bigM * (1 - z[i][j][o]),
                        f"No_Solapamiento_{i}_{j}_{o}"
                    )

    # 5. Definición de los retrasos:
    # u[i] es al menos la diferencia entre el tiempo de finalización y el deadline.
    # Además, u[i] no puede ser negativo.
    for i in S:
        prob += u[i] >= C_i[i] - d[i], f"Delay_Positive_{i}"
        prob += u[i] >= 0, f"Delay_NonNegative_{i}"  # El retraso no puede ser negativo

    # 6. Cálculo de la ociosidad de cada quirófano:
    # w_oo[o] es el tiempo total de trabajo en el quirófano o.
    for o in O:
        prob += (
            w_oo[o] == lpSum(x[i][o] * p[i] for i in S),
            f"Ociosidad_O_{o}"
        )

    # 7. Cálculo de la ociosidad total:
    # O_total es la suma de la ociosidad de todos los quirófanos.
    prob += (
        O_total == lpSum(H - w_oo[o] for o in O),
        "Ociosidad_Total"
    )

    # **Verificación de Variables Binarias**
    binary_vars = [v for v in prob.variables() if v.cat == 'Binary']
    print(f"Número de variables binarias en el modelo: {len(binary_vars)}")
    if len(binary_vars) == 0:
        print("Advertencia: No se encontraron variables binarias en el modelo.")

    # **Exportar el Modelo para Inspección**
    prob.writeLP("model.lp")
    prob.writeMPS("model.mps")

    return prob, x, z, S_i, C_i, u, O_total

def solve_instance(instance_type, solver_path=None, use_glpk=False):
    """
    Resuelve una instancia específica del modelo de programación de cirugías.

    Parámetros:
        instance_type (int): Tipo de instancia a resolver.
        solver_path (str): Ruta al ejecutable del solucionador CBC (opcional).
        use_glpk (bool): Si es True, utiliza GLPK en lugar de CBC.

    Retorna:
        tuple: Incluye el estado de la solución, valor objetivo, asignaciones,
               tiempos de inicio y finalización, retrasos, ociosidad total,
               y los datos de la instancia.
    """
    # Generar datos para la instancia especificada
    n, m, p, w, d = generate_instance_data(instance_type)

    # Construir el modelo con los datos generados
    prob, x, z, S_i, C_i, u, O_total = build_model(
        n, m, p, w, d,
        alpha=0.5, beta=1.0, gamma=0.5, bigM=10000  # Se cambiaron los valores de alpha, beta y gamma
    )

    # Verificar que hay variables binarias
    binary_vars = [v for v in prob.variables() if v.cat == 'Binary']
    print(f"Total de variables binarias: {len(binary_vars)}")

    # Seleccionar el solucionador
    if use_glpk:
        # Usar GLPK como solucionador alternativo
        solver = GLPK_CMD(msg=True, timeLimit=120)
    else:
        # Usar CBC como solucionador principal
        if solver_path:
            # Especificar la ruta personalizada del solucionador CBC usando COIN_CMD
            solver = COIN_CMD(path=solver_path, msg=True, timeLimit=120)
        else:
            # Usar la versión integrada de CBC en PuLP
            solver = COIN_CMD(msg=True, timeLimit=120)

    # Resolver el modelo
    prob.solve(solver)

    # Obtener el estado de la solución (Optimal, Infeasible, etc.)
    status = LpStatus[prob.status]

    # Obtener el valor de la función objetivo
    obj_value = value(prob.objective)

    # Extraer las asignaciones de cirugías a quirófanos
    # (i, o) indica la asignación de la cirugía i al quirófano o
    x_sol = {(i, o): value(x[i][o]) for i in range(n) for o in range(m)}

    # Extraer los tiempos de inicio de cada cirugía
    S_sol = {i: value(S_i[i]) for i in range(n)}

    # Extraer los tiempos de finalización de cada cirugía
    C_sol = {i: value(C_i[i]) for i in range(n)}

    # Extraer los retrasos de cada cirugía
    u_sol = {i: value(u[i]) for i in range(n)}

    # Extraer la ociosidad total
    O_total_sol = value(O_total)

    return status, obj_value, x_sol, S_sol, C_sol, u_sol, O_total_sol, n, m, p, w, d

def print_summary(summary, detailed_summary):
    """
    Imprime un resumen tabular de los resultados de todas las instancias.

    Parámetros:
        summary (dict): Diccionario con el resumen general de las instancias.
        detailed_summary (dict): Diccionario con el resumen detallado de cada instancia.
    """
    print("=== Resumen de Todas las Instancias ===")
    print("{:<10} {:<15} {:<20} {:<20} {:<20} {:<20}".format(
        "Instancia", "Status", "Valor Objetivo",
        "Total Asignaciones", "Total Retrasos", "Total Ociosidad"
    ))
    for i in range(len(summary["Instancia"])):
        print("{:<10} {:<15} {:<20} {:<20} {:<20} {:<20}".format(
            summary["Instancia"][i],
            summary["Status"][i],
            round(summary["Valor Objetivo"][i], 2),
            summary["Total Asignaciones"][i],
            round(summary["Total Retrasos"][i], 2),
            round(summary["Total Ociosidad"][i], 2)
        ))

    # Imprimir resumen detallado (opcional)
    # Descomentar estas dos líneas si deseas que se imprima el resumen detallado
    # for inst_type, details in detailed_summary.items():
    #     print_detailed_summary(inst_type, details)

def print_detailed_summary(inst_type, details):
    """
    Imprime el resumen detallado de una instancia específica.

    Parámetros:
        inst_type (int): Tipo de instancia.
        details (dict): Diccionario con los detalles de la instancia.
    """
    
    print(f"\n=== Resumen Detallado Instancia {inst_type} ===")
    print("Asignaciones (Cirugía -> Quirófano):", details["Asignaciones"])
    print("\nTiempos de Inicio y Finalización (en minutos desde la medianoche):")
    for i in range(len(details["Inicios"])):
        inicio = details["Inicios"][i]
        fin = details["Finalizaciones"][i]
        retraso = details["Retrasos"][i]
        
        # Convertir minutos desde la medianoche a formato HH:MM
        inicio_hhmm = f"{int(inicio // 60):02d}:{int(inicio % 60):02d}"
        fin_hhmm = f"{int(fin // 60):02d}:{int(fin % 60):02d}"

        print(f"Cirugía {i}: Inicio = {inicio_hhmm}, Finalización = {fin_hhmm}, Retraso = {retraso}")
    print("\nOciosidad por Quirófano:")
    for o, ociosidad in details["Ociosidad_Quirófano"].items():
        print(f"  Quirófano {o}: {ociosidad:.2f}")
    print(f"Ociosidad Total: {details['Ociosidad']:.2f}")

def main():
    """
    Función principal que resuelve múltiples instancias del modelo
    y proporciona un resumen de los resultados.
    """
    # Inicializar el diccionario para el resumen de resultados
    summary = {
        "Instancia": [],
        "Status": [],
        "Valor Objetivo": [],
        "Total Asignaciones": [],
        "Total Retrasos": [],
        "Total Ociosidad": []
    }
    # Diccionario para almacenar detalles más específicos por instancia
    detailed_summary = {}

    # Ruta al solucionador CBC actualizado (ajustar según tu instalación)
    # Por ejemplo: 'C:\\cbc\\bin\\cbc.exe'
    # Si está en el PATH, puedes dejarlo como None
    # Ruta al solucionador CBC
    solver_path = "C:\\Users\\cocan\\OneDrive\\Escritorio\\otros\\Universidad\\Metodos de Optimizacion\\bin\\cbc.exe"

    # Iterar sobre los tipos de instancias definidos (1, 2, 3, 5)
    for inst_type in [1, 2, 3, 5]:
        print(f"--- Resolviendo instancia {inst_type} ---")

        # Resolver la instancia
        # Puedes cambiar `use_glpk=True` para usar GLPK en lugar de CBC
        status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n, m, p, w, d = solve_instance(inst_type, solver_path=solver_path, use_glpk=False)

        # Imprimir el estado y valor objetivo
        print("Status:", status)
        print("Valor Objetivo:", obj)

        # Identificar las asignaciones efectivas (donde x[i][o] ≈ 1)
        asignaciones = [(i, o) for (i, o), val in x_sol.items() if val > 0.9]
        print(f"Asignaciones (Cirugía->Quirófano) en instancia {inst_type}:", asignaciones)

        # Imprimir detalles de inicio y finalización de cada cirugía
        print("\nDetalles de inicio y finalización (en minutos desde la medianoche):")
        for i in range(n):
            inicio = S_sol[i]
            fin = C_sol[i]

            # Convertir minutos desde la medianoche a formato HH:MM
            inicio_hhmm = f"{int(inicio // 60):02d}:{int(inicio % 60):02d}"
            fin_hhmm = f"{int(fin // 60):02d}:{int(fin % 60):02d}"

            print(f"Cirugía {i}: Inicio = {inicio_hhmm}, Finalización = {fin_hhmm}, Retraso = {u_sol[i]}")
        print("\n" + "-"*50 + "\n")

        # Calcular la ociosidad de cada quirófano
        ociosidad_quirofano = {}
        for o in range(m):
            # Tiempo total de trabajo en el quirófano o
            tiempo_trabajo = sum(p[i] for i in range(n) if x_sol.get((i, o), 0) > 0.9)
            # Tiempo de inicio de la primera cirugía asignada al quirófano o
            tiempos_asignados = [S_sol[i] for i in range(n) if x_sol.get((i, o), 0) > 0.9]
            if tiempos_asignados:
                tiempo_inicio = min(tiempos_asignados)
                tiempo_fin = max([C_sol[i] for i in range(n) if x_sol.get((i, o), 0) > 0.9])
                # Cálculo de la ociosidad:
                # ociosidad = tiempo disponible (tiempo entre la primera y última cirugía) - tiempo de trabajo
                ociosidad = (tiempo_fin - tiempo_inicio - tiempo_trabajo)
            else:
                ociosidad = 0
            ociosidad_quirofano[o] = ociosidad

        # Guardar detalles específicos de la instancia
        detailed_summary[inst_type] = {
            "Asignaciones": asignaciones,
            "Inicios": S_sol,
            "Finalizaciones": C_sol,
            "Retrasos": u_sol,
            "Ociosidad": O_total,
            "Ociosidad_Quirófano": ociosidad_quirofano
        }

        # Actualizar el resumen con los resultados de la instancia actual
        summary["Instancia"].append(inst_type)
        summary["Status"].append(status)
        summary["Valor Objetivo"].append(obj)
        summary["Total Asignaciones"].append(len(asignaciones))
        summary["Total Retrasos"].append(sum(u_sol.values()))
        summary["Total Ociosidad"].append(O_total)

    # Imprimir el resumen tabular de todas las instancias
    print_summary(summary, detailed_summary)

if __name__ == "__main__":
    main()
