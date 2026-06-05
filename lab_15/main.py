# main.py
# Library Ghost - finalna wersja: strony, półka, strażnicy, światło,
# tryb przezroczystości, cząsteczki i opcjonalne dźwięki.

import pyray as pr

from audio_manager import AudioManager
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WINDOW_TITLE,
    PAGES_TO_WIN,
    FLASHLIGHT_DAMAGE_PER_SECOND,
    TRANSPARENT_FLASHLIGHT_MULTIPLIER,
)
from game_state import GameState
from guard import Guard
from obstacle import Obstacle
from page import Page
from particle import create_sparkles, update_particles, draw_particles
from player import Player
from shelf import Shelf


def draw_centered_text(text: str, y: int, size: int, color) -> None:
    text_width = pr.measure_text(text, size)
    x = (SCREEN_WIDTH - text_width) // 2
    pr.draw_text(text, x, y, size, color)


def create_obstacles() -> list[Obstacle]:
    obstacles = []

    for x in range(95, SCREEN_WIDTH - 180, 165):
        obstacles.append(Obstacle(x, 145, 95, 28, "top_shelf"))

    for x in range(95, SCREEN_WIDTH - 180, 165):
        obstacles.append(Obstacle(x, 455, 95, 28, "bottom_shelf"))

    for y in range(200, 420, 95):
        obstacles.append(Obstacle(95, y, 28, 80, "left_shelf"))
        obstacles.append(Obstacle(SCREEN_WIDTH - 125, y, 28, 80, "right_shelf"))

    obstacles.append(Obstacle(300, 250, 110, 28, "middle_shelf"))
    obstacles.append(Obstacle(500, 330, 110, 28, "middle_shelf"))

    return obstacles


def create_pages() -> list[Page]:
    return [
        Page(170, 180),
        Page(720, 180),
        Page(235, 390),
        Page(680, 420),
        Page(450, 210),
        Page(450, 500),
    ]


def create_guards() -> list[Guard]:
    return [
        Guard(220, 315, "x", 160, 360),
        Guard(650, 290, "y", 190, 430),
    ]


def reset_game(player: Player, pages: list[Page], guards: list[Guard], particles: list) -> tuple[int, bool]:
    player.reset()
    particles.clear()

    for page in pages:
        page.collected = False
        page.delivered = False

    for guard in guards:
        guard.x = guard.start_x
        guard.y = guard.start_y
        guard.direction = 1

    return 0, False


def update_menu(
    player: Player,
    pages: list[Page],
    guards: list[Guard],
    particles: list,
) -> tuple[GameState, int, bool]:
    if pr.is_key_pressed(pr.KEY_ENTER):
        delivered_pages, carrying_page = reset_game(player, pages, guards, particles)
        return GameState.PLAYING, delivered_pages, carrying_page

    return GameState.MENU, 0, False


def draw_menu() -> None:
    pr.clear_background(pr.Color(18, 16, 28, 255))

    draw_centered_text("LIBRARY GHOST", 140, 42, pr.Color(230, 230, 255, 255))
    draw_centered_text("Autorska gra 2D w Raylib/Python", 210, 22, pr.Color(180, 180, 210, 255))
    draw_centered_text("ENTER - start", 285, 24, pr.Color(220, 220, 180, 255))
    draw_centered_text("WASD/strzalki - ruch | SPACE - przezroczystosc", 325, 18, pr.Color(170, 190, 225, 255))
    draw_centered_text("ESC - wyjscie", 360, 18, pr.Color(160, 160, 180, 255))

    pr.draw_rectangle_lines(235, 110, 430, 310, pr.Color(100, 90, 130, 255))


def update_playing(
    player: Player,
    obstacles: list[Obstacle],
    pages: list[Page],
    shelf: Shelf,
    guards: list[Guard],
    delivered_pages: int,
    carrying_page: bool,
    particles: list,
    audio: AudioManager,
) -> tuple[GameState, int, bool]:
    dt = pr.get_frame_time()
    update_particles(particles, dt)

    old_x = player.x
    old_y = player.y

    player.update(dt)

    # Normalnie duch nie przechodzi przez półki.
    # W trybie przezroczystości kolizje z półkami są pomijane.
    if not player.is_transparent:
        for obstacle in obstacles:
            if obstacle.collides_with_circle(player.x, player.y, player.radius):
                player.x = old_x
                player.y = old_y
                break

    player_in_light = False

    for guard in guards:
        guard.update(dt)

        if guard.sees_player(player):
            player_in_light = True

    if player_in_light:
        damage = FLASHLIGHT_DAMAGE_PER_SECOND

        # Przezroczystość trochę zmniejsza obrażenia od światła,
        # ale nadal zużywa własną energię, więc nie jest darmową ochroną.
        if player.is_transparent:
            damage *= TRANSPARENT_FLASHLIGHT_MULTIPLIER

        player.energy -= damage * dt

    if player.energy <= 0:
        player.energy = 0
        audio.play("hit")
        return GameState.GAME_OVER, delivered_pages, carrying_page

    # Zbieranie jednej strony naraz.
    if not carrying_page:
        for page in pages:
            if page.can_be_picked() and page.collides_with_player(player):
                page.collected = True
                carrying_page = True
                particles.extend(
                    create_sparkles(
                        page.x,
                        page.y,
                        14,
                        pr.Color(235, 226, 185, 255),
                    )
                )
                audio.play("pickup")
                break

    # Oddawanie strony na magiczną półkę.
    if carrying_page and shelf.collides_with_player(player):
        for page in pages:
            if page.collected and not page.delivered:
                page.delivered = True
                page.collected = False
                delivered_pages += 1
                carrying_page = False

                particles.extend(
                    create_sparkles(
                        shelf.rect.x + shelf.rect.width / 2,
                        shelf.rect.y + shelf.rect.height / 2,
                        20,
                        pr.Color(190, 150, 255, 255),
                    )
                )
                audio.play("deliver")
                break

    if delivered_pages >= PAGES_TO_WIN:
        audio.play("win")
        return GameState.WIN, delivered_pages, carrying_page

    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        return GameState.MENU, delivered_pages, carrying_page

    return GameState.PLAYING, delivered_pages, carrying_page


def update_win(
    player: Player,
    pages: list[Page],
    guards: list[Guard],
    particles: list,
) -> tuple[GameState, int, bool]:
    if pr.is_key_pressed(pr.KEY_ENTER):
        delivered_pages, carrying_page = reset_game(player, pages, guards, particles)
        return GameState.PLAYING, delivered_pages, carrying_page

    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        return GameState.MENU, 0, False

    return GameState.WIN, PAGES_TO_WIN, False


def update_game_over(
    player: Player,
    pages: list[Page],
    guards: list[Guard],
    particles: list,
) -> tuple[GameState, int, bool]:
    if pr.is_key_pressed(pr.KEY_ENTER):
        delivered_pages, carrying_page = reset_game(player, pages, guards, particles)
        return GameState.PLAYING, delivered_pages, carrying_page

    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        return GameState.MENU, 0, False

    return GameState.GAME_OVER, 0, False


def draw_library_background() -> None:
    pr.clear_background(pr.Color(24, 22, 34, 255))

    pr.draw_rectangle(40, 70, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 110, pr.Color(34, 30, 48, 255))
    pr.draw_rectangle_lines(40, 70, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 110, pr.Color(95, 85, 120, 255))

    for x in range(40, SCREEN_WIDTH - 40, 40):
        pr.draw_line(x, 70, x, SCREEN_HEIGHT - 40, pr.Color(40, 36, 55, 255))

    for y in range(70, SCREEN_HEIGHT - 40, 40):
        pr.draw_line(40, y, SCREEN_WIDTH - 40, y, pr.Color(40, 36, 55, 255))


def draw_carried_page_icon(player: Player, carrying_page: bool) -> None:
    if not carrying_page:
        return

    x = int(player.x + 18)
    y = int(player.y - 24)

    pr.draw_rectangle(x, y, 13, 17, pr.Color(235, 226, 185, 255))
    pr.draw_rectangle_lines(x, y, 13, 17, pr.Color(130, 115, 80, 255))


def draw_hud(player: Player, delivered_pages: int, carrying_page: bool, player_in_light: bool) -> None:
    pr.draw_rectangle(0, 0, SCREEN_WIDTH, 48, pr.Color(14, 12, 22, 240))

    pr.draw_text("Library Ghost", 20, 14, 18, pr.RAYWHITE)
    pr.draw_text(f"Strony: {delivered_pages}/{PAGES_TO_WIN}", 370, 14, 18, pr.Color(235, 226, 185, 255))

    energy_color = pr.Color(210, 220, 255, 255)
    if player.energy < 35:
        energy_color = pr.Color(255, 120, 120, 255)

    pr.draw_text(f"Energia: {int(player.energy)}", 535, 14, 18, energy_color)

    if player.is_transparent:
        pr.draw_text("TRYB PRZEZROCZYSTOSCI", 700, 14, 18, pr.Color(130, 210, 255, 255))
    else:
        pr.draw_text("SPACE - przezroczystosc", 685, 14, 18, pr.GRAY)

    if player_in_light:
        pr.draw_text("UWAGA: duch jest w swietle latarki!", 20, SCREEN_HEIGHT - 28, 16, pr.Color(255, 210, 120, 255))
    elif carrying_page:
        pr.draw_text("Niesiesz strone - wroc do magicznej polki", 20, SCREEN_HEIGHT - 28, 16, pr.Color(235, 226, 185, 255))
    else:
        pr.draw_text("Zbierz strone, unikaj swiatla, SPACE pozwala przechodzic przez polki", 20, SCREEN_HEIGHT - 28, 16, pr.GRAY)


def is_player_in_any_light(player: Player, guards: list[Guard]) -> bool:
    for guard in guards:
        if guard.sees_player(player):
            return True

    return False


def draw_playing(
    player: Player,
    obstacles: list[Obstacle],
    pages: list[Page],
    shelf: Shelf,
    guards: list[Guard],
    delivered_pages: int,
    carrying_page: bool,
    particles: list,
) -> None:
    draw_library_background()

    shelf.draw()

    for obstacle in obstacles:
        obstacle.draw()

    for page in pages:
        page.draw()

    for guard in guards:
        guard.draw()

    draw_particles(particles)

    player.draw()
    draw_carried_page_icon(player, carrying_page)

    player_in_light = is_player_in_any_light(player, guards)
    draw_hud(player, delivered_pages, carrying_page, player_in_light)


def draw_win() -> None:
    pr.clear_background(pr.Color(18, 16, 28, 255))

    draw_centered_text("YOU WIN", 190, 46, pr.Color(180, 255, 180, 255))
    draw_centered_text("Duch odniosl zagubione strony do magicznej polki.", 260, 22, pr.RAYWHITE)
    draw_centered_text("ENTER - zagraj ponownie", 325, 22, pr.Color(220, 220, 180, 255))
    draw_centered_text("BACKSPACE - menu", 360, 20, pr.GRAY)


def draw_game_over() -> None:
    pr.clear_background(pr.Color(18, 12, 22, 255))

    draw_centered_text("GAME OVER", 190, 46, pr.Color(255, 120, 120, 255))
    draw_centered_text("Duch stracil cala energie.", 260, 22, pr.RAYWHITE)
    draw_centered_text("ENTER - sproboj ponownie", 325, 22, pr.Color(220, 220, 180, 255))
    draw_centered_text("BACKSPACE - menu", 360, 20, pr.GRAY)


def main() -> None:
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    pr.set_target_fps(FPS)

    state = GameState.MENU
    player = Player()
    obstacles = create_obstacles()
    pages = create_pages()
    shelf = Shelf()
    guards = create_guards()
    particles = []

    audio = AudioManager()
    audio.load()

    delivered_pages = 0
    carrying_page = False

    while not pr.window_should_close():
        if state == GameState.MENU:
            state, delivered_pages, carrying_page = update_menu(player, pages, guards, particles)
        elif state == GameState.PLAYING:
            state, delivered_pages, carrying_page = update_playing(
                player,
                obstacles,
                pages,
                shelf,
                guards,
                delivered_pages,
                carrying_page,
                particles,
                audio,
            )
        elif state == GameState.WIN:
            state, delivered_pages, carrying_page = update_win(player, pages, guards, particles)
        elif state == GameState.GAME_OVER:
            state, delivered_pages, carrying_page = update_game_over(player, pages, guards, particles)

        pr.begin_drawing()

        if state == GameState.MENU:
            draw_menu()
        elif state == GameState.PLAYING:
            draw_playing(
                player,
                obstacles,
                pages,
                shelf,
                guards,
                delivered_pages,
                carrying_page,
                particles,
            )
        elif state == GameState.GAME_OVER:
            draw_game_over()
        elif state == GameState.WIN:
            draw_win()

        pr.end_drawing()

    audio.unload()
    pr.close_window()


if __name__ == "__main__":
    main()
