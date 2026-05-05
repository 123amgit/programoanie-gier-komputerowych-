import math
import os
import random
import pyray as rl

from config import (
    SCREEN_W,
    SCREEN_H,
    FPS,
    BG_COLOR,
    ASTEROID_COUNT,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MAX_RADIUS,
    SHIP_RADIUS,
    BULLET_LIMIT,
)
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import circle_collision


# ============================================================
# LABORATORIUM 07 - ASTEROIDS
# Temat:
# - pociski,
# - zasoby,
# - dźwięki,
# - kolizje,
# - eksplozje,
# - tło gry.
#
# Ten plik jest głównym plikiem programu.
# Znajduje się tutaj:
# - inicjalizacja okna i audio,
# - tworzenie obiektów gry,
# - główna pętla gry,
# - obsługa wejścia z klawiatury,
# - aktualizacja obiektów,
# - sprawdzanie kolizji,
# - rysowanie sceny,
# - zwalnianie zasobów po zamknięciu programu.
# ============================================================


# Folder z zasobami gry.
# W nim powinny znajdować się pliki:
# - shoot.wav
# - explode.wav
# - stars.png
ASSETS_DIR = "assets"

SHOOT_SOUND_PATH = os.path.join(ASSETS_DIR, "shoot.wav")
EXPLODE_SOUND_PATH = os.path.join(ASSETS_DIR, "explode.wav")
STARS_PATH = os.path.join(ASSETS_DIR, "stars.png")


def create_asteroids(count: int):
    """
    Tworzy listę asteroid.

    Każda asteroida dostaje:
    - losową pozycję,
    - losowy promień,
    - losowy kierunek ruchu i prędkość,
    - nieregularny kształt wielokąta.

    Funkcja jest używana na początku gry oraz wtedy,
    gdy wszystkie asteroidy zostaną zniszczone.
    """
    asteroids = []

    for _ in range(count):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        radius = random.uniform(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)

        asteroids.append(Asteroid(x, y, radius))

    return asteroids


def create_star_field(count: int = 160):
    """
    Tworzy proceduralne tło gwiazd.

    Jest to zapasowa wersja tła.
    Jeżeli w folderze assets nie ma pliku stars.png,
    program nadal działa i rysuje proste gwiazdy jako małe kropki.

    Gwiazdy są generowane tylko raz, a potem rysowane co klatkę.
    Dzięki temu tło nie miga i nie zmienia się przypadkowo.
    """
    stars = []

    for _ in range(count):
        x = random.randint(0, SCREEN_W - 1)
        y = random.randint(0, SCREEN_H - 1)

        # Większość gwiazd ma promień 1,
        # tylko część jest trochę większa.
        radius = random.choice([1, 1, 1, 2])

        stars.append((x, y, radius))

    return stars


def draw_procedural_stars(stars):
    """
    Rysuje proceduralnie wygenerowane gwiazdy.

    Funkcja jest używana tylko wtedy,
    gdy nie korzystamy z tekstury stars.png.
    """
    for x, y, radius in stars:
        rl.draw_circle(x, y, radius, rl.Color(190, 190, 210, 255))


def ship_nose_position(ship: Ship):
    """
    Oblicza pozycję nosa statku.

    Ważne:
    Pocisk nie powinien startować ze środka statku ani z boku.
    Powinien pojawiać się z przodu, czyli na czubku statku.

    W klasie Ship kąt jest zapisany w stopniach.
    Kierunek statku jest zgodny z ruchem:
    - cos(angle) daje składową X,
    - sin(angle) daje składową Y.

    Dlatego pozycja nosa to:
    pozycja statku + kierunek * promień statku.

    Dodałem +8, żeby pocisk był od razu lekko przed statkiem,
    a nie wewnątrz jego kształtu.
    """
    angle_rad = math.radians(ship.angle_deg)

    nose_x = ship.x + math.cos(angle_rad) * (ship.radius + 8)
    nose_y = ship.y + math.sin(angle_rad) * (ship.radius + 8)

    return nose_x, nose_y


def reset_ship(ship: Ship):
    """
    Resetuje statek po kolizji z asteroidą.

    Gra się nie kończy.
    Statek wraca na środek ekranu,
    jego prędkość jest zerowana,
    a kierunek ustawiany ponownie do góry.
    """
    ship.x = SCREEN_W / 2
    ship.y = SCREEN_H / 2
    ship.vx = 0.0
    ship.vy = 0.0
    ship.angle_deg = -90.0


def load_background():
    """
    Ładuje tło gry.

    Jeżeli istnieje plik assets/stars.png,
    program ładuje go jako teksturę.

    Jeżeli pliku nie ma,
    program używa proceduralnego tła z gwiazd.
    Dzięki temu projekt jest odporny na brak pliku graficznego.
    """
    if os.path.exists(STARS_PATH):
        texture = rl.load_texture(STARS_PATH)
        return texture, None

    stars = create_star_field()
    return None, stars


def draw_background(stars_texture, procedural_stars):
    """
    Rysuje tło jako pierwszą warstwę sceny.

    Kolejność rysowania jest ważna:
    1. tło,
    2. statek,
    3. asteroidy,
    4. pociski,
    5. eksplozje,
    6. tekst interfejsu.

    Dzięki temu tło nie zasłania obiektów gry.
    """
    if stars_texture is not None:
        rl.draw_texture(stars_texture, 0, 0, rl.WHITE)
    else:
        draw_procedural_stars(procedural_stars)


def handle_shooting(ship: Ship, bullets: list, shoot_sound):
    """
    Obsługuje strzał gracza.

    Używamy is_key_pressed, a nie is_key_down.

    Różnica:
    - is_key_down działa cały czas, gdy klawisz jest trzymany,
      więc pociski powstawałyby co klatkę.
    - is_key_pressed działa tylko w momencie pojedynczego naciśnięcia,
      więc jeden klik = jeden pocisk.

    Dodatkowo używany jest limit pocisków.
    Jeśli na ekranie jest już za dużo pocisków,
    nowy strzał zostaje zignorowany.
    """
    if rl.is_key_pressed(rl.KEY_SPACE):
        if len(bullets) < BULLET_LIMIT:
            nose_x, nose_y = ship_nose_position(ship)

            bullet = Bullet(nose_x, nose_y, ship.angle_deg)
            bullets.append(bullet)

            rl.play_sound(shoot_sound)


def update_game_objects(dt: float, ship: Ship, asteroids: list, bullets: list, explosions: list):
    """
    Aktualizuje wszystkie obiekty gry.

    dt oznacza delta time, czyli czas od poprzedniej klatki.
    Dzięki temu ruch nie zależy bezpośrednio od liczby FPS.
    """
    ship.update(dt)
    ship.wrap()

    for asteroid in asteroids:
        asteroid.update(dt)
        asteroid.wrap()

    for bullet in bullets:
        bullet.update(dt)

    for explosion in explosions:
        explosion.update(dt)


def check_bullet_asteroid_collisions(bullets: list, asteroids: list, explosions: list, explode_sound):
    """
    Sprawdza kolizje pocisków z asteroidami.

    Kolizja jest kołowa:
    jeżeli odległość między środkami dwóch obiektów
    jest mniejsza lub równa sumie ich promieni,
    to obiekty się zderzyły.

    Po trafieniu:
    - pocisk zostaje oznaczony jako nieaktywny,
    - asteroida zostaje oznaczona jako nieaktywna,
    - powstaje animacja eksplozji,
    - odtwarzany jest dźwięk eksplozji.

    Ważne:
    Nie usuwamy elementów z listy w trakcie pętli.
    Najpierw tylko ustawiamy alive = False.
    Czyszczenie listy odbywa się później przez list comprehension.
    """
    for bullet in bullets:
        if not bullet.alive:
            continue

        for asteroid in asteroids:
            if not asteroid.alive:
                continue

            hit = circle_collision(
                bullet.x,
                bullet.y,
                bullet.radius,
                asteroid.x,
                asteroid.y,
                asteroid.radius,
            )

            if hit:
                bullet.alive = False
                asteroid.alive = False

                explosions.append(
                    Explosion(
                        asteroid.x,
                        asteroid.y,
                        asteroid.radius * 1.8,
                    )
                )

                rl.play_sound(explode_sound)

                # Jeden pocisk powinien zniszczyć tylko jedną asteroidę.
                break


def check_ship_asteroid_collision(ship: Ship, asteroids: list, explosions: list, explode_sound):
    """
    Zadanie dodatkowe:
    sprawdza kolizję statku z asteroidą.

    Statek jest traktowany jak koło.
    Po kolizji:
    - pojawia się eksplozja w miejscu statku,
    - odtwarzany jest dźwięk,
    - statek wraca na środek ekranu.

    Asteroida nie jest tutaj niszczona,
    ponieważ zadanie dodatkowe mówi tylko o resecie statku.
    """
    for asteroid in asteroids:
        if not asteroid.alive:
            continue

        hit = circle_collision(
            ship.x,
            ship.y,
            ship.radius,
            asteroid.x,
            asteroid.y,
            asteroid.radius,
        )

        if hit:
            explosions.append(
                Explosion(
                    ship.x,
                    ship.y,
                    ship.radius * 2.2,
                )
            )

            rl.play_sound(explode_sound)
            reset_ship(ship)

            # Po jednej kolizji kończymy sprawdzanie w tej klatce.
            break


def remove_dead_objects(bullets: list, asteroids: list, explosions: list):
    """
    Usuwa nieaktywne obiekty z list.

    To jest bezpieczniejsze niż remove() wewnątrz pętli for.

    Przykład złego podejścia:
    for b in bullets:
        bullets.remove(b)

    Problem:
    Usuwanie elementu podczas iteracji może spowodować,
    że Python pominie niektóre elementy albo zachowanie będzie trudne do kontroli.

    Lepsze podejście:
    tworzymy nową listę tylko z obiektów, które nadal żyją.
    """
    bullets = [b for b in bullets if b.alive]
    asteroids = [a for a in asteroids if a.alive]
    explosions = [e for e in explosions if e.alive]

    return bullets, asteroids, explosions


def draw_game(ship: Ship, asteroids: list, bullets: list, explosions: list, stars_texture, procedural_stars):
    """
    Rysuje całą scenę gry.

    Wszystkie obiekty mają własne metody draw(),
    więc main.py tylko ustala kolejność rysowania.
    """
    rl.begin_drawing()
    rl.clear_background(rl.Color(*BG_COLOR))

    draw_background(stars_texture, procedural_stars)

    ship.draw()

    for asteroid in asteroids:
        asteroid.draw()

    for bullet in bullets:
        bullet.draw()

    for explosion in explosions:
        explosion.draw()

    draw_hud(asteroids, bullets)

    rl.end_drawing()


def draw_hud(asteroids: list, bullets: list):
    """
    Rysuje prosty interfejs tekstowy.

    HUD pokazuje:
    - sterowanie,
    - liczbę asteroid,
    - liczbę pocisków,
    - opis funkcji z laboratorium.
    """
    rl.draw_text("ARROWS: move ship", 20, 20, 20, rl.RAYWHITE)
    rl.draw_text("SPACE: shoot", 20, 45, 20, rl.RAYWHITE)

    rl.draw_text(
        f"Asteroids: {len(asteroids)}  Bullets: {len(bullets)}/{BULLET_LIMIT}",
        20,
        70,
        20,
        rl.GRAY,
    )

    rl.draw_text(
        "Lab 07: TTL bullets + sounds + circle collisions + explosions",
        20,
        SCREEN_H - 35,
        20,
        rl.GRAY,
    )


def unload_resources(stars_texture, shoot_sound, explode_sound):
    """
    Zwalnia zasoby po zakończeniu programu.

    To jest ważne w Raylib, bo zasoby takie jak:
    - tekstury,
    - dźwięki,
    - urządzenie audio,
    nie powinny być zostawione bez zwolnienia.

    Kolejność:
    1. unload_texture,
    2. unload_sound,
    3. close_audio_device,
    4. close_window.
    """
    if stars_texture is not None:
        rl.unload_texture(stars_texture)

    rl.unload_sound(shoot_sound)
    rl.unload_sound(explode_sound)

    rl.close_audio_device()
    rl.close_window()


def main():
    """
    Główna funkcja programu.

    Schemat programu:
    1. Inicjalizacja okna.
    2. Inicjalizacja audio.
    3. Załadowanie zasobów.
    4. Utworzenie obiektów gry.
    5. Główna pętla:
       - input,
       - update,
       - collisions,
       - cleanup,
       - draw.
    6. Zwolnienie zasobów.
    """
    rl.init_window(SCREEN_W, SCREEN_H, "Lab 07 - Asteroids: bullets, collisions, explosions")
    rl.init_audio_device()
    rl.set_target_fps(FPS)

    # Zasoby dźwiękowe ładujemy przed pętlą gry.
    # Nie wolno ładować ich w każdej klatce, bo to obciąża pamięć i procesor.
    shoot_sound = rl.load_sound(SHOOT_SOUND_PATH)
    explode_sound = rl.load_sound(EXPLODE_SOUND_PATH)

    # Tło może być teksturą albo proceduralnym polem gwiazd.
    stars_texture, procedural_stars = load_background()

    # Tworzenie obiektów startowych.
    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)
    asteroids = create_asteroids(ASTEROID_COUNT)

    bullets = []
    explosions = []

    # ========================================================
    # GŁÓWNA PĘTLA GRY
    # ========================================================
    while not rl.window_should_close():
        dt = rl.get_frame_time()

        # 1. Obsługa strzelania.
        handle_shooting(ship, bullets, shoot_sound)

        # 2. Aktualizacja ruchu obiektów.
        update_game_objects(dt, ship, asteroids, bullets, explosions)

        # 3. Kolizje pocisków z asteroidami.
        check_bullet_asteroid_collisions(
            bullets,
            asteroids,
            explosions,
            explode_sound,
        )

        # 4. Kolizja statku z asteroidą.
        check_ship_asteroid_collision(
            ship,
            asteroids,
            explosions,
            explode_sound,
        )

        # 5. Czyszczenie nieaktywnych obiektów.
        bullets, asteroids, explosions = remove_dead_objects(
            bullets,
            asteroids,
            explosions,
        )

        # 6. Jeśli wszystkie asteroidy zostały zniszczone,
        # tworzymy nową falę asteroid.
        if len(asteroids) == 0:
            asteroids = create_asteroids(ASTEROID_COUNT)

        # 7. Rysowanie całej sceny.
        draw_game(
            ship,
            asteroids,
            bullets,
            explosions,
            stars_texture,
            procedural_stars,
        )

    # Po wyjściu z pętli zwalniamy zasoby.
    unload_resources(stars_texture, shoot_sound, explode_sound)


if __name__ == "__main__":
    main()