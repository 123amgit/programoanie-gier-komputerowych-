# page.py
# Obiekt kolekcjonowany: zagubiona strona książki.

import pyray as pr

from config import PAGE_RADIUS
from utils import circle_collision


class Page:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.radius = PAGE_RADIUS
        self.collected = False
        self.delivered = False

    def can_be_picked(self) -> bool:
        return not self.collected and not self.delivered

    def collides_with_player(self, player) -> bool:
        return circle_collision(self.x, self.y, self.radius, player.x, player.y, player.radius)

    def draw(self) -> None:
        if self.collected or self.delivered:
            return

        # Kartka papieru.
        pr.draw_rectangle(int(self.x - 8), int(self.y - 11), 16, 22, pr.Color(235, 226, 185, 255))
        pr.draw_rectangle_lines(int(self.x - 8), int(self.y - 11), 16, 22, pr.Color(130, 115, 80, 255))

        # Proste linie tekstu na kartce.
        pr.draw_line(int(self.x - 5), int(self.y - 5), int(self.x + 5), int(self.y - 5), pr.Color(150, 130, 90, 255))
        pr.draw_line(int(self.x - 5), int(self.y), int(self.x + 4), int(self.y), pr.Color(150, 130, 90, 255))
        pr.draw_line(int(self.x - 5), int(self.y + 5), int(self.x + 2), int(self.y + 5), pr.Color(150, 130, 90, 255))
