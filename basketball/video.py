from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy as np


def open_video(path: Path) -> cv2.VideoCapture:
    reader = cv2.VideoCapture(str(path))
    if not reader.isOpened():
        reader.release()
        raise OSError(f"Cannot open input video: {path}")
    return reader


def frames(reader: cv2.VideoCapture) -> Iterator[np.ndarray]:
    while True:
        success, frame = reader.read()
        if not success:
            return
        yield frame


def open_writer(path: Path, fps: float, frame: np.ndarray) -> cv2.VideoWriter:
    height, width = frame.shape[:2]
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        writer.release()
        raise OSError(f"Cannot open output video: {path}")
    return writer
