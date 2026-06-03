# shelf.py
# Magiczna półka do oddawania zagubionych stron.

import pyray as pr

from config import SHELF_X, SHELF_Y, SHELF_WIDTH, SHELF_HEIGHT
from utils import circle_rect_collision


class Shelf:
    def __init__(self) -> None:
        self.rect = pr.Rectangle(SHELF_X, SHELF_Y, SHELF_WIDTH, SHELF_HEIGHT)

    def collides_with_player(self, player) -> bool:
        return circle_rect_collision(player.x, player.y, player.radius, self.rect)

    def draw(self) -> None:
        # Magiczna półka.
        pr.draw_rectangle_rec(self.rect, pr.Color(75, 45, 95, 255))
        pr.draw_rectangle_lines_ex(self.rect, 3, pr.Color(190, 150, 255, 255))

        pr.draw_text(
            "MAGIC SHELF",
            int(self.rect.x + 10),
            int(self.rect.y + 12),
            16,
            pr.Color(230, 220, 255, 255),
        )

        # Delikatny magiczny blask.
        pr.draw_circle_lines(
            int(self.rect.x + self.rect.width / 2),
            int(self.rect.y + self.rect.height / 2),
            78,
            pr.Color(160, 120, 255, 90),
        )
