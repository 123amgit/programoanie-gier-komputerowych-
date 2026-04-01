import math
import pyray as rl

DEBUG = {"enabled": True}

SHIP_VERTS = [
    (0.0, -18.0),
    (-12.0, 12.0),
    (12.0, 12.0),
]

FLAME_VERTS = [
    (0.0, 22.0),
    (-7.0, 12.0),
    (7.0, 12.0),
]

ROT_SPEED = 3.2
THRUST = 260.0
FRICTION = 90.0
MAX_SPEED = 320.0
BRAKE_FACTOR = 4.5
DEBUG_VECTOR_SCALE = 0.35
SHIP_RADIUS = 18.0


class Ship:
    def __init__(self, x: float, y: float, screen_w: int, screen_h: int) -> None:
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.reset(x, y)

    def reset(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.angle = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.thrusting = False

    @staticmethod
    def rotate_point(px: float, py: float, angle: float) -> tuple[float, float]:
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        rx = px * cos_a - py * sin_a
        ry = px * sin_a + py * cos_a
        return rx, ry

    def transform_vertices(self, verts: list[tuple[float, float]]) -> list[rl.Vector2]:
        transformed = []
        for px, py in verts:
            rx, ry = self.rotate_point(px, py, self.angle)
            transformed.append(rl.Vector2(self.x + rx, self.y + ry))
        return transformed

    def get_forward_vector(self) -> tuple[float, float]:
        fx = math.sin(self.angle)
        fy = -math.cos(self.angle)
        return fx, fy

    def apply_friction(self, dt: float, strength_multiplier: float = 1.0) -> None:
        speed = math.hypot(self.vx, self.vy)
        if speed <= 1e-8:
            self.vx = 0.0
            self.vy = 0.0
            return

        decel = FRICTION * strength_multiplier * dt

        if decel >= speed:
            self.vx = 0.0
            self.vy = 0.0
            return

        new_speed = speed - decel
        scale = new_speed / speed
        self.vx *= scale
        self.vy *= scale

    def clamp_speed(self) -> None:
        speed = math.hypot(self.vx, self.vy)
        if speed > MAX_SPEED:
            scale = MAX_SPEED / speed
            self.vx *= scale
            self.vy *= scale

    def bounce_off_screen_edges(self) -> None:
        if self.x < SHIP_RADIUS:
            self.x = SHIP_RADIUS
            self.vx = -self.vx
        elif self.x > self.screen_w - SHIP_RADIUS:
            self.x = self.screen_w - SHIP_RADIUS
            self.vx = -self.vx

        if self.y < SHIP_RADIUS:
            self.y = SHIP_RADIUS
            self.vy = -self.vy
        elif self.y > self.screen_h - SHIP_RADIUS:
            self.y = self.screen_h - SHIP_RADIUS
            self.vy = -self.vy

    def update(self, dt: float) -> None:
        self.thrusting = False

        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.angle -= ROT_SPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.angle += ROT_SPEED * dt

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            fx, fy = self.get_forward_vector()
            self.vx += fx * THRUST * dt
            self.vy += fy * THRUST * dt
            self.thrusting = True

        if rl.is_key_down(rl.KeyboardKey.KEY_Z):
            self.apply_friction(dt, BRAKE_FACTOR)
        else:
            self.apply_friction(dt)

        self.clamp_speed()

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.bounce_off_screen_edges()

    def draw(self) -> None:
        ship_pts = self.transform_vertices(SHIP_VERTS)
        rl.draw_triangle_lines(ship_pts[0], ship_pts[1], ship_pts[2], rl.RAYWHITE)

        if self.thrusting:
            flame_pts = self.transform_vertices(FLAME_VERTS)
            rl.draw_triangle_lines(flame_pts[0], flame_pts[1], flame_pts[2], rl.ORANGE)

        if DEBUG["enabled"]:
            rl.draw_circle_v(rl.Vector2(self.x, self.y), 2.5, rl.YELLOW)

            speed = math.hypot(self.vx, self.vy)
            end_x = self.x + self.vx * DEBUG_VECTOR_SCALE
            end_y = self.y + self.vy * DEBUG_VECTOR_SCALE

            rl.draw_line_ex(
                rl.Vector2(self.x, self.y),
                rl.Vector2(end_x, end_y),
                2.0,
                rl.GREEN
            )

            rl.draw_text(
                f"speed = {speed:.2f} px/s",
                int(self.x + 18),
                int(self.y - 18),
                18,
                rl.GREEN
            )

            rl.draw_text(
                f"vx = {self.vx:.2f}, vy = {self.vy:.2f}",
                int(self.x + 18),
                int(self.y + 4),
                16,
                rl.LIME
            )

            display_angle = math.degrees(self.angle) % 360.0
            rl.draw_text(
                f"angle = {display_angle:.1f} deg",
                int(self.x + 18),
                int(self.y + 24),
                16,
                rl.SKYBLUE
            )