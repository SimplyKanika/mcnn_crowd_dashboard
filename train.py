"""Training entry point for the crowd counting model."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader

from models.mcnn import MCNN
from utils.data_loader import CrowdDataset
from utils.metrics import MetricTracker

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_ROOT = PROJECT_ROOT / "data" / "ShanghaiTech"
DEFAULT_CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"


def build_dataloaders(root: Path, part: str, batch_size: int = 4, image_size: int = 512):
    train_dataset = CrowdDataset(root=root, part=part, split="train", image_size=image_size, augment=False)
    test_dataset = CrowdDataset(root=root, part=part, split="test", image_size=image_size, augment=False)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    return train_loader, test_loader


def evaluate(model: torch.nn.Module, loader: DataLoader, device: torch.device) -> tuple[float, float]:
    tracker = MetricTracker()
    model.eval()
    with torch.no_grad():
        for images, targets in loader:
            images = images.to(device)
            targets = targets.to(device)
            predictions, _ = model(images)
            counts_true = targets.sum(dim=(1, 2, 3))
            counts_pred = predictions.sum(dim=(1, 2, 3))
            tracker.update(counts_true, counts_pred)
    return tracker.compute()


def train(args: argparse.Namespace) -> None:
    if torch.cuda.is_available() and args.device == "cuda":
        torch.backends.cudnn.benchmark = True

    device = torch.device(args.device if torch.cuda.is_available() and args.device == "cuda" else "cpu")
    DEFAULT_CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    train_loader, test_loader = build_dataloaders(
        root=args.data_root,
        part=args.part,
        batch_size=args.batch_size,
        image_size=args.image_size,
    )

    model = MCNN(pretrained=True, freeze_backbone=args.freeze_backbone).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(1, args.epochs))

    best_mae = float("inf")
    for epoch in range(args.epochs):
        model.train()
        train_loss = 0.0
        for images, targets in train_loader:
            images = images.to(device)
            targets = targets.to(device)
            optimizer.zero_grad()
            predictions, _ = model(images)
            density_loss = F.mse_loss(predictions, targets)
            target_counts = targets.sum(dim=(1, 2, 3))
            pred_counts = predictions.sum(dim=(1, 2, 3))
            count_loss = F.l1_loss(pred_counts, target_counts)
            loss = density_loss + args.count_loss_weight * count_loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item() * images.size(0)

        scheduler.step()
        mae, rmse = evaluate(model, test_loader, device)
        train_loss /= len(train_loader.dataset)
        print(f"Epoch {epoch + 1}/{args.epochs} | train_loss={train_loss:.4f} | test_mae={mae:.4f} | test_rmse={rmse:.4f}")

        if mae < best_mae:
            best_mae = mae
            checkpoint_path = DEFAULT_CHECKPOINT_DIR / f"part_{args.part.lower()}_mcnn.pth"
            torch.save({"model_state": model.state_dict(), "epoch": epoch + 1, "mae": mae}, checkpoint_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the adaptive MCNN crowd estimator")
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--part", type=str, default="A", choices=["A", "B"], help="ShanghaiTech part to train on")
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--image-size", type=int, default=512)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--count-loss-weight", type=float, default=0.01, help="Weight for the L1 count loss term used alongside density MSE")
    parser.add_argument("--freeze-backbone", action="store_true")
    parser.add_argument("--device", type=str, default="cuda")
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
