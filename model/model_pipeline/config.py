from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineConfig:
    data_dir: Path = Path(".")
    artifacts_dir: Path = Path("model/artifacts")
    seed: int = 42
    batch_size: int = 128
