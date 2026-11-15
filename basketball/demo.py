from pathlib import Path

import cv2
import numpy as np

from .video import open_writer

DEMO_FPS = 24.0


def make_demo(path: Path) -> None:
    """Generate a small deterministic video for a smoke test."""
    path.parent.mkdir(parents=True, exist_ok=True)
    background = np.full((240, 400, 3), (135, 94, 53), dtype=np.uint8)
    cv2.line(background, (0, 206), (399, 206), (225, 225, 225), 2)
    writer = open_writer(path, DEMO_FPS, background)

    try:
        for index in range(96):
            frame = background.copy()
            if index < 32:
                x = 47 + 3 * index
            elif index < 64:
                x = 190
            else:
                x = 256 + 3 * (index - 64)

            center = (x, 144 + round(13 * np.sin(index / 8)))
            cv2.circle(frame, center, 17, (20, 126, 250), -1, cv2.LINE_AA)
            cv2.line(frame, (x - 13, center[1]), (x + 13, center[1]), (18, 52, 110), 1)
            cv2.rectangle(frame, (167, 78), (232, 200), (100, 103, 105), -1)
            writer.write(frame)
    finally:
        writer.release()
