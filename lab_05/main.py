import pyray as rl
from ship import Ship, DEBUG

SCREEN_W = 800
SCREEN_H = 600
TITLE = "Lab 05 - Statek: geometria, ruch i fizyka"


def draw_hud(current_fps: int) -> None:
    rl.draw_text("STEROWANIE:", 10, 10, 20, rl.RAYWHITE)
    rl.draw_text("LEWO/PRAWO - obrot", 10, 38, 18, rl.LIGHTGRAY)
    rl.draw_text("GORA - thrust", 10, 62, 18, rl.LIGHTGRAY)
    rl.draw_text("Z - hamulec awaryjny (*)", 10, 86, 18, rl.LIGHTGRAY)
    rl.draw_text("D - debug ON/OFF", 10, 110, 18, rl.LIGHTGRAY)
    rl.draw_text("R - reset statku", 10, 134, 18, rl.LIGHTGRAY)
    rl.draw_text("ESC - wyjscie", 10, 158, 18, rl.LIGHTGRAY)

    rl.draw_text(f"FPS: {current_fps}", 10, 190, 18, rl.GREEN)

    if DEBUG["enabled"]:
        rl.draw_text("DEBUG: ON", 10, 214, 18, rl.YELLOW)
    else:
        rl.draw_text("DEBUG: OFF", 10, 214, 18, rl.DARKGRAY)


def main() -> None:
    rl.init_window(SCREEN_W, SCREEN_H, TITLE)
    rl.set_target_fps(1000)

    ship = Ship(SCREEN_W / 2, SCREEN_H / 2, SCREEN_W, SCREEN_H)

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        if dt > 0.05:
            dt = 0.05

        if rl.is_key_pressed(rl.KEY_D):
            DEBUG["enabled"] = not DEBUG["enabled"]

        if rl.is_key_pressed(rl.KEY_R):
            ship.reset(SCREEN_W / 2, SCREEN_H / 2)

        ship.update(dt)

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        ship.draw()
        draw_hud(rl.get_fps())

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()