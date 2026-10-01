"""Evaluation script for the crowd counting model."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from models.mcnn import MCNN
from train import build_dataloaders
from utils.metrics import MetricTracker

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_ROOT = PROJECT_ROOT / "data" / "ShanghaiTech"
DEFAULT_CHECKPOINT = PROJECT_ROOT / "checkpoints" / "part_a_mcnn.pth"


def evaluate_checkpoint(path: Path, data_root: Path, part: str, batch_size: int, image_size: int) -> tuple[float, float]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MCNN(pretrained=False).to(device)
    state = torch.load(path, map_location=device)
    if isinstance(state, dict) and "model_state" in state:
        state = state["model_state"]
    model.load_state_dict(state)
    model.eval()

    _, test_loader = build_dataloaders(root=data_root, part=part, batch_size=batch_size, image_size=image_size)
    tracker = MetricTracker()
    with torch.no_grad():
        for images, targets in test_loader:
            images = images.to(device)
            targets = targets.to(device)
            predictions, _ = model(images)
            counts_true = targets.sum(dim=(1, 2, 3))
            counts_pred = predictions.sum(dim=(1, 2, 3))
            tracker.update(counts_true, counts_pred)
    return tracker.compute()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate the crowd regression model")
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--part", type=str, default="A", choices=["A", "B"], help="ShanghaiTech part to evaluate")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--image-size", type=int, default=512)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    mae, rmse = evaluate_checkpoint(
    args.checkpoint,
    args.data_root,
    args.part,
    args.batch_size,
    args.image_size
)

print(
    f"MAE={mae:.4f} | RMSE={rmse:.4f}"
)
