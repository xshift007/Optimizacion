from pulp import (
    LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpContinuous,
    LpStatus, value, PULP_CBC_CMD
)

def generate_instance_data(instance_type):
    """
    Genera los datos de entrada para una instancia específica basada en el tipo de hospital.
    
    Parámetros:
        instance_type (int): Tipo de instancia (1, 2, 3 o 5).
    
    Retorna:
        tuple: Contiene el número de cirugías (n), número de quirófanos (m),
               lista de duraciones de cirugías (p), pesos/prioridades (w),
               y deadlines (d) para cada cirugía.
    """
    if instance_type == 1:
        # Instancia 1: Hospital urbano alta complejidad
        n = 20  # Número total de cirugías
        m = 7   # Número de quirófanos disponibles
        # Detalle de las cirugías:
        # 5 oftalmológicas (60 minutos, peso=1, deadline=200)
        # 10 colecciones (150 minutos, peso=2, deadline=250)
        # 5 artroscópicas (180 minutos, peso=5, deadline=200)
        p = [60]*5 + [150]*10 + [180]*5  # Duraciones de las cirugías
        w = [1]*5 + [2]*10 + [5]*5      # Pesos/prioridades de las cirugías
        d = [200]*5 + [250]*10 + [200]*5  # Deadlines para cada cirugía
    elif instance_type == 2:
        # Instancia 2: Hospital rural con 1 quirófano
        n = 8
        m = 1
        p = [90]*8        # Todas las cirugías duran 90 minutos
        w = [2]*8         # Peso=2 para todas las cirugías
        d = [300]*8       # Deadline de 300 minutos para todas
    elif instance_type == 3:
        # Instancia 3: Centro oftalmológico con 3 quirófanos
        n = 15
        m = 3
        p = [60]*15        # Todas las cirugías duran 60 minutos
        w = [1]*15         # Peso=1 para todas las cirugías
        d = [200]*15       # Deadline de 200 minutos para todas
    elif instance_type == 5:
        # Instancia 5: Región Extrema (Magallanes) con 1 quirófano
        n = 10
        m = 1
        p = [150]*5 + [60]*5   # 5 cirugías de 150 min y 5 de 60 min
        w = [2]*5 + [1]*5       # 5 cirugías con peso=2 y 5 con peso=1
        d = [400]*10            # Deadline de 400 minutos para todas
    else:
        raise ValueError("Instancia no definida. Use 1,2,3 o 5.")
    return n, m, p, w, d

def build_model(n, m, p, w, d, alpha=1.0, beta=0.1, gamma=0.5, bigM=10000):
    """
    Construye el modelo de Programación Entera Mixta para la asignación y programación de cirugías.
    
    Parámetros:
        n (int): Número de cirugías.
        m (int): Número de quirófanos.
        p (list): Duraciones de las cirugías.
        w (list): Pesos/prioridades de las cirugías.
        d (list): Deadlines para cada cirugía.
        alpha (float): Coeficiente para el término de tiempos de finalización ponderados.
        beta (float): Coeficiente para la ociosidad total.
        gamma (float): Coeficiente para los retrasos.
        bigM (int): Constante grande para las restricciones de no solapamiento.
    
    Retorna:
        tuple: Contiene el modelo (prob) y las variables definidas (x, z, S_i, C_i, u, O_total).
    """
    # Definición del problema de optimización: Minimizar la función objetivo
    prob = LpProblem("Programacion_Cirugias_no_GES", LpMinimize)
    
    S = range(n)  # Conjunto de cirugías
    O = range(m)  # Conjunto de quirófanos

    # Variables de decisión:
    # x[i][o]: 1 si la cirugía i se asigna al quirófano o, 0 en caso contrario
    x = LpVariable.dicts("x", (S, O), 0, 1, LpBinary)
    
    # z[i][j][o]: 1 si la cirugía i precede a la cirugía j en el quirófano o, 0 en caso contrario
    z = LpVariable.dicts("z", (S, S, O), 0, 1, LpBinary)
    
    # S_i: Tiempo de inicio de la cirugía i
    S_i = LpVariable.dicts("Start", S, 0, None, LpContinuous)
    
    # C_i: Tiempo de finalización de la cirugía i
    C_i = LpVariable.dicts("Completion", S, 0, None, LpContinuous)
    
    # u[i]: Retraso de la cirugía i (max(C_i - d_i, 0))
    u = LpVariable.dicts("Delay", S, 0, None, LpContinuous)

    # H: Constante grande para calcular la ociosidad
    H = sum(p) + 100
    
    # w_oo[o]: Tiempo total de trabajo asignado al quirófano o
    w_oo = LpVariable.dicts("Work_O", O, 0, None, LpContinuous)
    
    # O_total: Ociosidad total de todos los quirófanos
    O_total = LpVariable("Ociosidad_Total", 0)

    # Definición de la función objetivo:
    # Minimizar: 
    #   - Tiempo de finalización ponderado por prioridad
    #   - Retrasos acumulados
    #   - Ociosidad total de quirófanos
    prob += (
        alpha * lpSum(w[i] * C_i[i] for i in S) +  # Tiempos de finalización ponderados
        gamma * lpSum(u[i] for i in S) +          # Retrasos acumulados
        beta * O_total                            # Ociosidad total
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
            prob += (
                lpSum(z[i][j][o] for j in S if j != i) <= x[i][o],
                f"Secuenciacion_1_{i}_{o}"
            )
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
    for i in S:
        prob += u[i] >= C_i[i] - d[i], f"Delay_Positive_{i}"
        prob += u[i] >= 0, f"Delay_NonNegative_{i}"

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

    return prob, x, z, S_i, C_i, u, O_total

def solve_instance(instance_type, solver_path=None):
    """
    Resuelve una instancia específica del modelo de programación de cirugías.
    
    Parámetros:
        instance_type (int): Tipo de instancia a resolver.
        solver_path (str, opcional): Ruta al solucionador, si es necesario.
    
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
        alpha=1.0, beta=0.1, gamma=0.5, bigM=10000
    )

    # Configurar el solucionador CBC con mensajes activados y límite de tiempo de 120 segundos
    solver = PULP_CBC_CMD(msg=1, timeLimit=120)
    
    # Resolver el modelo
    prob.solve(solver)

    # Obtener el estado de la solución (Optimal, Infeasible, etc.)
    status = LpStatus[prob.status]
    
    # Obtener el valor de la función objetivo
    obj_value = value(prob.objective)

    # Extraer las asignaciones de cirugías a quirófanos
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

    # Iterar sobre los tipos de instancias definidos (1, 2, 3, 5)
    for inst_type in [1, 2, 3, 5]:
        print(f"--- Resolviendo instancia {inst_type} ---")
        
        # Resolver la instancia
        status, obj, x_sol, S_sol, C_sol, u_sol, O_total, n, m, p, w, d = solve_instance(inst_type)
        
        # Imprimir el estado y valor objetivo
        print("Status:", status)
        print("Valor Objetivo:", obj)
        
        # Identificar las asignaciones efectivas (donde x[i][o] ≈ 1)
        asignaciones = [(i, o) for (i, o), val in x_sol.items() if val > 0.9]
        print(f"Asignaciones (Cirugía->Quirófano) en instancia {inst_type}:", asignaciones)
        
        # Imprimir detalles de inicio y finalización de cada cirugía
        print("\nDetalles de inicio y finalización:")
        for i in range(n):
            print(f"Cirugía {i}: Inicio = {S_sol[i]}, Finalización = {C_sol[i]}, Retraso = {u_sol[i]}")
        print("\n" + "-"*50 + "\n")

        # Actualizar el resumen con los resultados de la instancia actual
        summary["Instancia"].append(inst_type)
        summary["Status"].append(status)
        summary["Valor Objetivo"].append(obj)
        summary["Total Asignaciones"].append(len(asignaciones))
        summary["Total Retrasos"].append(sum(u_sol.values()))
        summary["Total Ociosidad"].append(O_total)

        # Guardar detalles específicos de la instancia
        detailed_summary[inst_type] = {
            "Asignaciones": asignaciones,
            "Inicios": S_sol,
            "Finalizaciones": C_sol,
            "Retrasos": u_sol,
            "Ociosidad": O_total
        }

    # Imprimir un resumen consolidado de todas las instancias resueltas
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

    # Opcional: Puedes guardar `detailed_summary` en un archivo o procesarlo según tus necesidades

if __name__ == "__main__":
    main()
