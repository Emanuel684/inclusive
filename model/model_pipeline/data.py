from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset


class SignDataset(Dataset):
    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.x = torch.from_numpy(x).view(-1, 1, 28, 28)
        self.y = torch.from_numpy(y).long()

    def __len__(self) -> int:
        return len(self.y)

    def __getitem__(self, idx: int):
        return self.x[idx], self.y[idx]


def _find_csv(base: Path, name: str) -> Path:
    for root, _, files in os.walk(base):
        if name in files:
            return Path(root) / name
    raise FileNotFoundError(f"Could not find {name} in {base}")


def load_data(data_dir: Path, seed: int = 42):
    train_path = _find_csv(data_dir, "sign_mnist_train.csv")
    test_path = _find_csv(data_dir, "sign_mnist_test.csv")

    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    x_all = df_train.drop(columns=["label"]).values.astype(np.float32) / 255.0
    y_all = df_train["label"].values.astype(np.int64)
    x_test = df_test.drop(columns=["label"]).values.astype(np.float32) / 255.0
    y_test = df_test["label"].values.astype(np.int64)

    x_train, x_val, y_train, y_val = train_test_split(
        x_all, y_all, test_size=0.15, random_state=seed, stratify=y_all
    )
    num_classes = int(np.max(y_all)) + 1
    return (x_train, y_train), (x_val, y_val), (x_test, y_test), num_classes


def build_loaders(data_dir: Path, batch_size: int, seed: int = 42):
    train, val, test, num_classes = load_data(data_dir, seed)
    ds_train = SignDataset(*train)
    ds_val = SignDataset(*val)
    ds_test = SignDataset(*test)
    train_loader = DataLoader(ds_train, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(ds_val, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(ds_test, batch_size=batch_size, shuffle=False, num_workers=0)
    return train_loader, val_loader, test_loader, num_classes
