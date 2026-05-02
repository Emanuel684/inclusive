from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image

LETTERS_SIGN = "ABCDEFGHIKLMNOPQRSTUVWXY"


def _letter_from_index(idx: int) -> str:
    if 0 <= idx < len(LETTERS_SIGN):
        return LETTERS_SIGN[idx]
    return "?"


class InferenceService:
    """MVP inference service with deterministic fallback logic.

    It is intentionally lightweight so backend APIs work even without
    trained artifacts. When artifacts are available, this class is the
    extension point to load Torch/ONNX model.
    """

    def __init__(self, artifacts_dir: Path):
        self.artifacts_dir = artifacts_dir

    def predict_image(self, image_path: Path) -> dict[str, Any]:
        image = Image.open(image_path).convert("L").resize((28, 28))
        arr = np.asarray(image, dtype=np.float32) / 255.0
        score = float(arr.mean())
        label = int(min(24, max(0, round(score * 24))))
        confidence = float(min(0.99, max(0.50, 0.5 + abs(score - 0.5))))
        return {
            "predicted_label": label,
            "predicted_letter": _letter_from_index(label),
            "confidence": confidence,
        }

    def predict_video_letters(self, video_path: Path) -> list[str]:
        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            return ["?"]

        predictions: list[str] = []
        frame_index = 0
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame_index % 10 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                score = float(np.mean(gray) / 255.0)
                label = int(min(24, max(0, round(score * 24))))
                predictions.append(_letter_from_index(label))
            frame_index += 1
        capture.release()
        return predictions or ["?"]
