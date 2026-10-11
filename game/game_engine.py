"""Round state, spawning, scoring, lives, and elapsed-time movement."""

import math
import random

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT, RESTART_RECT

SPAWN_INTERVAL_SECONDS = 0.75
STARTING_LIVES = 3
ROUND_SECONDS = 30.0


class GameEngine:
    def __init__(self):
        self.restart_round()

    def restart_round(self):
        """Reset every piece of round state, including pending spawns."""
        self.balloons = []
        self.seconds_until_spawn = 0.0
        self.score = 0
        self.lives = STARTING_LIVES
        self.remaining_time = ROUND_SECONDS
        self.game_over = False
        self.end_reason = None

    @property
    def displayed_time(self):
        # Show 30 immediately and 1 throughout the final partial second.
        return math.ceil(self.remaining_time)

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(90.0, 180.0)
        balloon_type = random.choices(
            ["normal", "bonus", "penalty"], weights=[6, 2, 2]
        )[0]
        self.balloons.append(Balloon(x, -radius, radius, speed, balloon_type))

    def handle_click(self, pos):
        if self.game_over:
            if RESTART_RECT.collidepoint(pos):
                self.restart_round()
            return None
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points
        return popped

    def _end_round(self, reason):
        self.game_over = True
        self.end_reason = reason

    def update(self, dt):
        """Advance a live round by dt seconds; ended rounds stay frozen."""
        if dt < 0:
            raise ValueError("Elapsed time cannot be negative")
        if self.game_over:
            return
        self.remaining_time = max(0.0, self.remaining_time - dt)
        if self.remaining_time <= 0:
            self._end_round("Time's up!")
            return

        # Advance existing balloons, removing each miss exactly once.
        survivors = []
        for balloon in self.balloons:
            balloon.update(dt)
            if balloon.is_past_bottom(HEIGHT):
                self.lives = max(0, self.lives - 1)
            else:
                survivors.append(balloon)
        self.balloons = survivors
        if self.lives == 0:
            self._end_round("No lives left!")
            return

        self.seconds_until_spawn -= dt
        if self.seconds_until_spawn <= 0:
            self._spawn_balloon()
            # Avoid a burst of off-screen spawns after a paused window.
            self.seconds_until_spawn = SPAWN_INTERVAL_SECONDS

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons, font)
        renderer.draw_hud(surface, font, self.score, self.lives, self.displayed_time)
        if self.game_over:
            renderer.draw_game_over(surface, font, self.score, self.end_reason)
