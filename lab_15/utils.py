# utils.py
# Funkcje pomocnicze. W kolejnych etapach pojawią się tutaj kolizje,
# ograniczanie pozycji do ekranu i obliczanie odległości.

import math


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)
