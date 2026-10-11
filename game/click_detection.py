"""
click_detection: figures out whether a click landed on a balloon.
"""

import math


def check_pop(balloons, click_pos):
    """
    Returns the balloon that was clicked, or None if the click missed
    every balloon.
    """
    # Last drawn is on top, so pop the visible balloon in an overlap.
    for balloon in reversed(balloons):
        dx = click_pos[0] - balloon.x
        dy = click_pos[1] - balloon.y
        distance_squared = dx * dx + dy * dy
        radius_squared = balloon.radius * balloon.radius
        # Allow only floating-point rounding at the exact circular boundary.
        if distance_squared <= radius_squared or math.isclose(
            distance_squared, radius_squared, rel_tol=1e-12
        ):
            return balloon
    return None
