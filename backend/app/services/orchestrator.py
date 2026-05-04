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

LEX_DURATION_MS = 1000
SPELL_DURATION_MS = 650


class TranslationOrchestrator:
    def __init__(self, inference_service: InferenceService):
        self.inference = inference_service

    def translate_text_to_sign(self, text: str) -> dict:
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        signs: list[dict] = []
        for token in normalized.split(" "):
            if token in SIGN_DICTIONARY:
                gloss = SIGN_DICTIONARY[token]
                # Canonical animation_id: lex_<slug> lowercase for stable frontend mapping
                slug = gloss.lower()
                signs.append(
                    {
                        "token": token,
                        "sign_gloss": gloss,
                        "source": "dictionary",
                        "animation_id": f"lex_{slug}",
                        "duration_ms": LEX_DURATION_MS,
                        "emphasis": None,
                    }
                )
            else:
                for char in token:
                    if not char.strip():
                        continue
                    upper = char.upper()
                    signs.append(
                        {
                            "token": char,
                            "sign_gloss": upper,
                            "source": "spelling",
                            "animation_id": f"spell_{upper.lower()}",
                            "duration_ms": SPELL_DURATION_MS,
                            "emphasis": None,
                        }
                    )
        return {"normalized_text": normalized, "signs": signs}

    def translate_image_to_sign(self, image_path: Path) -> dict:
        pred = self.inference.predict_image(image_path)
        letter = pred["predicted_letter"]
        slug = letter.lower() if letter.isalpha() else letter
        signs = [
            {
                "token": letter,
                "sign_gloss": letter,
                "source": "dictionary",
                "animation_id": f"lex_{slug}",
                "duration_ms": LEX_DURATION_MS,
                "emphasis": None,
            }
        ]
        return {**pred, "signs": signs}

    def translate_video_sign_to_text(self, video_path: Path) -> dict:
        frame_predictions = self.inference.predict_video_letters(video_path)
        transcript = "".join(frame_predictions).replace("?", "").strip() or "NO_DETECTIONS"
        return {"frame_predictions": frame_predictions, "transcript": transcript}
