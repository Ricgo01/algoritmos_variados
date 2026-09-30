# ============================================================
# PROGRAMA PRINCIPAL
# Aquí se ejecutan los 3 algoritmos con una aplicación sencilla:
#   1. A*                          -> robot saliendo de un laberinto
#   2. Hill Climbing               -> maximizar la ganancia de una tienda
#   3. Flujo Máximo - Costo Mínimo -> envío de cajas de fábrica a tienda
# ============================================================

from a_star import a_estrella, dibujar_mapa
from hill import ganancia, hill_climbing, hill_climbing_reinicios
from flujo_max import RedFlujo


def titulo(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


# ------------------------------------------------------------
# 1. A*
# aqui se implementa A* para encontrar la ruta más corta de un
# robot en un laberinto (0 = libre, 1 = pared)
# ------------------------------------------------------------
def demo_a_estrella():
    titulo("1. A* - Robot saliendo de un laberinto")

    laberinto = [
        [0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 1, 0, 0],
    ]
    inicio, meta = (0, 0), (6, 7)

    print("\nLaberinto original (S = inicio, M = meta, █ = pared):\n")
    dibujar_mapa(laberinto, [], inicio, meta)

    camino, explorados = a_estrella(laberinto, inicio, meta)

    if camino:
        print("\nCamino encontrado (*):\n")
        dibujar_mapa(laberinto, camino, inicio, meta)
        print(f"\n-> Pasos del camino más corto: {len(camino) - 1}")
        print(f"-> Nodos explorados por A*:    {explorados}")
        print(f"-> Coordenadas: {camino}")
    else:
        print("\nNo existe un camino hasta la meta.")


# ------------------------------------------------------------
# 2. HILL CLIMBING
# aqui se implementa Hill Climbing para decidir cuántas unidades
# producir y así obtener la mayor ganancia
# ------------------------------------------------------------
def demo_hill_climbing():
    titulo("2. Hill Climbing - Maximizar ganancia de producción")

    # Caso A: Hill Climbing simple (puede quedarse en un máximo local)
    print("\n[A] Hill Climbing simple iniciando en x = 20:\n")
    x, valor = hill_climbing(ganancia, inicio=20)
    print(f"\n-> Cima encontrada: producir {x} unidades, ganancia = {valor:.2f}")
    print("   (ojo: puede ser solo un MÁXIMO LOCAL)")

    # Caso B: con reinicios aleatorios para buscar el máximo global
    print("\n[B] Hill Climbing con reinicios aleatorios:\n")
    mejor_x, mejor_valor = hill_climbing_reinicios(ganancia, reinicios=6)
    print(f"\n-> Mejor solución: producir {mejor_x} unidades, ganancia = {mejor_valor:.2f}")


# ------------------------------------------------------------
# 3. FLUJO MÁXIMO - COSTO MÍNIMO
# aqui se implementa Min-Cost Max-Flow para enviar la mayor
# cantidad de cajas de la fábrica a la tienda al menor costo
# ------------------------------------------------------------
def demo_flujo_max_costo_min():
    titulo("3. Flujo Máximo - Costo Mínimo - Envío de cajas")

    red = RedFlujo(["Fabrica", "AlmacenA", "AlmacenB", "AlmacenC", "Tienda"])

    #               origen      destino    capacidad  costo por caja
    red.agregar_ruta("Fabrica",  "AlmacenA", 10, 2)
    red.agregar_ruta("Fabrica",  "AlmacenB",  8, 4)
    red.agregar_ruta("AlmacenA", "AlmacenB",  5, 1)
    red.agregar_ruta("AlmacenA", "AlmacenC",  7, 6)
    red.agregar_ruta("AlmacenB", "AlmacenC", 10, 2)
    red.agregar_ruta("AlmacenB", "Tienda",    6, 5)
    red.agregar_ruta("AlmacenC", "Tienda",   12, 3)

    print("\nRutas disponibles (capacidad / costo por caja):")
    print("   Fabrica->AlmacenA 10/2 | Fabrica->AlmacenB 8/4 | AlmacenA->AlmacenB 5/1")
    print("   AlmacenA->AlmacenC 7/6 | AlmacenB->AlmacenC 10/2")
    print("   AlmacenB->Tienda 6/5   | AlmacenC->Tienda 12/3")

    print("\nCaminos aumentantes (del más barato al más caro):\n")
    flujo, costo = red.flujo_max_costo_min("Fabrica", "Tienda")

    print("\nFlujo final por cada ruta:\n")
    red.mostrar_rutas_usadas()

    print(f"\n-> Flujo máximo enviado: {flujo} cajas")
    print(f"-> Costo mínimo total:   ${costo}")


if __name__ == "__main__":
    demo_a_estrella()
    demo_hill_climbing()
    demo_flujo_max_costo_min()
