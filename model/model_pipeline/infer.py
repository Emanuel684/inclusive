from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from model_pipeline.model import ConvClassifier


def load_inference_bundle(artifacts_dir: Path) -> tuple[dict, list[str]]:
    metadata = json.loads((artifacts_dir / "metadata.json").read_text(encoding="utf-8"))
    labels = json.loads((artifacts_dir / "labels.json").read_text(encoding="utf-8"))
    return metadata, labels


def load_model_from_artifacts(artifacts_dir: Path) -> ConvClassifier:
    metadata, _ = load_inference_bundle(artifacts_dir)
    h = metadata["hparams"]
    model = ConvClassifier(
        num_classes=metadata["num_classes"],
        c1=h["c1"],
        c2=h["c2"],
        hidden=h["hidden"],
        dropout=h["dropout"],
    )
    state = torch.load(artifacts_dir / "model.pt", map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return model


def predict_image(image_path: Path, artifacts_dir: Path) -> dict:
    model = load_model_from_artifacts(artifacts_dir)
    _, labels = load_inference_bundle(artifacts_dir)
    image = Image.open(image_path).convert("L").resize((28, 28))
    arr = np.asarray(image, dtype=np.float32) / 255.0
    x = torch.from_numpy(arr).view(1, 1, 28, 28)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)
        conf, pred = probs.max(dim=1)
    pred_i = int(pred.item())
    return {"label_index": pred_i, "label": labels[pred_i], "confidence": float(conf.item())}
