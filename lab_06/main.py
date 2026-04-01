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
)
from ship import Ship
from asteroid import Asteroid


def create_asteroids(count: int):
    asteroids = []
    for _ in range(count):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        radius = random.uniform(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        asteroids.append(Asteroid(x, y, radius))
    return asteroids


def main():
    rl.init_window(SCREEN_W, SCREEN_H, "Lab 06 - Asteroids / Toroidal World")
    rl.set_target_fps(FPS)

    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)
    asteroids = create_asteroids(ASTEROID_COUNT)

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        ship.update(dt)
        ship.wrap()

        for asteroid in asteroids:
            asteroid.update(dt)
            asteroid.wrap()

        rl.begin_drawing()
        rl.clear_background(rl.Color(*BG_COLOR))

        ship.draw()
        for asteroid in asteroids:
            asteroid.draw()

        rl.draw_text("ARROWS: move ship", 20, 20, 20, rl.RAYWHITE)
        rl.draw_text("Toroidal world + ghost rendering + polygon asteroids", 20, 50, 20, rl.GRAY)

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()