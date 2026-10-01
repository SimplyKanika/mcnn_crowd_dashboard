"""Adaptive collation module that dynamically weights branch outputs."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class AdaptiveCollationModule(nn.Module):
    """Apply a squeeze-and-excitation style gating over three columns."""

    def __init__(self, channels: int, bottleneck: int = 64) -> None:
        super().__init__()
        self.squeeze = nn.AdaptiveAvgPool2d(1)
        self.fc1 = nn.Linear(channels * 3, bottleneck)
        self.fc2 = nn.Linear(bottleneck, 3)

    def forward(self, columns: tuple[torch.Tensor, torch.Tensor, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor]:
        if len(columns) != 3:
            raise ValueError("AdaptiveCollationModule expects three column outputs")

        stacked_columns = torch.stack(columns, dim=1)
        squeezed = self.squeeze(stacked_columns).flatten(1)
        gate_logits = self.fc2(F.relu(self.fc1(squeezed)))
        attention_weights = torch.softmax(gate_logits, dim=1)

        weighted_columns = []
        for index, column in enumerate(columns):
            weight = attention_weights[:, index:index + 1].view(-1, 1, 1, 1)
            weighted_columns.append(column * weight)

        collated = weighted_columns[0] + weighted_columns[1] + weighted_columns[2]
        return collated, attention_weights
