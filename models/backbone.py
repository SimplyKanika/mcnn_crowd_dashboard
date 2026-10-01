"""Shared VGG-16 frontend used as the low-to-mid level feature extractor."""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn
from torchvision import models

try:
    from torchvision.models import VGG16_Weights  # type: ignore
except ImportError:  # pragma: no cover - old torchvision compatibility
    VGG16_Weights = None  # type: ignore


class SharedFrontend(nn.Module):
    """A truncated VGG-16 backbone ending before the pool4 layer."""

    def __init__(self, pretrained: bool = True) -> None:
        super().__init__()
        weights = None
        if pretrained and VGG16_Weights is not None:
            weights = VGG16_Weights.DEFAULT

        vgg = models.vgg16(weights=weights)
        self.features = nn.Sequential(*list(vgg.features.children())[:23])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.features(x)


def build_shared_frontend(
    pretrained: bool = True,
    freeze: bool = False,
    device: Optional[torch.device] = None,
) -> nn.Module:
    """Create the shared VGG-16 frontend module."""

    module = SharedFrontend(pretrained=pretrained)
    if freeze:
        for parameter in module.parameters():
            parameter.requires_grad = False
    if device is not None:
        module.to(device)
    return module
