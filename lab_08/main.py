"""
main.py
=======

Laboratorium 08: FSM, podział asteroid, punktacja i koniec gry.

Ten plik jest sercem programu, ale po refaktoryzacji nie powinien być
jednym wielkim kłębowiskiem ifów. Dlatego zastosowano:
- enum.Enum do stanów gry,
- osobne funkcje update_* i draw_* dla każdego stanu,
- funkcję init_game() do resetowania rozgrywki,
- helpery do zasobów i czyszczenia list.

Stany gry:
- MENU      : ekran startowy,
- GAME      : właściwa rozgrywka,
- GAME_OVER : ekran końcowy po zwycięstwie lub śmierci.
"""

import os
import random
from enum import Enum, auto

import pyray as rl

from asteroid import Asteroid
from bullet import Bullet
from config import (
    ASSETS_DIR,
    BG_COLOR,
    BULLET_LIMIT,
    EXPLODE_SOUND_FILE,
    FPS,
    SAFE_SPAWN_DISTANCE,
    SCORE_BY_LEVEL,
    SCORES_FILE,
    SCREEN_H,
    SCREEN_W,
    SHIP_RADIUS,
    SHOOT_SOUND_FILE,
    START_ASTEROID_COUNT,
    ASTEROID_START_LEVEL,
    STARS_TEXTURE_FILE,
)
from explosion import Explosion
from ship import Ship
from utils import circle_collision, keep_alive


# ------------------------------------------------------------
# ENUMY STANÓW
# ------------------------------------------------------------

class GameState(Enum):
    """
    Maszyna stanów gry.

    Enum jest bezpieczniejszy niż stringi.
    Przy stringach łatwo napisać "gaem" zamiast "game"
    i Python nie zauważy błędu od razu.
    Przy enum IDE zwykle podpowiada możliwe wartości.
    """
    MENU = auto()
    GAME = auto()
    GAME_OVER = auto()


class EndReason(Enum):
    """
    Powód zakończenia gry.

    Ekran końcowy pokazuje inny tekst dla zwycięstwa i dla śmierci.
    """
    NONE = auto()
    WIN = auto()
    DEATH = auto()


# ------------------------------------------------------------
# ŚCIEŻKI DO ZASOBÓW
# ------------------------------------------------------------

SHOOT_SOUND_PATH = os.path.join(ASSETS_DIR, SHOOT_SOUND_FILE)
EXPLODE_SOUND_PATH = os.path.join(ASSETS_DIR, EXPLODE_SOUND_FILE)
STARS_PATH = os.path.join(ASSETS_DIR, STARS_TEXTURE_FILE)


# ------------------------------------------------------------
# FUNKCJE PLIKOWE DLA NAJLEPSZEGO WYNIKU
# ------------------------------------------------------------

def load_best_score() -> int:
    """
    Wczytuje najlepszy wynik z pliku scores.txt.

    Jeśli pliku nie ma, zwracamy 0.
    Dzięki try/except program działa także przy pierwszym uruchomieniu.
    """
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            text = file.read().strip()
            return int(text)
    except (FileNotFoundError, ValueError):
        return 0


def save_best_score(best: int) -> None:
    """
    Zapisuje najlepszy wynik do pliku.

    To jest zadanie dodatkowe, ale bardzo proste i praktyczne.
    """
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        file.write(str(best))


# ------------------------------------------------------------
# TWORZENIE OBIEKTÓW GRY
# ------------------------------------------------------------

def random_position_far_from_center() -> tuple[float, float]:
    """
    Losuje pozycję asteroidy z dala od środka ekranu.

    Na środku startuje statek, więc bez tego asteroida mogłaby
    pojawić się od razu na graczu i natychmiast zakończyć grę.
    """
    center_x = SCREEN_W / 2
    center_y = SCREEN_H / 2

    while True:
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)

        if not circle_collision(x, y, SAFE_SPAWN_DISTANCE, center_x, center_y, SHIP_RADIUS):
            return x, y


def create_asteroids(count: int) -> list[Asteroid]:
    """
    Tworzy początkową listę dużych asteroid.

    W Lab 08 nie przekazujemy promienia do Asteroid.
    Przekazujemy level, a klasa sama dobiera promień i prędkość.
    """
    asteroids = []

    for _ in range(count):
        x, y = random_position_far_from_center()
        asteroids.append(Asteroid(x, y, ASTEROID_START_LEVEL))

    return asteroids


def create_star_field(count: int = 160) -> list[tuple[int, int, int]]:
    """
    Tworzy awaryjne proceduralne tło gwiazd.

    Jeśli stars.png nie istnieje, gra nadal będzie miała tło.
    """
    stars = []

    for _ in range(count):
        x = random.randint(0, SCREEN_W - 1)
        y = random.randint(0, SCREEN_H - 1)
        radius = random.choice([1, 1, 1, 2])
        stars.append((x, y, radius))

    return stars


def init_game():
    """
    Resetuje rozgrywkę do stanu początkowego.

    Funkcja jest wywoływana przy przejściu:
    MENU -> GAME.

    Zwraca wszystkie obiekty potrzebne do gry.
    """
    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)
    asteroids = create_asteroids(START_ASTEROID_COUNT)
    bullets = []
    explosions = []
    score = 0
    end_reason = EndReason.NONE

    return ship, asteroids, bullets, explosions, score, end_reason


# ------------------------------------------------------------
# ZASOBY: DŹWIĘKI I TŁO
# ------------------------------------------------------------

def load_background():
    """
    Ładuje tło jako teksturę albo tworzy tło proceduralne.

    Teksturę należy ładować przed pętlą gry, nie w każdej klatce.
    """
    if os.path.exists(STARS_PATH):
        return rl.load_texture(STARS_PATH), None

    return None, create_star_field()


def draw_background(stars_texture, procedural_stars) -> None:
    """
    Rysuje tło jako pierwszą warstwę sceny.
    """
    if stars_texture is not None:
        rl.draw_texture(stars_texture, 0, 0, rl.WHITE)
        return

    for x, y, radius in procedural_stars:
        rl.draw_circle(x, y, radius, rl.Color(190, 190, 210, 255))


def unload_resources(stars_texture, shoot_sound, explode_sound) -> None:
    """
    Zwalnia zasoby przed zamknięciem programu.

    To ważne przy Raylib, bo dźwięki i tekstury nie powinny zostać
    pozostawione bez unload.
    """
    if stars_texture is not None:
        rl.unload_texture(stars_texture)

    rl.unload_sound(shoot_sound)
    rl.unload_sound(explode_sound)
    rl.close_audio_device()
    rl.close_window()


# ------------------------------------------------------------
# UPDATE: STANY GRY
# ------------------------------------------------------------

def update_menu():
    """
    Aktualizacja menu.

    ENTER rozpoczyna nową grę.
    ESC zamyka okno, bo Raylib obsługuje to domyślnie.
    """
    if rl.is_key_pressed(rl.KEY_ENTER):
        return GameState.GAME

    return GameState.MENU


def update_game(ship, asteroids, bullets, explosions, score, shoot_sound, explode_sound):
    """
    Aktualizuje właściwą rozgrywkę.

    Kolejność:
    1. strzelanie,
    2. ruch obiektów,
    3. kolizje,
    4. czyszczenie list,
    5. sprawdzenie końca gry.
    """
    dt = rl.get_frame_time()

    handle_shooting(ship, bullets, shoot_sound)
    update_game_objects(dt, ship, asteroids, bullets, explosions)

    score = check_bullet_asteroid_collisions(
        bullets,
        asteroids,
        explosions,
        score,
        explode_sound,
    )

    end_reason = check_ship_asteroid_collision(
        ship,
        asteroids,
        explosions,
        explode_sound,
    )

    bullets = keep_alive(bullets)
    asteroids = keep_alive(asteroids)
    explosions = keep_alive(explosions)

    # Warunek zwycięstwa z zadania 5:
    # jeśli po czyszczeniu nie ma żadnej asteroidy, gra kończy się wygraną.
    if end_reason == EndReason.NONE and len(asteroids) == 0:
        end_reason = EndReason.WIN

    if end_reason != EndReason.NONE:
        return GameState.GAME_OVER, ship, asteroids, bullets, explosions, score, end_reason

    return GameState.GAME, ship, asteroids, bullets, explosions, score, EndReason.NONE


def update_game_over(score: int, best: int) -> tuple[GameState, int]:
    """
    Aktualizacja ekranu końcowego.

    ENTER wraca do menu.
    Przy powrocie aktualizujemy najlepszy wynik sesji i zapis do pliku.
    """
    if rl.is_key_pressed(rl.KEY_ENTER):
        if score > best:
            best = score
            save_best_score(best)

        return GameState.MENU, best

    return GameState.GAME_OVER, best


# ------------------------------------------------------------
# LOGIKA GRY
# ------------------------------------------------------------

def handle_shooting(ship: Ship, bullets: list[Bullet], shoot_sound) -> None:
    """
    Obsługuje strzelanie.

    is_key_pressed oznacza jeden strzał na pojedyncze naciśnięcie.
    BULLET_LIMIT ogranicza spamowanie pociskami.
    """
    if not rl.is_key_pressed(rl.KEY_SPACE):
        return

    if len(bullets) >= BULLET_LIMIT:
        return

    nose_x, nose_y = ship.get_nose_position(offset=8.0)
    bullets.append(Bullet(nose_x, nose_y, ship.angle_deg))
    rl.play_sound(shoot_sound)


def update_game_objects(dt: float, ship: Ship, asteroids: list[Asteroid], bullets: list[Bullet], explosions: list[Explosion]) -> None:
    """
    Aktualizuje wszystkie aktywne obiekty gry.
    """
    ship.update(dt)
    ship.wrap()

    for asteroid in asteroids:
        asteroid.update(dt)

    for bullet in bullets:
        bullet.update(dt)

    for explosion in explosions:
        explosion.update(dt)


def check_bullet_asteroid_collisions(
    bullets: list[Bullet],
    asteroids: list[Asteroid],
    explosions: list[Explosion],
    score: int,
    explode_sound,
) -> int:
    """
    Sprawdza trafienia pocisków w asteroidy.

    Po trafieniu:
    - pocisk znika,
    - asteroida znika,
    - wynik rośnie zgodnie z level,
    - split() dodaje mniejsze asteroidy,
    - pojawia się eksplozja.
    """
    new_asteroids = []

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

            if not hit:
                continue

            bullet.alive = False
            asteroid.alive = False

            score += SCORE_BY_LEVEL[asteroid.level]

            new_asteroids.extend(asteroid.split())
            explosions.append(Explosion(asteroid.x, asteroid.y, asteroid.radius * 1.8))

            rl.play_sound(explode_sound)

            # Jeden pocisk niszczy tylko jedną asteroidę.
            break

    asteroids.extend(new_asteroids)
    return score


def check_ship_asteroid_collision(ship: Ship, asteroids: list[Asteroid], explosions: list[Explosion], explode_sound) -> EndReason:
    """
    Sprawdza śmierć gracza.

    W Lab 07 kolizja resetowała statek.
    W Lab 08 jest to warunek końca gry.
    """
    for asteroid in asteroids:
        if not asteroid.alive:
            continue

        if circle_collision(ship.x, ship.y, ship.radius, asteroid.x, asteroid.y, asteroid.radius):
            ship.alive = False
            explosions.append(Explosion(ship.x, ship.y, ship.radius * 2.5))
            rl.play_sound(explode_sound)
            return EndReason.DEATH

    return EndReason.NONE


# ------------------------------------------------------------
# DRAW: STANY GRY
# ------------------------------------------------------------

def draw_menu(stars_texture, procedural_stars, best: int) -> None:
    """
    Rysuje menu startowe.
    """
    rl.begin_drawing()
    rl.clear_background(rl.Color(*BG_COLOR))

    draw_background(stars_texture, procedural_stars)

    draw_center_text("ASTEROIDS - LAB 08", SCREEN_H // 2 - 90, 42, rl.RAYWHITE)
    draw_center_text("FSM + punktacja + podzial asteroid", SCREEN_H // 2 - 40, 22, rl.LIGHTGRAY)
    draw_center_text("ENTER - start gry", SCREEN_H // 2 + 15, 24, rl.YELLOW)
    draw_center_text("Strzalki - ruch, SPACE - strzal", SCREEN_H // 2 + 55, 20, rl.GRAY)
    draw_center_text(f"Najlepszy wynik: {best}", SCREEN_H // 2 + 95, 20, rl.RAYWHITE)

    rl.end_drawing()


def draw_game(ship, asteroids, bullets, explosions, stars_texture, procedural_stars, score: int, best: int) -> None:
    """
    Rysuje główny ekran gry.
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

    draw_hud(score, best, asteroids, bullets)

    rl.end_drawing()


def draw_game_over(stars_texture, procedural_stars, score: int, best: int, end_reason: EndReason) -> None:
    """
    Rysuje ekran końcowy.
    """
    rl.begin_drawing()
    rl.clear_background(rl.Color(*BG_COLOR))

    draw_background(stars_texture, procedural_stars)

    if end_reason == EndReason.WIN:
        title = "ZWYCIESTWO"
        subtitle = "Wszystkie asteroidy zostaly zniszczone."
        color = rl.YELLOW
    else:
        title = "GAME OVER"
        subtitle = "Statek zderzyl sie z asteroida."
        color = rl.RED

    shown_best = max(best, score)

    draw_center_text(title, SCREEN_H // 2 - 95, 44, color)
    draw_center_text(subtitle, SCREEN_H // 2 - 42, 22, rl.RAYWHITE)
    draw_center_text(f"Wynik: {score}", SCREEN_H // 2 + 5, 24, rl.YELLOW)
    draw_center_text(f"Najlepszy wynik: {shown_best}", SCREEN_H // 2 + 40, 22, rl.LIGHTGRAY)
    draw_center_text("ENTER - powrot do menu", SCREEN_H // 2 + 95, 22, rl.GRAY)

    rl.end_drawing()


def draw_hud(score: int, best: int, asteroids: list[Asteroid], bullets: list[Bullet]) -> None:
    """
    Rysuje HUD podczas gry.
    """
    rl.draw_text(f"Wynik: {score}", 20, 20, 24, rl.RAYWHITE)
    rl.draw_text(f"Best: {max(best, score)}", 20, 50, 20, rl.LIGHTGRAY)
    rl.draw_text(f"Asteroidy: {len(asteroids)}", 20, 78, 20, rl.GRAY)
    rl.draw_text(f"Pociski: {len(bullets)}/{BULLET_LIMIT}", 20, 104, 20, rl.GRAY)
    rl.draw_text("ENTER w menu | SPACE strzal | Strzalki ruch", 20, SCREEN_H - 35, 20, rl.GRAY)


def draw_center_text(text: str, y: int, font_size: int, color) -> None:
    """
    Rysuje tekst wyśrodkowany poziomo.

    Używamy measure_text, żeby obliczyć szerokość napisu.
    """
    text_width = rl.measure_text(text, font_size)
    x = int((SCREEN_W - text_width) / 2)
    rl.draw_text(text, x, y, font_size, color)


# ------------------------------------------------------------
# GŁÓWNY PROGRAM
# ------------------------------------------------------------

def main() -> None:
    """
    Główna funkcja programu.

    Tutaj powstaje okno, audio, zasoby oraz pętla FSM.
    """
    rl.init_window(SCREEN_W, SCREEN_H, "Lab 08 - Asteroids FSM")
    rl.init_audio_device()
    rl.set_target_fps(FPS)

    shoot_sound = rl.load_sound(SHOOT_SOUND_PATH)
    explode_sound = rl.load_sound(EXPLODE_SOUND_PATH)
    stars_texture, procedural_stars = load_background()

    best = load_best_score()
    state = GameState.MENU

    # Zmienne gry tworzymy od razu, żeby istniały przed pierwszym startem.
    ship, asteroids, bullets, explosions, score, end_reason = init_game()

    while not rl.window_should_close():
        if state == GameState.MENU:
            new_state = update_menu()

            if new_state == GameState.GAME:
                ship, asteroids, bullets, explosions, score, end_reason = init_game()

            state = new_state
            draw_menu(stars_texture, procedural_stars, best)

        elif state == GameState.GAME:
            state, ship, asteroids, bullets, explosions, score, end_reason = update_game(
                ship,
                asteroids,
                bullets,
                explosions,
                score,
                shoot_sound,
                explode_sound,
            )

            draw_game(
                ship,
                asteroids,
                bullets,
                explosions,
                stars_texture,
                procedural_stars,
                score,
                best,
            )

        elif state == GameState.GAME_OVER:
            state, best = update_game_over(score, best)
            draw_game_over(stars_texture, procedural_stars, score, best, end_reason)

    # Przy zamknięciu okna także zapisz najlepszy wynik,
    # żeby nie zależeć wyłącznie od ENTER na ekranie końcowym.
    if score > best:
        best = score
        save_best_score(best)

    unload_resources(stars_texture, shoot_sound, explode_sound)


if __name__ == "__main__":
    main()
