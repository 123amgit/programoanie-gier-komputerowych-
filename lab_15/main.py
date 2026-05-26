# main.py
# Library Ghost - etap 1: pętla gry, ekran menu i globalna FSM.

import pyray as pr

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE
from game_state import GameState


def draw_centered_text(text: str, y: int, size: int, color) -> None:
    text_width = pr.measure_text(text, size)
    x = (SCREEN_WIDTH - text_width) // 2
    pr.draw_text(text, x, y, size, color)


def update_menu() -> GameState:
    if pr.is_key_pressed(pr.KEY_ENTER):
        return GameState.PLAYING
    return GameState.MENU


def draw_menu() -> None:
    pr.clear_background(pr.Color(18, 16, 28, 255))

    draw_centered_text("LIBRARY GHOST", 150, 42, pr.Color(230, 230, 255, 255))
    draw_centered_text("Autorska gra 2D w Raylib/Python", 220, 22, pr.Color(180, 180, 210, 255))
    draw_centered_text("ENTER - start", 300, 24, pr.Color(220, 220, 180, 255))
    draw_centered_text("ESC - wyjscie", 335, 20, pr.Color(160, 160, 180, 255))

    pr.draw_rectangle_lines(260, 120, 380, 280, pr.Color(100, 90, 130, 255))


def update_playing() -> GameState:
    # Tymczasowy ekran gry. W kolejnym commicie dodamy ruch ducha.
    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        return GameState.MENU
    return GameState.PLAYING


def draw_playing() -> None:
    pr.clear_background(pr.Color(24, 22, 34, 255))
    draw_centered_text("Etap gry - tutaj pojawi sie biblioteka", 250, 24, pr.RAYWHITE)
    draw_centered_text("BACKSPACE - powrot do menu", 290, 20, pr.GRAY)


def main() -> None:
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    pr.set_target_fps(FPS)

    state = GameState.MENU

    while not pr.window_should_close():
        if state == GameState.MENU:
            state = update_menu()
        elif state == GameState.PLAYING:
            state = update_playing()

        pr.begin_drawing()

        if state == GameState.MENU:
            draw_menu()
        elif state == GameState.PLAYING:
            draw_playing()
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
