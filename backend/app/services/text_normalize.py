from __future__ import annotations

import re
import unicodedata


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def normalize_display_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).strip()


def tokenize_words(text: str) -> list[str]:
    """Lowercase, strip accents, replace punctuation with spaces, split words."""
    raw = text.strip().lower()
    raw = strip_accents(raw)
    raw = re.sub(r"[^\w\s]+", " ", raw, flags=re.UNICODE)
    raw = re.sub(r"\s+", " ", raw).strip()
    if not raw:
        return []
    return [w for w in raw.split(" ") if w]


def split_words_for_signs(text: str) -> list[tuple[str, str]]:
    """Return (lookup_key, surface_word) per palabra; lookup sin acentos en minúsculas."""
    display = normalize_display_text(text)
    spaced = re.sub(r"[^\w\s]+", " ", display, flags=re.UNICODE)
    spaced = re.sub(r"\s+", " ", spaced).strip()
    if not spaced:
        return []
    out: list[tuple[str, str]] = []
    for raw in spaced.split(" "):
        if not raw:
            continue
        lookup = strip_accents(raw.lower())
        out.append((lookup, raw))
    return out


def letters_only(word: str) -> str:
    return "".join(ch for ch in word if ch.isalpha())
