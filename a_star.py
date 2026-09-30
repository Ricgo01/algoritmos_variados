# ============================================================
# ALGORITMO A* (A estrella)
# Algoritmo que ayuda a encontrar el camino MÁS CORTO entre un
# punto de inicio y un punto destino, usando una heurística
# (estimación de la distancia restante) para explorar primero
# los caminos más prometedores.
#
# Fórmula clave:  f(n) = g(n) + h(n)
#   g(n) -> costo real desde el inicio hasta el nodo n
#   h(n) -> estimación (heurística) desde n hasta la meta
#
# Aplicación sencilla: un robot que debe salir de un laberinto
# (cuadrícula) esquivando paredes.
# ============================================================

import heapq


# Heurística: distancia Manhattan (sirve porque solo nos movemos
# arriba, abajo, izquierda y derecha)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# aqui se implementa el algoritmo A*
def a_estrella(mapa, inicio, meta):
    filas, columnas = len(mapa), len(mapa[0])

    # Cola de prioridad (lista abierta) ordenada por f(n)
    abiertos = [(heuristica(inicio, meta), 0, inicio)]
    padre = {inicio: None}   # para reconstruir el camino
    g = {inicio: 0}          # costo real acumulado
    visitados = set()        # lista cerrada

    while abiertos:
        _, g_actual, actual = heapq.heappop(abiertos)

        if actual in visitados:
            continue
        visitados.add(actual)

        # Si llegamos a la meta, reconstruimos el camino hacia atrás
        if actual == meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1], len(visitados)

        # Revisamos los 4 vecinos (arriba, abajo, izquierda, derecha)
        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecino = (actual[0] + df, actual[1] + dc)
            f, c = vecino

            # Validar que esté dentro del mapa y que no sea pared (1)
            if 0 <= f < filas and 0 <= c < columnas and mapa[f][c] == 0:
                nuevo_g = g_actual + 1  # cada paso cuesta 1
                if nuevo_g < g.get(vecino, float("inf")):
                    g[vecino] = nuevo_g
                    padre[vecino] = actual
                    heapq.heappush(abiertos, (nuevo_g + heuristica(vecino, meta), nuevo_g, vecino))

    return None, len(visitados)  # no existe camino


# Función auxiliar para dibujar el laberinto con el camino encontrado
def dibujar_mapa(mapa, camino, inicio, meta):
    camino = set(camino or [])
    for i, fila in enumerate(mapa):
        linea = ""
        for j, celda in enumerate(fila):
            if (i, j) == inicio:
                linea += " S "
            elif (i, j) == meta:
                linea += " M "
            elif celda == 1:
                linea += " █ "
            elif (i, j) in camino:
                linea += " * "
            else:
                linea += " . "
        print(linea)
