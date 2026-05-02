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
