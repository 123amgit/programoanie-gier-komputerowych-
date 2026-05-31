# player.py
# Klasa gracza - mały duch poruszający się po bibliotece.

import pyray as pr

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_RADIUS,
    PLAYER_SPEED,
    PLAYER_MAX_ENERGY,
)
from utils import clamp


class Player:
    def __init__(self) -> None:
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.energy = PLAYER_MAX_ENERGY

    def reset(self) -> None:
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.energy = PLAYER_MAX_ENERGY

    def update(self, dt: float) -> None:
        dx = 0
        dy = 0

        if pr.is_key_down(pr.KEY_A) or pr.is_key_down(pr.KEY_LEFT):
            dx -= 1
        if pr.is_key_down(pr.KEY_D) or pr.is_key_down(pr.KEY_RIGHT):
            dx += 1
        if pr.is_key_down(pr.KEY_W) or pr.is_key_down(pr.KEY_UP):
            dy -= 1
        if pr.is_key_down(pr.KEY_S) or pr.is_key_down(pr.KEY_DOWN):
            dy += 1

        # Normalizacja ruchu po skosie, żeby duch nie poruszał się szybciej diagonalnie.
        if dx != 0 or dy != 0:
            length = (dx * dx + dy * dy) ** 0.5
            dx /= length
            dy /= length

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        # Duch nie może wyjść poza ekran.
        self.x = clamp(self.x, self.radius, SCREEN_WIDTH - self.radius)
        self.y = clamp(self.y, self.radius, SCREEN_HEIGHT - self.radius)

    def draw(self) -> None:
        ghost_color = pr.Color(220, 230, 255, 220)
        eye_color = pr.Color(40, 35, 70, 255)
        aura_color = pr.Color(140, 150, 220, 120)

        # Główne ciało ducha.
        pr.draw_circle(int(self.x), int(self.y), self.radius, ghost_color)

        # Dolna falująca część ducha.
        pr.draw_circle(int(self.x - 10), int(self.y + 13), 7, ghost_color)
        pr.draw_circle(int(self.x), int(self.y + 15), 7, ghost_color)
        pr.draw_circle(int(self.x + 10), int(self.y + 13), 7, ghost_color)

        # Oczy.
        pr.draw_circle(int(self.x - 6), int(self.y - 4), 3, eye_color)
        pr.draw_circle(int(self.x + 6), int(self.y - 4), 3, eye_color)

        # Delikatna aura.
        pr.draw_circle_lines(int(self.x), int(self.y), self.radius + 5, aura_color)
