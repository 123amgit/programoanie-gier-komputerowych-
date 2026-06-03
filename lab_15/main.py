# main.py
# Library Ghost - etap 3: pętla gry, menu, FSM, ruch ducha i kolizje z przeszkodami.

import pyray as pr

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE
from game_state import GameState
from obstacle import Obstacle
from player import Player


def draw_centered_text(text: str, y: int, size: int, color) -> None:
    text_width = pr.measure_text(text, size)
    x = (SCREEN_WIDTH - text_width) // 2
    pr.draw_text(text, x, y, size, color)


def create_obstacles() -> list[Obstacle]:
    obstacles = []

    # Górny rząd poziomych półek.
    for x in range(95, SCREEN_WIDTH - 180, 165):
        obstacles.append(Obstacle(x, 115, 95, 28, "top_shelf"))

    # Dolny rząd poziomych półek.
    for x in range(95, SCREEN_WIDTH - 180, 165):
        obstacles.append(Obstacle(x, 455, 95, 28, "bottom_shelf"))

    # Lewy i prawy rząd pionowych półek.
    for y in range(175, 420, 95):
        obstacles.append(Obstacle(95, y, 28, 80, "left_shelf"))
        obstacles.append(Obstacle(SCREEN_WIDTH - 125, y, 28, 80, "right_shelf"))

    # Dwie środkowe półki, żeby mapa nie była pusta.
    obstacles.append(Obstacle(300, 250, 110, 28, "middle_shelf"))
    obstacles.append(Obstacle(500, 330, 110, 28, "middle_shelf"))

    return obstacles


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


def update_playing(player: Player, obstacles: list[Obstacle]) -> GameState:
    dt = pr.get_frame_time()

    old_x = player.x
    old_y = player.y

    player.update(dt)

    # Jeżeli duch wszedł w półkę, cofamy go na poprzednią pozycję.
    for obstacle in obstacles:
        if obstacle.collides_with_circle(player.x, player.y, player.radius):
            player.x = old_x
            player.y = old_y
            break

    if pr.is_key_pressed(pr.KEY_BACKSPACE):
        return GameState.MENU

    return GameState.PLAYING


def draw_library_background() -> None:
    pr.clear_background(pr.Color(24, 22, 34, 255))

    # Zarys sali biblioteki.
    pr.draw_rectangle(40, 70, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 110, pr.Color(34, 30, 48, 255))
    pr.draw_rectangle_lines(40, 70, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 110, pr.Color(95, 85, 120, 255))

    # Delikatna siatka podłogi.
    for x in range(40, SCREEN_WIDTH - 40, 40):
        pr.draw_line(x, 70, x, SCREEN_HEIGHT - 40, pr.Color(40, 36, 55, 255))

    for y in range(70, SCREEN_HEIGHT - 40, 40):
        pr.draw_line(40, y, SCREEN_WIDTH - 40, y, pr.Color(40, 36, 55, 255))


def draw_hud(player: Player) -> None:
    pr.draw_rectangle(0, 0, SCREEN_WIDTH, 45, pr.Color(14, 12, 22, 240))

    pr.draw_text("Library Ghost - kolizje z polkami", 20, 13, 18, pr.RAYWHITE)
    pr.draw_text(f"Energia: {int(player.energy)}", 650, 13, 18, pr.Color(210, 220, 255, 255))
    pr.draw_text("WASD/strzalki - ruch | BACKSPACE - menu", 20, SCREEN_HEIGHT - 28, 16, pr.GRAY)


def draw_playing(player: Player, obstacles: list[Obstacle]) -> None:
    draw_library_background()

    for obstacle in obstacles:
        obstacle.draw()

    player.draw()
    draw_hud(player)


def main() -> None:
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    pr.set_target_fps(FPS)

    state = GameState.MENU
    player = Player()
    obstacles = create_obstacles()

    while not pr.window_should_close():
        if state == GameState.MENU:
            state = update_menu(player)
        elif state == GameState.PLAYING:
            state = update_playing(player, obstacles)

        pr.begin_drawing()

        if state == GameState.MENU:
            draw_menu()
        elif state == GameState.PLAYING:
            draw_playing(player, obstacles)
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
