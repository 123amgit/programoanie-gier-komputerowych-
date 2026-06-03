# obstacle.py
# Przeszkody biblioteczne: półki, stoły i ściany.

import pyray as pr

from utils import circle_rect_collision


class Obstacle:
    def __init__(self, x: float, y: float, width: float, height: float, name: str = "shelf") -> None:
        self.rect = pr.Rectangle(x, y, width, height)
        self.name = name

    def collides_with_circle(self, x: float, y: float, radius: float) -> bool:
        return circle_rect_collision(x, y, radius, self.rect)

    def draw(self) -> None:
        # Prosty styl drewnianej półki.
        pr.draw_rectangle_rec(self.rect, pr.Color(85, 58, 45, 255))
        pr.draw_rectangle_lines_ex(self.rect, 2, pr.Color(130, 95, 70, 255))

        # Linie książek/dekoracji na półce.
        if self.rect.width > self.rect.height:
            step = 14
            start_x = int(self.rect.x + 8)
            end_x = int(self.rect.x + self.rect.width - 8)

            for x in range(start_x, end_x, step):
                pr.draw_line(
                    x,
                    int(self.rect.y + 5),
                    x,
                    int(self.rect.y + self.rect.height - 5),
                    pr.Color(115, 85, 65, 255),
                )
        else:
            step = 14
            start_y = int(self.rect.y + 8)
            end_y = int(self.rect.y + self.rect.height - 8)

            for y in range(start_y, end_y, step):
                pr.draw_line(
                    int(self.rect.x + 5),
                    y,
                    int(self.rect.x + self.rect.width - 5),
                    y,
                    pr.Color(115, 85, 65, 255),
                )
