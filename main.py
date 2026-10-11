"""
Balloon Pop (Completed Lab)

Run with:  python3 main.py

Click balloons to pop them before they reach the bottom.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Balloon Pop")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    engine = GameEngine()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        # End an expired round before processing further gameplay clicks.
        engine.update(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif engine.game_over and event.key in (pygame.K_r, pygame.K_RETURN):
                    engine.restart_round()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                engine.handle_click(event.pos)

        engine.draw(screen, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
