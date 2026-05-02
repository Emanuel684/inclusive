from __future__ import annotations

import re
from pathlib import Path

from app.services.inference import InferenceService

SIGN_DICTIONARY = {
    "hola": "HOLA",
    "gracias": "GRACIAS",
    "adios": "ADIOS",
    "buenos": "BUENOS",
    "dias": "DIAS",
    "ayuda": "AYUDA",
}


class TranslationOrchestrator:
    def __init__(self, inference_service: InferenceService):
        self.inference = inference_service

    def translate_text_to_sign(self, text: str) -> dict:
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        signs: list[dict] = []
        for token in normalized.split(" "):
            if token in SIGN_DICTIONARY:
                signs.append(
                    {"token": token, "sign_gloss": SIGN_DICTIONARY[token], "source": "dictionary"}
                )
            else:
                for char in token:
                    signs.append(
                        {"token": char, "sign_gloss": char.upper(), "source": "spelling"}
                    )
        return {"normalized_text": normalized, "signs": signs}

    def translate_image_to_sign(self, image_path: Path) -> dict:
        pred = self.inference.predict_image(image_path)
        signs = [
            {
                "token": pred["predicted_letter"],
                "sign_gloss": pred["predicted_letter"],
                "source": "dictionary",
            }
        ]
        return {**pred, "signs": signs}

    def translate_video_sign_to_text(self, video_path: Path) -> dict:
        frame_predictions = self.inference.predict_video_letters(video_path)
        transcript = "".join(frame_predictions).replace("?", "").strip() or "NO_DETECTIONS"
        return {"frame_predictions": frame_predictions, "transcript": transcript}
