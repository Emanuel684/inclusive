import io

from PIL import Image
from fastapi.testclient import TestClient

from app.main import app


def test_text_to_sign() -> None:
    client = TestClient(app)
    response = client.post("/translate/text-to-sign", json={"text": "hola mundo"})
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "text-to-sign"
    assert len(data["signs"]) > 0
    first = data["signs"][0]
    assert "animation_id" in first
    assert first["animation_id"].startswith("lex_") or first["animation_id"].startswith("spell_")
    assert first["animation_id"] == "lex_hola"
    assert first.get("duration_ms") is not None
    assert first.get("word_index") == 0
    assert all("animation_id" in s for s in data["signs"])
    assert data["signs"][1]["animation_id"] == "spell_m"
    assert data["signs"][1]["word_index"] == 1


def test_text_to_sign_hola_como_estas() -> None:
    client = TestClient(app)
    response = client.post("/translate/text-to-sign", json={"text": "hola como estas?"})
    assert response.status_code == 200
    data = response.json()
    signs = data["signs"]
    assert len(signs) == 3
    assert [s["animation_id"] for s in signs] == ["lex_hola", "lex_como", "lex_estas"]
    assert [s["word_index"] for s in signs] == [0, 1, 2]
    assert signs[0]["surface_word"].lower().startswith("hola")


def test_text_to_sign_lex_slugs_lowercase() -> None:
    client = TestClient(app)
    response = client.post("/translate/text-to-sign", json={"text": "gracias"})
    assert response.status_code == 200
    signs = response.json()["signs"]
    assert len(signs) == 1
    assert signs[0]["animation_id"] == "lex_gracias"
    assert signs[0]["sign_gloss"] == "GRACIAS"


def test_image_to_sign() -> None:
    client = TestClient(app)
    image = Image.new("L", (28, 28), color=120)
    buff = io.BytesIO()
    image.save(buff, format="PNG")
    buff.seek(0)
    response = client.post(
        "/translate/image-to-sign",
        files={"file": ("sample.png", buff, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "image-to-sign"
    assert "predicted_letter" in data
    assert data["signs"][0].get("word_index") == 0
