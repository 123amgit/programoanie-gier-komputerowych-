"""
config.py
=========

Plik konfiguracyjny projektu Lab 08.

W tym pliku celowo trzymamy większość liczb sterujących grą.
Dzięki temu w innych plikach nie ma wielu tak zwanych "magic numbers",
czyli przypadkowych wartości wpisanych bez nazwy i wyjaśnienia.

Laboratorium 08 wymaga refaktoryzacji, dlatego konfiguracja jest
wydzielona w jedno miejsce. Jeżeli chcemy zmienić rozmiar okna,
szybkość statku, limit pocisków albo punktację, najpierw zaglądamy tutaj.
"""

# ------------------------------------------------------------
# OKNO I PODSTAWOWE USTAWIENIA GRY
# ------------------------------------------------------------

SCREEN_W = 1000
SCREEN_H = 700
FPS = 60

# Kolor tła używany jako awaryjne tło pod teksturą gwiazd.
# Raylib przyjmuje kolor jako R, G, B, A.
BG_COLOR = (10, 10, 20, 255)

# ------------------------------------------------------------
# STATEK GRACZA
# ------------------------------------------------------------

SHIP_THRUST = 220.0
SHIP_ROT_SPEED = 180.0
SHIP_FRICTION = 0.99
SHIP_RADIUS = 18.0
SHIP_MAX_SPEED = 420.0

# ------------------------------------------------------------
# POCISKI
# ------------------------------------------------------------

BULLET_SPEED = 620.0
BULLET_RADIUS = 4.0
BULLET_TTL = 1.25
BULLET_LIMIT = 5

# ------------------------------------------------------------
# ASTEROIDY
# ------------------------------------------------------------

# Na starcie gry tworzymy kilka dużych asteroid.
# W Lab 08 asteroidy mają poziomy:
# 3 = duża, 2 = średnia, 1 = mała.
START_ASTEROID_COUNT = 5
ASTEROID_START_LEVEL = 3

# Liczba wierzchołków wielokąta asteroidy.
# Asteroida nie jest idealnym kołem, tylko nierównym polygonem.
ASTEROID_VERTICES = 9

# Promień zależny od poziomu.
# Wymaganie z zadania: promień ma wynikać z level,
# a nie być przekazywany z zewnątrz.
ASTEROID_RADIUS_BY_LEVEL = {
    1: 18.0,
    2: 34.0,
    3: 56.0,
}

# Zakres prędkości zależny od poziomu.
# Mniejsze asteroidy są szybsze, bo trudniej je trafić.
ASTEROID_SPEED_BY_LEVEL = {
    1: (95.0, 165.0),
    2: (60.0, 120.0),
    3: (25.0, 85.0),
}

# Punktacja: mniejsza asteroida daje więcej punktów.
# To zachęca gracza do kończenia podziału asteroid.
SCORE_BY_LEVEL = {
    1: 100,
    2: 50,
    3: 20,
}

# Przy starcie gry asteroidy nie powinny powstawać dokładnie na graczu.
SAFE_SPAWN_DISTANCE = 170.0

# ------------------------------------------------------------
# EKSPLOZJE
# ------------------------------------------------------------

EXPLOSION_TIME = 0.45
EXPLOSION_WIDTH = 3

# ------------------------------------------------------------
# PLIKI I ZASOBY
# ------------------------------------------------------------

ASSETS_DIR = "assets"
SHOOT_SOUND_FILE = "shoot.wav"
EXPLODE_SOUND_FILE = "explode.wav"
STARS_TEXTURE_FILE = "stars.png"

# Najlepszy wynik można zapisać w pliku.
# To jest zadanie dodatkowe, ale działa też jako dobry przykład pracy z plikami.
SCORES_FILE = "scores.txt"
