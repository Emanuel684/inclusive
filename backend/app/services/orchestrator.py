from __future__ import annotations

import re
from pathlib import Path

from app.services.inference import InferenceService
from app.services.text_normalize import (
    letters_only,
    normalize_display_text,
    split_words_for_signs,
    strip_accents,
)

# Claves en ASCII minúsculas (post strip_accents). Gloss en MAYÚSCULAS para UI.
SIGN_DICTIONARY: dict[str, str] = {
    "hola": "HOLA",
    "gracias": "GRACIAS",
    "adios": "ADIOS",
    "buenos": "BUENOS",
    "dias": "DIAS",
    "ayuda": "AYUDA",
    "como": "COMO",
    "estas": "ESTAS",
    "esta": "ESTA",
    "estan": "ESTAN",
    "tu": "TU",
    "usted": "USTED",
    "bien": "BIEN",
    "mal": "MAL",
    "si": "SI",
    "no": "NO",
    "por": "POR",
    "favor": "FAVOR",
    "que": "QUE",
    "quien": "QUIEN",
    "donde": "DONDE",
    "cuando": "CUANDO",
    "mucho": "MUCHO",
    "poco": "POCO",
    "yo": "YO",
    "nosotros": "NOSOTROS",
    "ellos": "ELLOS",
    "ellas": "ELLAS",
    "el": "EL",
    "ella": "ELLA",
    "unos": "UNOS",
    "unas": "UNAS",
    "porque": "PORQUE",
    "pero": "PERO",
    "disculpa": "DISCULPA",
    "perdon": "PERDON",
    "placer": "PLACER",
    "encantado": "ENCANTADO",
    "encantada": "ENCANTADA",
}

LEX_DURATION_MS = 1050
SPELL_DURATION_MS = 580
INTER_LETTER_PAUSE_MS = 40


class TranslationOrchestrator:
    def __init__(self, inference_service: InferenceService):
        self.inference = inference_service

    def translate_text_to_sign(self, text: str) -> dict:
        display = normalize_display_text(text)
        word_pairs = split_words_for_signs(text)
        signs: list[dict] = []

        for word_index, (lookup, surface) in enumerate(word_pairs):
            if lookup in SIGN_DICTIONARY:
                gloss = SIGN_DICTIONARY[lookup]
                slug = gloss.lower()
                signs.append(
                    {
                        "token": lookup,
                        "sign_gloss": gloss,
                        "source": "dictionary",
                        "animation_id": f"lex_{slug}",
                        "duration_ms": LEX_DURATION_MS,
                        "emphasis": None,
                        "word_index": word_index,
                        "surface_word": surface,
                    }
                )
                continue

            letters = letters_only(lookup)
            if not letters:
                continue

            for char in letters:
                upper = char.upper()
                signs.append(
                    {
                        "token": char,
                        "sign_gloss": upper,
                        "source": "spelling",
                        "animation_id": f"spell_{upper.lower()}",
                        "duration_ms": SPELL_DURATION_MS + INTER_LETTER_PAUSE_MS,
                        "emphasis": None,
                        "word_index": word_index,
                        "surface_word": letters or surface,
                    }
                )

        normalized = re.sub(r"\s+", " ", strip_accents(display.lower()))
        normalized = re.sub(r"[^\w\s]+", " ", normalized, flags=re.UNICODE)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return {"normalized_text": normalized or display.lower(), "signs": signs}

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
                "word_index": 0,
                "surface_word": letter,
            }
        ]
        return {**pred, "signs": signs}

    def translate_video_sign_to_text(self, video_path: Path) -> dict:
        frame_predictions = self.inference.predict_video_letters(video_path)
        transcript = "".join(frame_predictions).replace("?", "").strip() or "NO_DETECTIONS"
        return {"frame_predictions": frame_predictions, "transcript": transcript}
