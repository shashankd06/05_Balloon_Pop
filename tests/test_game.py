"""Behavior checks for the four lab requirements. Run with unittest discover."""

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from unittest.mock import patch

import pygame
from game.balloon import Balloon, BALLOON_TYPES
from game.click_detection import check_pop
from game.game_engine import GameEngine, ROUND_SECONDS, STARTING_LIVES
from game.renderer import HEIGHT, WINDOW_SIZE, RESTART_RECT
import main


def balloon(kind="normal", **kwargs):
    values = dict(x=200, y=200, radius=40, speed=120, balloon_type=kind)
    values.update(kwargs)
    return Balloon(**values)


class ClickTests(unittest.TestCase):
    def test_visible_edge_clicks_hit_for_all_sizes(self):
        for radius in (16, 30, 44):
            b = balloon(radius=radius)
            for pos in ((200 + radius, 200), (200, 200 - radius),
                        (200 + radius * 0.6, 200 + radius * 0.8)):
                with self.subTest(radius=radius, pos=pos):
                    self.assertIs(check_pop([b], pos), b)

    def test_just_outside_and_square_corner_miss(self):
        b = balloon()
        self.assertIsNone(check_pop([b], (240.01, 200)))
        self.assertIsNone(check_pop([b], (239, 239)))
        self.assertIsNone(check_pop([], (200, 200)))

    def test_overlapping_balloons_pop_topmost(self):
        lower, upper = balloon(), balloon("bonus")
        self.assertIs(check_pop([lower, upper], (230, 200)), upper)


class RoundTests(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.engine.seconds_until_spawn = 100

    def test_initial_state(self):
        e = GameEngine()
        self.assertEqual((e.score, e.lives, e.displayed_time), (0, 3, 30))
        self.assertFalse(e.game_over)
        self.assertEqual(e.balloons, [])

    def test_all_type_scores_and_pops_never_cost_lives(self):
        for kind, expected in (("normal", 10), ("bonus", 30), ("penalty", -10)):
            with self.subTest(kind=kind):
                self.engine.restart_round()
                b = balloon(kind)
                self.engine.balloons = [b]
                self.assertIs(self.engine.handle_click((230, 200)), b)
                self.assertEqual(self.engine.score, expected)
                self.assertEqual(self.engine.lives, STARTING_LIVES)
                self.assertEqual(self.engine.balloons, [])

    def test_distinct_colors_and_correct_spawned_types(self):
        self.assertEqual(len({v["color"] for v in BALLOON_TYPES.values()}), 3)
        for kind in BALLOON_TYPES:
            with patch("game.game_engine.random.choices", return_value=[kind]):
                self.engine._spawn_balloon()
            b = self.engine.balloons[-1]
            self.assertEqual(b.balloon_type, kind)
            self.assertEqual(b.points, BALLOON_TYPES[kind]["points"])
            self.assertEqual(b.color, BALLOON_TYPES[kind]["color"])
            self.assertLessEqual(b.x + b.radius, WINDOW_SIZE[0])
            self.assertGreaterEqual(b.x - b.radius, 0)

    def test_each_missed_type_costs_one_life_once(self):
        for kind in BALLOON_TYPES:
            with self.subTest(kind=kind):
                self.setUp()
                self.engine.balloons = [balloon(kind, y=HEIGHT + 40)]
                self.engine.update(0)
                self.assertEqual(self.engine.lives, 2)
                self.engine.update(0.1)
                self.assertEqual(self.engine.lives, 2)
                self.assertEqual(self.engine.score, 0)

    def test_popped_balloon_cannot_be_counted_as_a_miss(self):
        b = balloon("penalty", y=HEIGHT + 39)
        self.engine.balloons = [b]
        self.engine.handle_click((b.x, b.y))
        self.engine.update(1)
        self.assertEqual(self.engine.lives, 3)

    def test_multiple_misses_end_round_without_negative_lives(self):
        self.engine.balloons = [balloon(y=HEIGHT + 40) for _ in range(5)]
        self.engine.update(0)
        self.assertEqual(self.engine.lives, 0)
        self.assertTrue(self.engine.game_over)
        self.assertEqual(self.engine.end_reason, "No lives left!")

    def test_balloons_still_partly_visible_do_not_count_as_misses(self):
        self.engine.balloons = [balloon(y=HEIGHT + 39, speed=0)]
        self.engine.update(1)
        self.assertEqual(self.engine.lives, 3)

    def test_movement_and_countdown_use_elapsed_seconds(self):
        b = balloon()
        self.engine.balloons = [b]
        self.engine.update(0.5)
        self.assertEqual(b.y, 260)
        self.assertEqual(self.engine.remaining_time, 29.5)
        self.assertEqual(self.engine.displayed_time, 30)

    def test_countdown_reaches_zero_and_ends_round(self):
        self.engine.update(29.1)
        self.assertEqual(self.engine.displayed_time, 1)
        self.assertFalse(self.engine.game_over)
        self.engine.update(1)
        self.assertEqual(self.engine.remaining_time, 0)
        self.assertTrue(self.engine.game_over)
        self.assertEqual(self.engine.end_reason, "Time's up!")

    def test_both_end_conditions_freeze_score_movement_and_spawning(self):
        for reason in ("timer", "lives"):
            with self.subTest(reason=reason):
                self.setUp()
                b = balloon()
                self.engine.balloons = [b]
                self.engine.score = 70
                if reason == "timer":
                    self.engine.update(ROUND_SECONDS)
                else:
                    self.engine.balloons += [balloon(y=HEIGHT + 40) for _ in range(3)]
                    self.engine.update(0)
                snapshot = (self.engine.score, self.engine.lives, self.engine.remaining_time, b.y)
                self.engine.handle_click((b.x, b.y))
                with patch.object(self.engine, "_spawn_balloon") as spawn:
                    self.engine.update(10)
                    spawn.assert_not_called()
                self.assertEqual(snapshot, (self.engine.score, self.engine.lives,
                                            self.engine.remaining_time, b.y))

    def test_restart_button_resets_everything(self):
        self.engine.score = -20
        self.engine.lives = 1
        self.engine.balloons = [balloon()]
        self.engine.update(30)
        self.engine.handle_click(RESTART_RECT.center)
        self.assertEqual((self.engine.score, self.engine.lives, self.engine.remaining_time), (0, 3, 30))
        self.assertEqual(self.engine.balloons, [])
        self.assertEqual(self.engine.seconds_until_spawn, 0)
        self.assertIsNone(self.engine.end_reason)
        self.assertFalse(self.engine.game_over)

    def test_restart_rectangle_is_a_normal_play_area_during_round(self):
        b = balloon(x=RESTART_RECT.centerx, y=RESTART_RECT.centery)
        self.engine.balloons = [b]
        self.engine.handle_click(RESTART_RECT.center)
        self.assertEqual(self.engine.score, 10)
        self.assertFalse(self.engine.game_over)

    def test_spawning_starts_and_repeats(self):
        e = GameEngine()
        e.update(0)
        self.assertEqual(len(e.balloons), 1)
        e.update(0.5)
        self.assertEqual(len(e.balloons), 1)
        e.update(0.25)
        self.assertEqual(len(e.balloons), 2)

    def test_negative_elapsed_time_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.update(-1)


class ApplicationTests(unittest.TestCase):
    def test_real_main_loop_renders_handles_clicks_restart_keys_and_quits(self):
        for key in (pygame.K_r, pygame.K_RETURN):
            with self.subTest(key=key):
                e = GameEngine()
                e.balloons = [balloon()]
                fake_clock = unittest.mock.Mock()
                fake_clock.tick.side_effect = [0, 30000, 0, 0]
                batches = [
                    [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=(200, 200))],
                    [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(200, 200))],
                    [pygame.event.Event(pygame.KEYDOWN, key=key)],
                    [pygame.event.Event(pygame.QUIT)],
                ]
                with patch("main.GameEngine", return_value=e), \
                     patch("main.pygame.time.Clock", return_value=fake_clock), \
                     patch("main.pygame.event.get", side_effect=batches):
                    main.main()
                self.assertEqual((e.score, e.lives, e.remaining_time), (0, 3, 30))
                self.assertFalse(e.game_over)


if __name__ == "__main__":
    unittest.main()
