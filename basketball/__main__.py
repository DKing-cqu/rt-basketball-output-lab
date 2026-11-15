import argparse
import math
from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy as np

from .demo import make_demo
from .detection import detect_ball
from .output import write_outputs
from .tracking import Tracker, TrackingResult
from .video import frames, open_video


def track_video(reader: cv2.VideoCapture, fps: float) -> Iterator[tuple[np.ndarray, TrackingResult]]:
    tracker = Tracker()
    for index, frame in enumerate(frames(reader)):
        detection = detect_ball(frame)
        yield frame, tracker.update(index, fps, detection)


def main() -> None:
    parser = argparse.ArgumentParser(description="Track the basketball in a video.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="Path to the input video.")
    source.add_argument("--demo", action="store_true", help="Generate and use the synthetic smoke-test video.")
    parser.add_argument("--output-dir", type=Path, default=Path("runs/tracking"))
    args = parser.parse_args()

    try:
        input_path = args.input
        if args.demo:
            input_path = Path("runs/fixtures/basketball-demo.mp4")
            make_demo(input_path)

        reader = open_video(input_path)
        try:
            fps = reader.get(cv2.CAP_PROP_FPS)
            if not math.isfinite(fps) or fps <= 0:
                parser.error(f"Invalid frame rate in {input_path}")
            count = write_outputs(track_video(reader, fps), fps, args.output_dir)
            if count == 0:
                parser.error(f"No frames could be decoded from {input_path}")
        finally:
            reader.release()
    except OSError as error:
        parser.exit(1, f"{error}\n")

    print(f"{count} frames -> {args.output_dir / 'tracking.csv'} and {args.output_dir / 'annotated.mp4'}")


if __name__ == "__main__":
    main()
