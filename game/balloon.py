"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size - this matters for
how click detection should work.
"""

import pygame

BALLOON_TYPES = {
    "normal": {"color": (45, 140, 220), "points": 10},
    "bonus": {"color": (245, 190, 40), "points": 30},
    "penalty": {"color": (220, 65, 85), "points": -10},
}


class Balloon:
    def __init__(self, x, y, radius, speed, balloon_type="normal"):
        if balloon_type not in BALLOON_TYPES:
            raise ValueError(f"Unknown balloon type: {balloon_type}")
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type
        self.color = BALLOON_TYPES[balloon_type]["color"]
        self.points = BALLOON_TYPES[balloon_type]["points"]

    def update(self, dt):
        # Speed is in pixels per second, independent of rendering speed.
        self.y += self.speed * dt

    def is_past_bottom(self, height):
        return self.y - self.radius >= height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
