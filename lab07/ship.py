import math
import pyray as rl

from config import (
    SCREEN_W,
    SCREEN_H,
    SHIP_THRUST,
    SHIP_ROT_SPEED,
    SHIP_FRICTION,
    SHIP_RADIUS,
    SHIP_MAX_SPEED,
)
from utils import rotate_point, clamp_speed, ghost_positions


class Ship:
    """
    Klasa statku gracza.

    Najważniejsza poprawka:
    - przód statku znajduje się lokalnie na osi X, czyli w punkcie (radius, 0),
    - ruch statku też używa osi X przez cos(angle), sin(angle),
    - dzięki temu statek leci i strzela dokładnie tam, gdzie wizualnie pokazuje nos.

    W poprzedniej wersji nos statku był lokalnie w punkcie (0, -radius),
    czyli wizualny kształt był obrócony o 90 stopni względem ruchu.
    Dlatego pocisk wyglądał, jakby leciał z boku.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        self.vx = 0.0
        self.vy = 0.0

        # -90 stopni oznacza startowo kierunek do góry.
        # Przy angle = -90:
        # cos(-90) = 0
        # sin(-90) = -1
        # czyli ruch jest w górę ekranu.
        self.angle_deg = -90.0

        self.radius = SHIP_RADIUS

        # Kształt statku w lokalnych współrzędnych.
        #
        # Bardzo ważne:
        # Nos statku jest w punkcie (radius, 0).
        # To oznacza, że domyślnie statek patrzy w prawo,
        # a potem jest obracany przez angle_deg.
        #
        # Ponieważ ruch też korzysta z:
        # cos(angle), sin(angle),
        # kształt i fizyka mają ten sam kierunek.
        self.local_points = [
            (self.radius, 0),                         # nos statku
            (-self.radius * 0.75, self.radius * 0.65),
            (-self.radius * 0.35, 0),                 # wewnętrzne wcięcie z tyłu
            (-self.radius * 0.75, -self.radius * 0.65),
        ]

    def get_angle_rad(self) -> float:
        """
        Zwraca kąt statku w radianach.

        Raylib i matematyka ruchu używają radianów,
        ale dla czytelności kąt statku przechowujemy w stopniach.
        """
        return math.radians(self.angle_deg)

    def get_forward_vector(self) -> tuple[float, float]:
        """
        Zwraca wektor kierunku przodu statku.

        Ten sam wektor powinien być używany do:
        - przyspieszania statku,
        - wyznaczania nosa statku,
        - kierunku pocisku.

        Dzięki temu nie ma rozjazdu między grafiką a logiką.
        """
        angle_rad = self.get_angle_rad()
        return math.cos(angle_rad), math.sin(angle_rad)

    def get_nose_position(self, offset: float = 8.0) -> tuple[float, float]:
        """
        Zwraca pozycję nosa statku.

        offset dodaje kilka pikseli przed nosem,
        żeby pocisk nie pojawiał się w środku statku.
        """
        forward_x, forward_y = self.get_forward_vector()

        nose_x = self.x + forward_x * (self.radius + offset)
        nose_y = self.y + forward_y * (self.radius + offset)

        return nose_x, nose_y

    def reset(self) -> None:
        """
        Resetuje statek do pozycji startowej.

        Przydatne po kolizji z asteroidą.
        """
        self.x = SCREEN_W / 2
        self.y = SCREEN_H / 2

        self.vx = 0.0
        self.vy = 0.0

        self.angle_deg = -90.0

    def update(self, dt: float) -> None:
        """
        Aktualizuje ruch statku.

        Sterowanie:
        - strzałka w lewo: obrót w lewo,
        - strzałka w prawo: obrót w prawo,
        - strzałka w górę: przyspieszenie do przodu.

        dt sprawia, że ruch jest zależny od czasu,
        a nie bezpośrednio od liczby klatek.
        """
        if rl.is_key_down(rl.KEY_LEFT):
            self.angle_deg -= SHIP_ROT_SPEED * dt

        if rl.is_key_down(rl.KEY_RIGHT):
            self.angle_deg += SHIP_ROT_SPEED * dt

        if rl.is_key_down(rl.KEY_UP):
            forward_x, forward_y = self.get_forward_vector()

            self.vx += forward_x * SHIP_THRUST * dt
            self.vy += forward_y * SHIP_THRUST * dt

        # Proste tarcie / opór ruchu.
        # Statek nie zatrzymuje się natychmiast, tylko powoli wytraca prędkość.
        self.vx *= SHIP_FRICTION
        self.vy *= SHIP_FRICTION

        # Ograniczenie maksymalnej prędkości.
        self.vx, self.vy = clamp_speed(self.vx, self.vy, SHIP_MAX_SPEED)

        self.x += self.vx * dt
        self.y += self.vy * dt

    def wrap(self) -> None:
        """
        Zawijanie świata.

        Jeśli statek wyleci poza ekran z jednej strony,
        pojawia się z drugiej strony.
        """
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def draw(self) -> None:
        """
        Rysuje statek.

        ghost_positions rysuje dodatkowe kopie przy krawędziach ekranu.
        Dzięki temu przy zawijaniu świata obiekt nie znika nagle,
        tylko płynnie przechodzi przez krawędź.
        """
        angle_rad = self.get_angle_rad()

        for cx, cy in ghost_positions(self.x, self.y, self.radius):
            self._draw_body(cx, cy, angle_rad)

            if rl.is_key_down(rl.KEY_UP):
                self._draw_engine_flame(cx, cy, angle_rad)

    def _draw_body(self, cx: float, cy: float, angle_rad: float) -> None:
        """
        Rysuje obrys statku jako wielokąt z linii.
        """
        world_points = []

        for px, py in self.local_points:
            rx, ry = rotate_point(px, py, angle_rad)
            world_points.append((cx + rx, cy + ry))

        for i in range(len(world_points)):
            x1, y1 = world_points[i]
            x2, y2 = world_points[(i + 1) % len(world_points)]

            rl.draw_line(
                int(x1),
                int(y1),
                int(x2),
                int(y2),
                rl.WHITE,
            )

        # Mała kropka na nosie.
        # Pomaga szybko zobaczyć, gdzie naprawdę jest przód statku.
        nose_x, nose_y = rotate_point(self.radius, 0, angle_rad)
        rl.draw_circle(
            int(cx + nose_x),
            int(cy + nose_y),
            2,
            rl.YELLOW,
        )

    def _draw_engine_flame(self, cx: float, cy: float, angle_rad: float) -> None:
        """
        Rysuje płomień silnika z tyłu statku.

        Skoro nos jest po prawej stronie lokalnego układu,
        tył statku znajduje się po lewej stronie,
        czyli na ujemnej osi X.
        """
        flame_left = (-self.radius * 0.75, -5)
        flame_tip = (-self.radius * 1.45, 0)
        flame_right = (-self.radius * 0.75, 5)

        fx1, fy1 = rotate_point(flame_left[0], flame_left[1], angle_rad)
        fx2, fy2 = rotate_point(flame_tip[0], flame_tip[1], angle_rad)
        fx3, fy3 = rotate_point(flame_right[0], flame_right[1], angle_rad)

        rl.draw_line(
            int(cx + fx1),
            int(cy + fy1),
            int(cx + fx2),
            int(cy + fy2),
            rl.ORANGE,
        )

        rl.draw_line(
            int(cx + fx2),
            int(cy + fy2),
            int(cx + fx3),
            int(cy + fy3),
            rl.ORANGE,
        )