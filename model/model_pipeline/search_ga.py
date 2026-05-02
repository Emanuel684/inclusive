from __future__ import annotations

import random

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from model_pipeline.model import clone, crossover, mutate, random_genome
from model_pipeline.train import evaluate, train_one_epoch
from model_pipeline.model import build_model, genome_to_hparams, Genome


def _fitness(
    genome: Genome,
    num_classes: int,
    train_loader: DataLoader,
    val_loader: DataLoader,
    device: torch.device,
    epochs: int,
) -> float:
    model = build_model(genome, num_classes, device)
    h = genome_to_hparams(genome)
    optimizer = torch.optim.Adam(model.parameters(), lr=h["lr"])
    criterion = nn.CrossEntropyLoss()
    best = 0.0
    for _ in range(epochs):
        train_one_epoch(model, train_loader, optimizer, criterion, device)
        _, val_acc = evaluate(model, val_loader, criterion, device)
        best = max(best, val_acc)
    return float(best)


def _tournament(population: list[Genome], fitness: list[float], k: int, rng: random.Random) -> Genome:
    idxs = rng.sample(range(len(population)), k=k)
    best_i = max(idxs, key=lambda idx: fitness[idx])
    return clone(population[best_i])


def run_ga(
    train_loader: DataLoader,
    val_loader: DataLoader,
    num_classes: int,
    device: torch.device,
    pop_size: int = 4,
    generations: int = 3,
    epochs_per_eval: int = 2,
    mutation_rate: float = 0.25,
    crossover_rate: float = 0.85,
    tournament_k: int = 3,
    seed: int = 42,
):
    rng = random.Random(seed)
    population = [random_genome(rng) for _ in range(pop_size)]
    best = clone(population[0])
    best_fit = -1.0
    history_best: list[float] = []
    history_mean: list[float] = []

    for _ in range(generations):
        fitness = [
            _fitness(g, num_classes, train_loader, val_loader, device, epochs_per_eval)
            for g in population
        ]
        current_best = max(fitness)
        current_mean = float(np.mean(fitness))
        history_best.append(current_best)
        history_mean.append(current_mean)
        if current_best > best_fit:
            best_fit = current_best
            best = clone(population[int(np.argmax(fitness))])

        next_population: list[Genome] = [clone(population[int(np.argmax(fitness))])]
        while len(next_population) < pop_size:
            p1 = _tournament(population, fitness, tournament_k, rng)
            p2 = _tournament(population, fitness, tournament_k, rng)
            if rng.random() < crossover_rate:
                c1, c2 = crossover(p1, p2, rng)
            else:
                c1, c2 = clone(p1), clone(p2)
            next_population.append(mutate(c1, mutation_rate, rng))
            if len(next_population) < pop_size:
                next_population.append(mutate(c2, mutation_rate, rng))
        population = next_population

    return best, history_best, history_mean
