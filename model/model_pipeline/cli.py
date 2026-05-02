from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from model_pipeline.data import build_loaders
from model_pipeline.export import export_artifacts, export_torchscript
from model_pipeline.infer import predict_image
from model_pipeline.model import genome_to_hparams
from model_pipeline.search_ga import run_ga
from model_pipeline.train import evaluate, train_final

LETTERS_SIGN = list("ABCDEFGHIKLMNOPQRSTUVWXY")


def cmd_search(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader, _, num_classes = build_loaders(
        Path(args.data_dir), batch_size=args.batch_size, seed=args.seed
    )
    best, history_best, history_mean = run_ga(
        train_loader,
        val_loader,
        num_classes,
        device=device,
        pop_size=args.pop_size,
        generations=args.generations,
        epochs_per_eval=args.epochs_per_eval,
        seed=args.seed,
    )
    print("Best genome:", best)
    print("Best hparams:", genome_to_hparams(best))
    print("History best:", history_best)
    print("History mean:", history_mean)


def cmd_train_final(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader, test_loader, num_classes = build_loaders(
        Path(args.data_dir), batch_size=args.batch_size, seed=args.seed
    )
    from model_pipeline.model import Genome

    genome = Genome(*args.genome)
    model, _, val_best = train_final(
        genome, num_classes, train_loader, val_loader, device, args.epochs, args.patience
    )
    criterion = torch.nn.CrossEntropyLoss()
    _, test_acc = evaluate(model, test_loader, criterion, device)
    hparams = genome_to_hparams(genome)
    metadata = {
        "num_classes": num_classes,
        "hparams": hparams,
        "val_best_acc": val_best,
        "test_acc": test_acc,
    }
    export_artifacts(model.cpu(), Path(args.output_dir), LETTERS_SIGN, metadata)
    export_torchscript(model.cpu(), Path(args.output_dir))
    print(json.dumps(metadata, indent=2))


def cmd_infer(args):
    result = predict_image(Path(args.image_path), Path(args.artifacts_dir))
    print(json.dumps(result, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="Sign language training pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search")
    search.add_argument("--data-dir", required=True)
    search.add_argument("--batch-size", type=int, default=128)
    search.add_argument("--seed", type=int, default=42)
    search.add_argument("--pop-size", type=int, default=4)
    search.add_argument("--generations", type=int, default=3)
    search.add_argument("--epochs-per-eval", type=int, default=2)
    search.set_defaults(func=cmd_search)

    train_cmd = sub.add_parser("train-final")
    train_cmd.add_argument("--data-dir", required=True)
    train_cmd.add_argument("--output-dir", default="model/artifacts")
    train_cmd.add_argument("--batch-size", type=int, default=128)
    train_cmd.add_argument("--seed", type=int, default=42)
    train_cmd.add_argument("--epochs", type=int, default=30)
    train_cmd.add_argument("--patience", type=int, default=6)
    train_cmd.add_argument("--genome", type=int, nargs=5, required=True)
    train_cmd.set_defaults(func=cmd_train_final)

    infer = sub.add_parser("infer")
    infer.add_argument("--image-path", required=True)
    infer.add_argument("--artifacts-dir", default="model/artifacts")
    infer.set_defaults(func=cmd_infer)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
