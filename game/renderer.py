"""All Pygame drawing, including the HUD, type legend, and restart button."""

import pygame

from game.balloon import BALLOON_TYPES

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)
RESTART_RECT = pygame.Rect(220, 315, 260, 50)
COLOR_BG = (200, 230, 245)
COLOR_TEXT = (30, 30, 30)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_centered(surface, font, text, y, color=COLOR_TEXT):
    label = font.render(text, True, color)
    surface.blit(label, label.get_rect(center=(WIDTH // 2, y)))


def draw_scene(surface, balloons, font):
    surface.fill(COLOR_BG)
    for balloon in balloons:
        center = (int(balloon.x), int(balloon.y))
        pygame.draw.line(
            surface, (100, 115, 125),
            (center[0], center[1] + balloon.radius),
            (center[0], center[1] + balloon.radius + 12), 2,
        )
        pygame.draw.circle(surface, balloon.color, center, balloon.radius)
        pygame.draw.circle(surface, (55, 65, 75), center, balloon.radius, 2)
        symbol = {"normal": "+", "bonus": "*", "penalty": "-"}[balloon.balloon_type]
        label = font.render(symbol, True, COLOR_TEXT)
        surface.blit(label, label.get_rect(center=center))


def draw_hud(surface, font, score, lives, remaining_seconds):
    pygame.draw.rect(surface, (240, 248, 252), (0, 0, WIDTH, 90))
    draw_text(surface, font, f"Score: {score}", (15, 10))
    draw_text(surface, font, f"Lives: {lives}", (280, 10))
    timer_color = (175, 35, 55) if remaining_seconds <= 5 else COLOR_TEXT
    draw_text(surface, font, f"Time: {remaining_seconds}s", (520, 10), timer_color)
    small_font = pygame.font.SysFont("consolas", 16)
    for x, kind, label in (
        (25, "normal", "Normal +10"),
        (235, "bonus", "Bonus +30"),
        (440, "penalty", "Penalty -10"),
    ):
        pygame.draw.circle(surface, BALLOON_TYPES[kind]["color"], (x, 60), 9)
        draw_text(surface, small_font, label, (x + 17, 51))
    draw_text(surface, small_font, "Left-click balloons. Every missed type costs 1 life.", (15, 72))


def draw_game_over(surface, font, score, reason):
    veil = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    veil.fill((15, 30, 45, 160))
    surface.blit(veil, (0, 0))
    pygame.draw.rect(surface, (250, 252, 255), (145, 155, 410, 235), border_radius=15)
    title_font = pygame.font.SysFont("consolas", 32, bold=True)
    draw_centered(surface, title_font, "ROUND OVER", 195)
    draw_centered(surface, font, reason, 240)
    draw_centered(surface, title_font, f"Final score: {score}", 282)
    pygame.draw.rect(surface, (30, 105, 170), RESTART_RECT, border_radius=8)
    draw_centered(surface, font, "Play again (R/Enter)", RESTART_RECT.centery, (255, 255, 255))
