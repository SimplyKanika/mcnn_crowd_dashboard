"""Multi-column crowd density estimation network built on a shared VGG frontend."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from .acm import AdaptiveCollationModule
from .backbone import build_shared_frontend


class MCNN(nn.Module):
    """A three-column branch network with adaptive channel-wise collation."""

    def __init__(self, pretrained: bool = True, freeze_backbone: bool = False) -> None:
        super().__init__()
        self.shared_frontend = build_shared_frontend(pretrained=pretrained, freeze=freeze_backbone)

        self.column1 = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=3, padding=4, dilation=4),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=4, dilation=4),
            nn.ReLU(inplace=True),
        )
        self.column2 = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=3, padding=2, dilation=2),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=2, dilation=2),
            nn.ReLU(inplace=True),
        )
        self.column3 = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=3, padding=1, dilation=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1, dilation=1),
            nn.ReLU(inplace=True),
        )

        self.acm = AdaptiveCollationModule(channels=256)
        self.regressor = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 1, kernel_size=1),
        )

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        shared_features = self.shared_frontend(x)
        column_outputs = (
            self.column1(shared_features),
            self.column2(shared_features),
            self.column3(shared_features),
        )
        collated_features, attention_weights = self.acm(column_outputs)
        density_map = self.regressor(collated_features)
        density_map = F.interpolate(density_map, size=x.shape[-2:], mode="bilinear", align_corners=False)
        density_map = F.relu(density_map)
        return density_map, attention_weights
