import math
from typing import List, Tuple


# Função para calcular a distância euclidiana entre dois pontos
def distancia(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Função para encontrar a coordenada mais próxima em uma lista de coordenadas
def encontrar_coordenada_proxima(
    coord_referencia: Tuple[float, float], coordenadas: List[Tuple[float, float]]
) -> Tuple[Tuple[float, float], float]:
    if not coordenadas:
        raise ValueError("A lista de coordenadas não pode estar vazia")

    distancia_minima = float("inf")  # infinito positivo
    coord_proxima = coordenadas[0]

    for coord in coordenadas:
        dist = distancia(coord_referencia, coord)
        if dist < distancia_minima:
            distancia_minima = dist
            coord_proxima = coord

    return coord_proxima, distancia_minima
