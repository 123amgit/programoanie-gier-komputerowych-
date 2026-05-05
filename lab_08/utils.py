"""
utils.py
========

Funkcje pomocnicze używane przez kilka klas.

Ten plik jest częścią refaktoryzacji z Lab 08.
Zamiast powtarzać te same małe operacje w wielu miejscach,
trzymamy je tutaj i wywołujemy po nazwie.

Przykłady:
- obracanie punktu,
- ograniczanie prędkości,
- wykrywanie kolizji kołowej,
- rysowanie obiektów przy krawędziach świata,
- czyszczenie list obiektów po fladze alive.
"""

import math
from typing import Iterable, List, Tuple, TypeVar

from config import SCREEN_W, SCREEN_H


T = TypeVar("T")


def rotate_point(x: float, y: float, angle_rad: float) -> tuple[float, float]:
    """
    Obraca punkt (x, y) wokół środka układu o podany kąt.

    Funkcja jest używana głównie do rysowania statku i asteroid.
    Obiekty mają własne punkty lokalne, a potem te punkty są obracane
    zgodnie z aktualnym kątem obiektu.
    """
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rotated_x = x * cos_a - y * sin_a
    rotated_y = x * sin_a + y * cos_a

    return rotated_x, rotated_y


def clamp_speed(vx: float, vy: float, max_speed: float) -> tuple[float, float]:
    """
    Ogranicza długość wektora prędkości do max_speed.

    Statek może stale przyspieszać, więc bez limitu po jakimś czasie
    poruszałby się za szybko. Najpierw obliczamy aktualną prędkość
    przez math.hypot, a potem skalujemy wektor, jeśli jest za długi.
    """
    speed = math.hypot(vx, vy)

    if speed > max_speed and speed > 0:
        scale = max_speed / speed
        return vx * scale, vy * scale

    return vx, vy


def ghost_positions(x: float, y: float, size: float) -> List[Tuple[float, float]]:
    """
    Zwraca pozycje dodatkowych kopii obiektu przy krawędziach ekranu.

    Gra używa świata toroidalnego:
    gdy obiekt wyjdzie z lewej strony, pojawia się z prawej.
    Żeby przejście wyglądało płynnie, rysujemy "duchy" obiektu
    przy przeciwnej krawędzi, gdy obiekt jest blisko granicy ekranu.
    """
    possible_x = [x]
    possible_y = [y]

    if x < size:
        possible_x.append(x + SCREEN_W)

    if x > SCREEN_W - size:
        possible_x.append(x - SCREEN_W)

    if y < size:
        possible_y.append(y + SCREEN_H)

    if y > SCREEN_H - size:
        possible_y.append(y - SCREEN_H)

    positions = []

    for draw_x in possible_x:
        for draw_y in possible_y:
            positions.append((draw_x, draw_y))

    return positions


def circle_collision(
    x1: float,
    y1: float,
    r1: float,
    x2: float,
    y2: float,
    r2: float,
) -> bool:
    """
    Sprawdza kolizję dwóch okręgów.

    Kolizja zachodzi wtedy, gdy odległość między środkami
    jest mniejsza lub równa sumie promieni.

    To pasuje do asteroid i pocisków, bo ich przybliżone kształty
    są bardziej okrągłe niż prostokątne.
    """
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance <= r1 + r2


def keep_alive(objects: Iterable[T]) -> list[T]:
    """
    Zwraca nową listę tylko z obiektami, które mają alive == True.

    To zastępuje powtarzanie list comprehension w wielu miejscach.
    Dzięki temu spełniamy część refaktoryzacji z Lab 08:
    powtórzony kod został przeniesiony do funkcji pomocniczej.
    """
    return [obj for obj in objects if getattr(obj, "alive", False)]


def wrap_position(x: float, y: float) -> tuple[float, float]:
    """
    Zawija pozycję w granicach ekranu.

    Funkcja nie zmienia obiektu bezpośrednio, tylko zwraca nową parę.
    Można ją wykorzystać w klasach, które mają pola x i y.
    """
    return x % SCREEN_W, y % SCREEN_H
