from __future__ import annotations

import json
from pathlib import Path

import torch


def export_artifacts(model: torch.nn.Module, output_dir: Path, labels: list[str], metadata: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / "model.pt"
    labels_path = output_dir / "labels.json"
    metadata_path = output_dir / "metadata.json"
    torch.save(model.state_dict(), state_path)
    labels_path.write_text(json.dumps(labels, ensure_ascii=True, indent=2), encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=True, indent=2), encoding="utf-8")


def export_torchscript(model: torch.nn.Module, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    model.eval()
    scripted = torch.jit.script(model.cpu())
    path = output_dir / "model_scripted.pt"
    scripted.save(str(path))
    return path
