from __future__ import annotations

import copy
import random
from dataclasses import dataclass

import torch
import torch.nn as nn

CONV1_OPTS = [16, 32, 64]
CONV2_OPTS = [32, 64, 128, 256]
DENSE_OPTS = [64, 128, 256, 512]
DROP_OPTS = [0.0, 0.25, 0.4, 0.5]
LR_OPTS = [1e-4, 5e-4, 1e-3, 3e-3]
GENE_BOUNDS = [(0, 2), (0, 3), (0, 3), (0, 3), (0, 3)]


@dataclass
class Genome:
    g_conv1: int
    g_conv2: int
    g_dense: int
    g_drop: int
    g_lr: int

    def as_tuple(self):
        return (self.g_conv1, self.g_conv2, self.g_dense, self.g_drop, self.g_lr)


def random_genome(rng: random.Random) -> Genome:
    return Genome(*(rng.randint(lo, hi) for lo, hi in GENE_BOUNDS))


def genome_to_hparams(g: Genome) -> dict[str, float]:
    return {
        "c1": CONV1_OPTS[g.g_conv1],
        "c2": CONV2_OPTS[g.g_conv2],
        "hidden": DENSE_OPTS[g.g_dense],
        "dropout": DROP_OPTS[g.g_drop],
        "lr": LR_OPTS[g.g_lr],
    }


class ConvClassifier(nn.Module):
    def __init__(self, num_classes: int, c1: int, c2: int, hidden: int, dropout: float):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, c1, kernel_size=3, padding=1),
            nn.BatchNorm2d(c1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(c1, c2, kernel_size=3, padding=1),
            nn.BatchNorm2d(c2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(c2 * 7 * 7, hidden),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden, num_classes),
        )

    def forward(self, x):
        return self.head(self.features(x))


def build_model(g: Genome, num_classes: int, device: torch.device) -> ConvClassifier:
    h = genome_to_hparams(g)
    return ConvClassifier(num_classes, h["c1"], h["c2"], h["hidden"], h["dropout"]).to(device)


def crossover(a: Genome, b: Genome, rng: random.Random):
    ga = list(a.as_tuple())
    gb = list(b.as_tuple())
    point = rng.randint(1, len(ga) - 1)
    ga[point:], gb[point:] = gb[point:], ga[point:]
    return Genome(*ga), Genome(*gb)


def mutate(g: Genome, p_mut: float, rng: random.Random) -> Genome:
    genes = list(g.as_tuple())
    for idx, (lo, hi) in enumerate(GENE_BOUNDS):
        if rng.random() < p_mut:
            genes[idx] = rng.randint(lo, hi)
    return Genome(*genes)


def clone(g: Genome) -> Genome:
    return copy.deepcopy(g)
