# ============================================================
# ALGORITMO FLUJO MÁXIMO - COSTO MÍNIMO (Min-Cost Max-Flow)
# Algoritmo que ayuda a enviar la MAYOR cantidad posible de flujo
# (productos, agua, datos...) desde un origen hasta un destino,
# respetando la capacidad de cada ruta y gastando el MENOR costo
# total posible.
#
# Método usado: "caminos más cortos sucesivos". Se busca
# repetidamente el camino más barato (Bellman-Ford) en la red
# residual y se envía por él todo el flujo que se pueda, hasta
# que ya no existan caminos del origen al destino.
#
# Aplicación sencilla: una fábrica envía cajas a una tienda
# pasando por almacenes; cada carretera tiene una capacidad
# máxima de cajas y un costo por caja.
# ============================================================


class RedFlujo:
    def __init__(self, nombres):
        self.nombres = nombres
        self.n = len(nombres)
        self.indice = {nombre: i for i, nombre in enumerate(nombres)}
        # Cada arista: [destino, capacidad, costo, índice_arista_inversa]
        self.grafo = [[] for _ in range(self.n)]
        self.aristas_originales = []

    def agregar_ruta(self, origen, destino, capacidad, costo):
        u, v = self.indice[origen], self.indice[destino]
        # Arista de ida y arista inversa (residual) con costo negativo
        self.grafo[u].append([v, capacidad, costo, len(self.grafo[v])])
        self.grafo[v].append([u, 0, -costo, len(self.grafo[u]) - 1])
        self.aristas_originales.append((u, len(self.grafo[u]) - 1, capacidad))

    # aqui se implementa el algoritmo de Flujo Máximo - Costo Mínimo
    def flujo_max_costo_min(self, origen, destino):
        s, t = self.indice[origen], self.indice[destino]
        flujo_total, costo_total = 0, 0
        iteracion = 1

        while True:
            # Bellman-Ford: camino más barato de s a t en la red residual
            # (se usa Bellman-Ford porque las aristas inversas tienen costo negativo)
            distancia = [float("inf")] * self.n
            distancia[s] = 0
            previo = [None] * self.n  # (nodo_anterior, índice_arista)

            for _ in range(self.n - 1):
                hubo_cambio = False
                for u in range(self.n):
                    if distancia[u] == float("inf"):
                        continue
                    for i, (v, cap, costo, _) in enumerate(self.grafo[u]):
                        if cap > 0 and distancia[u] + costo < distancia[v]:
                            distancia[v] = distancia[u] + costo
                            previo[v] = (u, i)
                            hubo_cambio = True
                if not hubo_cambio:
                    break

            # Si ya no se puede llegar al destino, terminamos
            if distancia[t] == float("inf"):
                break

            # Buscar el cuello de botella (capacidad mínima del camino)
            envio = float("inf")
            v = t
            camino = [self.nombres[t]]
            while v != s:
                u, i = previo[v]
                envio = min(envio, self.grafo[u][i][1])
                camino.append(self.nombres[u])
                v = u
            camino.reverse()

            # Enviar el flujo: restar capacidad en ida, sumar en la inversa
            v = t
            while v != s:
                u, i = previo[v]
                self.grafo[u][i][1] -= envio
                inv = self.grafo[u][i][3]
                self.grafo[v][inv][1] += envio
                v = u

            flujo_total += envio
            costo_total += envio * distancia[t]
            print(f"   Camino {iteracion}: {' -> '.join(camino)} | "
                  f"envía {envio} cajas a costo {distancia[t]} c/u")
            iteracion += 1

        return flujo_total, costo_total

    # Muestra cuánto flujo pasó por cada ruta al final
    def mostrar_rutas_usadas(self):
        for u, i, capacidad in self.aristas_originales:
            v, cap_restante, costo, _ = self.grafo[u][i]
            usado = capacidad - cap_restante
            if usado > 0:
                print(f"   {self.nombres[u]:>10} -> {self.nombres[v]:<10} "
                      f"{usado:>2}/{capacidad:<2} cajas  (costo {costo} c/u)")
