"""Metric utilities for crowd counting.

Provides:
- MAE  : Mean Absolute Error
- MSE  : Mean Squared Error
- RMSE : Root Mean Squared Error

Metrics are accumulated per image using predicted and ground-truth
crowd counts.
"""

from __future__ import annotations

import math

import torch


class MetricTracker:
    """Accumulate crowd-count MAE, MSE and RMSE."""

    def __init__(self) -> None:
        self.count = 0
        self.mae_sum = 0.0
        self.mse_sum = 0.0

    def reset(self) -> None:
        """Reset all accumulated statistics."""

        self.count = 0
        self.mae_sum = 0.0
        self.mse_sum = 0.0

    def update(
        self,
        targets: torch.Tensor,
        predictions: torch.Tensor,
    ) -> None:
        """Add a batch of ground-truth and predicted counts.

        Parameters
        ----------
        targets:
            Tensor containing one ground-truth count per image.

        predictions:
            Tensor containing one predicted count per image.
        """

        targets = targets.detach().reshape(-1).float()
        predictions = predictions.detach().reshape(-1).float()

        if targets.numel() != predictions.numel():
            raise ValueError(
                "Targets and predictions must contain the same "
                f"number of values. Got "
                f"{targets.numel()} targets and "
                f"{predictions.numel()} predictions."
            )

        errors = targets - predictions

        self.mae_sum += float(
            torch.abs(errors).sum().item()
        )

        self.mse_sum += float(
            torch.square(errors).sum().item()
        )

        self.count += int(
            targets.numel()
        )

    def compute(
        self,
    ) -> tuple[float, float]:
        """Return MAE and RMSE.

        Returns
        -------
        mae:
            Mean Absolute Error.

        rmse:
            Root Mean Squared Error.
        """

        if self.count == 0:
            return 0.0, 0.0

        mae = (
            self.mae_sum / self.count
        )

        mse = (
            self.mse_sum / self.count
        )

        rmse = math.sqrt(mse)

        return mae, rmse

    def compute_with_mse(
        self,
    ) -> tuple[float, float, float]:
        """Return MAE, MSE and RMSE.

        Useful when all three metrics are required.
        """

        if self.count == 0:
            return 0.0, 0.0, 0.0

        mae = (
            self.mae_sum / self.count
        )

        mse = (
            self.mse_sum / self.count
        )

        rmse = math.sqrt(mse)

        return mae, mse, rmse