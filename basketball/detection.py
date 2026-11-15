from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class Ball:
    x: int
    y: int
    radius: int


def detect_ball(frame: np.ndarray) -> Ball | None:
    """Return the center and radius of the largest plausible orange region."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (4, 105, 85), (28, 255, 255))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ball = None
    best_area = 0.0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area <= best_area:
            continue

        (x, y), radius = cv2.minEnclosingCircle(contour)
        circular_fill = area / (np.pi * radius**2)
        if 4 <= radius <= min(frame.shape[:2]) / 4 and circular_fill >= 0.58:
            ball = Ball(round(x), round(y), round(radius))
            best_area = area

    return ball
