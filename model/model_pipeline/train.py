from __future__ import annotations

import copy

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from model_pipeline.model import Genome, build_model, genome_to_hparams


def train_one_epoch(model: nn.Module, loader: DataLoader, optimizer, criterion, device: torch.device):
    model.train()
    total, correct, loss_sum = 0, 0, 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = model(xb)
        loss = criterion(logits, yb)
        loss.backward()
        optimizer.step()
        total += xb.size(0)
        loss_sum += loss.item() * xb.size(0)
        correct += (logits.argmax(1) == yb).sum().item()
    return loss_sum / total, correct / total


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, criterion, device: torch.device):
    model.eval()
    total, correct, loss_sum = 0, 0, 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
        loss = criterion(logits, yb)
        total += xb.size(0)
        loss_sum += loss.item() * xb.size(0)
        correct += (logits.argmax(1) == yb).sum().item()
    return loss_sum / total, correct / total


def train_final(
    genome: Genome,
    num_classes: int,
    train_loader: DataLoader,
    val_loader: DataLoader,
    device: torch.device,
    epochs: int = 30,
    patience: int = 6,
):
    model = build_model(genome, num_classes, device)
    hparams = genome_to_hparams(genome)
    optimizer = torch.optim.Adam(model.parameters(), lr=hparams["lr"])
    criterion = nn.CrossEntropyLoss()
    history = {"train_acc": [], "val_acc": []}

    best_val = -1.0
    best_state = None
    stale = 0
    for _ in range(epochs):
        _, tr_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        _, val_acc = evaluate(model, val_loader, criterion, device)
        history["train_acc"].append(tr_acc)
        history["val_acc"].append(val_acc)
        if val_acc > best_val + 1e-4:
            best_val = val_acc
            stale = 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            stale += 1
            if stale >= patience:
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, history, best_val
