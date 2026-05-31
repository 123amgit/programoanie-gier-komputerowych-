# main.py
# Library Ghost - etap 2: pętla gry, menu, FSM i ruch ducha.

import pyray as pr

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE
from game_state import GameState
from player import Player


def draw_centered_text(text: str, y: int, size: int, color) -> None:
    text_width = pr.measure_text(text, size)
    x = (SCREEN_WIDTH - text_width) // 2
    pr.draw_text(text, x, y, size, color)


def update_menu(player: Player) -> GameState:
    if pr.is_key_pressed(pr.KEY_ENTER):
        player.reset()
        return GameState.PLAYING

    return GameState.MENU


def draw_menu() -> None:
    pr.clear_background(pr.Color(18, 16, 28, 255))

    draw_centered_text("LIBRARY GHOST", 145, 42, pr.Color(230, 230, 255, 255))
    draw_centered_text("Autorska gra 2D w Raylib/Python", 215, 22, pr.Color(180, 180, 210, 255))
    draw_centered_text("ENTER - start", 295, 24, pr.Color(220, 220, 180, 255))
    draw_centered_text("ESC - wyjscie", 330, 20, pr.Color(160, 160, 180, 255))

    pr.draw_rectangle_lines(260, 115, 380, 285, pr.Color(100, 90, 130, 255))


def update_playing(player: Player) -> GameState:
    dt = pr.get_frame_time()
    player.update(dt)

    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        return GameState.MENU

    return GameState.PLAYING


def draw_library_background() -> None:
    pr.clear_background(pr.Color(24, 22, 34, 255))

    # Prosty zarys sali biblioteki jako tło.
    pr.draw_rectangle(40, 70, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 110, pr.Color(34, 30, 48, 255))
    pr.draw_rectangle_lines(40, 70, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 110, pr.Color(95, 85, 120, 255))

    # Tymczasowe dekoracje półek, jeszcze bez kolizji.
    for x in range(90, SCREEN_WIDTH - 130, 160):
        pr.draw_rectangle(x, 110, 95, 28, pr.Color(80, 55, 45, 255))
        pr.draw_rectangle(x, 455, 95, 28, pr.Color(80, 55, 45, 255))

    for y in range(170, 420, 95):
        pr.draw_rectangle(90, y, 28, 80, pr.Color(80, 55, 45, 255))
        pr.draw_rectangle(SCREEN_WIDTH - 120, y, 28, 80, pr.Color(80, 55, 45, 255))


def draw_hud(player: Player) -> None:
    pr.draw_rectangle(0, 0, SCREEN_WIDTH, 45, pr.Color(14, 12, 22, 240))

    pr.draw_text("Library Ghost - etap ruchu gracza", 20, 13, 18, pr.RAYWHITE)
    pr.draw_text(f"Energia: {int(player.energy)}", 650, 13, 18, pr.Color(210, 220, 255, 255))
    pr.draw_text("WASD/strzalki - ruch | BACKSPACE - menu", 20, SCREEN_HEIGHT - 28, 16, pr.GRAY)


def draw_playing(player: Player) -> None:
    draw_library_background()
    player.draw()
    draw_hud(player)


def main() -> None:
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    pr.set_target_fps(FPS)

    state = GameState.MENU
    player = Player()

    while not pr.window_should_close():
        if state == GameState.MENU:
            state = update_menu(player)
        elif state == GameState.PLAYING:
            state = update_playing(player)

        pr.begin_drawing()

        if state == GameState.MENU:
            draw_menu()
        elif state == GameState.PLAYING:
            draw_playing(player)
        elif state == GameState.GAME_OVER:
            pr.clear_background(pr.BLACK)
            draw_centered_text("GAME OVER", 260, 36, pr.RED)
        elif state == GameState.WIN:
            pr.clear_background(pr.BLACK)
            draw_centered_text("YOU WIN", 260, 36, pr.GREEN)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
