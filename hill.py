# ============================================================
# ALGORITMO HILL CLIMBING (Ascenso de colina)
# Algoritmo de búsqueda local que ayuda a encontrar un MÁXIMO
# (o mínimo) de una función. Parte de una solución inicial y en
# cada paso se mueve al vecino que mejore el valor; se detiene
# cuando ningún vecino es mejor (llegó a la "cima").
#
# Limitación: puede quedarse atrapado en un MÁXIMO LOCAL, por eso
# también se implementa la variante con reinicios aleatorios.
#
# Aplicación sencilla: una tienda quiere decidir cuántas unidades
# producir (x entre 0 y 100) para obtener la mayor ganancia.
# ============================================================

import math
import random


# Función de ganancia (tiene varias "colinas": máximos locales)
def ganancia(x):
    return 50 * math.sin(x / 8) + 0.8 * x - 0.008 * x ** 2


# aqui se implementa el algoritmo Hill Climbing
def hill_climbing(funcion, inicio, paso=1, limite_inf=0, limite_sup=100, mostrar=True):
    actual = inicio
    iteracion = 0

    while True:
        # Generamos los vecinos: un paso a la izquierda y uno a la derecha
        vecinos = [v for v in (actual - paso, actual + paso) if limite_inf <= v <= limite_sup]

        # Elegimos el mejor vecino
        mejor_vecino = max(vecinos, key=funcion)

        if mostrar:
            print(f"   Iteración {iteracion:>2}: x = {actual:>3}  ganancia = {funcion(actual):7.2f}")

        # Si el mejor vecino NO mejora, llegamos a la cima (paramos)
        if funcion(mejor_vecino) <= funcion(actual):
            return actual, funcion(actual)

        actual = mejor_vecino
        iteracion += 1


# aqui se implementa Hill Climbing con reinicios aleatorios
# (ayuda a escapar de los máximos locales probando varios puntos de inicio)
def hill_climbing_reinicios(funcion, reinicios=5, limite_inf=0, limite_sup=100, semilla=42):
    random.seed(semilla)
    mejor_x, mejor_valor = None, float("-inf")

    for i in range(reinicios):
        inicio = random.randint(limite_inf, limite_sup)
        x, valor = hill_climbing(funcion, inicio, limite_inf=limite_inf,
                                 limite_sup=limite_sup, mostrar=False)
        print(f"   Reinicio {i + 1}: inicio en x = {inicio:>3} -> cima en x = {x:>3}  ganancia = {valor:7.2f}")
        if valor > mejor_valor:
            mejor_x, mejor_valor = x, valor

    return mejor_x, mejor_valor
