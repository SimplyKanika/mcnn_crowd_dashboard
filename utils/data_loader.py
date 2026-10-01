"""Dataset and preprocessing utilities for ShanghaiTech crowd density regression.

Important:
- Image resizing preserves aspect ratio.
- Density-map resizing preserves total density/count.
- Zero padding does not change the crowd count.
- Data augmentation keeps image, density map, and annotations aligned.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Optional, Union

import cv2
import numpy as np
import torch
from scipy.io import loadmat
from torch.utils.data import Dataset


MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


# ---------------------------------------------------------------------
# Ground-truth annotation loading
# ---------------------------------------------------------------------

def _extract_locations(mat_path: Path) -> np.ndarray:
    """Extract head locations from ShanghaiTech-style .mat annotations."""

    data = loadmat(mat_path)

    def walk(node: object) -> Optional[np.ndarray]:

        if isinstance(node, dict):
            for key in ("location", "points", "annPoints"):
                if key in node:
                    arr = np.asarray(node[key])

                    if arr.size == 0:
                        return np.empty((0, 2), dtype=np.float32)

                    if arr.ndim == 1:
                        return arr.reshape(-1, 2).astype(np.float32)

                    if arr.ndim >= 2 and arr.shape[-1] == 2:
                        return arr.reshape(-1, 2).astype(np.float32)

            for value in node.values():
                result = walk(value)
                if result is not None:
                    return result

        elif isinstance(node, (tuple, list)):
            for item in node:
                result = walk(item)
                if result is not None:
                    return result

        elif isinstance(node, np.void):
            if getattr(node.dtype, "names", None):
                for key in ("location", "points", "annPoints"):
                    if key in node.dtype.names:
                        arr = np.asarray(node[key])

                        if arr.size == 0:
                            return np.empty((0, 2), dtype=np.float32)

                        if arr.ndim == 1:
                            return arr.reshape(-1, 2).astype(np.float32)

                        if arr.ndim >= 2 and arr.shape[-1] == 2:
                            return arr.reshape(-1, 2).astype(np.float32)

        elif isinstance(node, np.ndarray):

            if getattr(node.dtype, "names", None):
                for key in ("location", "points", "annPoints"):
                    if key in node.dtype.names:
                        arr = np.asarray(node[key])

                        if arr.size == 0:
                            return np.empty((0, 2), dtype=np.float32)

                        if arr.ndim == 1:
                            return arr.reshape(-1, 2).astype(np.float32)

                        if arr.ndim >= 2 and arr.shape[-1] == 2:
                            return arr.reshape(-1, 2).astype(np.float32)

            if node.dtype == object:
                for item in node.flat:
                    result = walk(item)
                    if result is not None:
                        return result

            elif node.ndim > 0 and node.size == 1:
                return walk(node.item())

            elif node.ndim >= 2 and node.shape[-1] == 2:
                return node.reshape(-1, 2).astype(np.float32)

        return None

    result = walk(data)

    if result is None:
        return np.empty((0, 2), dtype=np.float32)

    return result


# ---------------------------------------------------------------------
# Density-map generation
# ---------------------------------------------------------------------

def _build_density_map(
    points: np.ndarray,
    image_shape: tuple[int, int],
    part: str,
) -> np.ndarray:
    """Create a continuous density map whose sum equals point count."""

    height, width = image_shape

    density = np.zeros((height, width), dtype=np.float32)

    if points.size == 0:
        return density

    points = np.asarray(points, dtype=np.float32).reshape(-1, 2)

    # -------------------------------------------------------------
    # Adaptive sigma for Part A
    # Fixed sigma for Part B, matching the current project design.
    # -------------------------------------------------------------
    if part.upper() == "A":

        sigmas: list[float] = []

        for index, point in enumerate(points):

            other_points = np.delete(points, index, axis=0)

            if other_points.size == 0:
                sigmas.append(15.0)
                continue

            distances = np.linalg.norm(
                other_points - point,
                axis=1,
            )

            nearest = np.sort(distances)[:3]

            if nearest.size:
                average_distance = float(np.mean(nearest))
            else:
                average_distance = 15.0

            sigmas.append(
                max(0.3 * average_distance, 1.0)
            )

    else:
        sigmas = [15.0] * len(points)

    # -------------------------------------------------------------
    # Generate normalized Gaussian around each head point.
    # Every kernel contributes exactly 1 person.
    # -------------------------------------------------------------
    for point, sigma in zip(points, sigmas):

        sigma = max(float(sigma), 1.0)

        center_x = float(point[0])
        center_y = float(point[1])

        radius = int(math.ceil(4 * sigma))

        x_min = max(
            int(math.floor(center_x - radius)),
            0,
        )

        x_max = min(
            int(math.ceil(center_x + radius)),
            width - 1,
        )

        y_min = max(
            int(math.floor(center_y - radius)),
            0,
        )

        y_max = min(
            int(math.ceil(center_y + radius)),
            height - 1,
        )

        y_coords = np.arange(
            y_min,
            y_max + 1,
            dtype=np.float32,
        )

        x_coords = np.arange(
            x_min,
            x_max + 1,
            dtype=np.float32,
        )

        yy, xx = np.meshgrid(
            y_coords,
            x_coords,
            indexing="ij",
        )

        distance = (
            (xx - center_x) ** 2
            + (yy - center_y) ** 2
        )

        kernel = np.exp(
            -distance / (2.0 * sigma * sigma)
        ).astype(np.float32)

        kernel_sum = float(kernel.sum())

        if kernel_sum > 0:

            density[
                y_min:y_max + 1,
                x_min:x_max + 1,
            ] += kernel / kernel_sum

    # -------------------------------------------------------------
    # Final normalization.
    #
    # This guarantees:
    #
    #     density.sum() ~= number of annotated people
    #
    # -------------------------------------------------------------
    target_count = float(len(points))
    current_sum = float(density.sum())

    if target_count > 0 and current_sum > 0:
        density *= target_count / current_sum

    return density.astype(np.float32)


# ---------------------------------------------------------------------
# Image resizing
# ---------------------------------------------------------------------

def _calculate_resize_shape(
    height: int,
    width: int,
    image_size: int,
) -> tuple[int, int, float]:
    """Calculate aspect-ratio-preserving resize dimensions."""

    if height <= 0 or width <= 0:
        raise ValueError(
            f"Invalid image dimensions: {(height, width)}"
        )

    scale = min(
        image_size / float(max(height, width)),
        1.0,
    )

    new_height = max(
        1,
        int(round(height * scale)),
    )

    new_width = max(
        1,
        int(round(width * scale)),
    )

    return new_height, new_width, scale


def resize_and_pad_image(
    image: np.ndarray,
    image_size: int = 512,
) -> np.ndarray:
    """Resize an image while preserving aspect ratio and zero-pad."""

    height, width = image.shape[:2]

    new_height, new_width, _ = _calculate_resize_shape(
        height,
        width,
        image_size,
    )

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR,
    ).astype(np.float32)

    # Keep dimensions compatible with VGG/MCNN downsampling.
    target_height = min(
        image_size,
        int(math.ceil(new_height / 8.0) * 8),
    )

    target_width = min(
        image_size,
        int(math.ceil(new_width / 8.0) * 8),
    )

    pad_height = image_size - target_height
    pad_width = image_size - target_width

    top = pad_height // 2
    bottom = pad_height - top

    left = pad_width // 2
    right = pad_width - left

    # First pad resized content to the final canvas.
    padded = cv2.copyMakeBorder(
        resized,
        top,
        bottom,
        left,
        right,
        cv2.BORDER_CONSTANT,
        value=0.0,
    )

    # Safety check.
    if padded.shape[0] != image_size or padded.shape[1] != image_size:
        padded = cv2.resize(
            padded,
            (image_size, image_size),
            interpolation=cv2.INTER_LINEAR,
        )

    return padded.astype(np.float32)


# ---------------------------------------------------------------------
# Density-map resizing
# ---------------------------------------------------------------------

def resize_and_pad_density(
    density: np.ndarray,
    image_size: int = 512,
) -> np.ndarray:
    """Resize and pad a density map while preserving total count.

    This is intentionally separate from resize_and_pad_image().

    For a density map, the numerical values represent people-per-pixel.
    When spatial resolution changes, density values must be compensated
    so that:

        processed_density.sum() ~= original_density.sum()

    Zero padding itself does not change the count.
    """

    if density.ndim != 2:
        raise ValueError(
            f"Expected 2-D density map, got shape {density.shape}"
        )

    density = density.astype(np.float32)

    original_height, original_width = density.shape

    new_height, new_width, scale = _calculate_resize_shape(
        original_height,
        original_width,
        image_size,
    )

    # -------------------------------------------------------------
    # Resize spatial distribution.
    # -------------------------------------------------------------
    resized = cv2.resize(
        density,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR,
    ).astype(np.float32)

    # -------------------------------------------------------------
    # IMPORTANT:
    #
    # If the image dimensions are scaled by `scale`, pixel area
    # changes by approximately scale^2.
    #
    # Therefore density values must be compensated by 1/scale^2.
    # -------------------------------------------------------------
    if scale > 0:
        resized /= float(scale * scale)

    # -------------------------------------------------------------
    # Match image padding logic.
    # -------------------------------------------------------------
    target_height = min(
        image_size,
        int(math.ceil(new_height / 8.0) * 8),
    )

    target_width = min(
        image_size,
        int(math.ceil(new_width / 8.0) * 8),
    )

    pad_height = image_size - target_height
    pad_width = image_size - target_width

    top = pad_height // 2
    bottom = pad_height - top

    left = pad_width // 2
    right = pad_width - left

    padded = cv2.copyMakeBorder(
        resized,
        top,
        bottom,
        left,
        right,
        cv2.BORDER_CONSTANT,
        value=0.0,
    )

    # Safety resize.
    if padded.shape[0] != image_size or padded.shape[1] != image_size:
        padded = cv2.resize(
            padded,
            (image_size, image_size),
            interpolation=cv2.INTER_LINEAR,
        )

        # If the safety resize changes area, preserve total count.
        resized_sum = float(padded.sum())
        original_sum = float(density.sum())

        if resized_sum > 0 and original_sum > 0:
            padded *= original_sum / resized_sum

    # -------------------------------------------------------------
    # Final count preservation.
    #
    # This compensates for interpolation/truncation numerical
    # differences and guarantees that the target count is retained.
    # -------------------------------------------------------------
    original_sum = float(density.sum())
    processed_sum = float(padded.sum())

    if original_sum > 0 and processed_sum > 0:
        padded *= original_sum / processed_sum

    return padded.astype(np.float32)


# ---------------------------------------------------------------------
# Image preprocessing for inference
# ---------------------------------------------------------------------

def preprocess_image(
    image: Union[str, Path, np.ndarray],
    image_size: int = 512,
) -> torch.Tensor:
    """Normalize an RGB image using ImageNet statistics."""

    if isinstance(image, (str, Path)):

        image_array = cv2.imread(
            str(image),
            cv2.IMREAD_COLOR,
        )

        if image_array is None:
            raise FileNotFoundError(
                f"Could not read image: {image}"
            )

    else:
        image_array = image

        if image_array is None:
            raise ValueError("Input image is None.")

    # If input is BGR from OpenCV, convert to RGB.
    if image_array.ndim == 3 and image_array.shape[2] == 3:
        image_array = cv2.cvtColor(
            image_array,
            cv2.COLOR_BGR2RGB,
        )

    image_array = image_array.astype(np.float32)

    processed = resize_and_pad_image(
        image_array,
        image_size=image_size,
    )

    processed /= 255.0

    tensor = torch.from_numpy(
        processed.transpose(2, 0, 1)
    ).float()

    mean = torch.tensor(
        MEAN,
        dtype=torch.float32,
    ).view(3, 1, 1)

    std = torch.tensor(
        STD,
        dtype=torch.float32,
    ).view(3, 1, 1)

    tensor = (tensor - mean) / std

    return tensor


# ---------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------

class CrowdDataset(Dataset):
    """Dataset wrapper for ShanghaiTech train/test splits."""

    def __init__(
        self,
        root: Union[str, Path],
        part: str = "A",
        split: str = "train",
        image_size: int = 512,
        augment: bool = True,
    ) -> None:

        self.root = Path(root)
        self.part = part.upper()
        self.split = split.lower()
        self.image_size = image_size
        self.augment = augment and self.split == "train"

        self.image_dir = (
            self.root
            / f"part_{self.part.lower()}"
            / f"{self.split}_data"
            / "images"
        )

        self.ground_truth_dir = (
            self.root
            / f"part_{self.part.lower()}"
            / f"{self.split}_data"
            / "ground-truth"
        )

        self.image_paths = [
            path
            for path in sorted(self.image_dir.glob("*"))
            if path.suffix.lower()
            in {
                ".jpg",
                ".jpeg",
                ".png",
                ".bmp",
                ".tif",
                ".tiff",
            }
        ]

        if not self.image_paths:
            raise FileNotFoundError(
                f"No image files were found in {self.image_dir}. "
                f"Place the ShanghaiTech {self.part} "
                f"{self.split} data there before training."
            )

    def __len__(self) -> int:
        return len(self.image_paths)

    # -------------------------------------------------------------
    # Ground-truth file matching
    # -------------------------------------------------------------

    def _resolve_gt_path(
        self,
        image_path: Path,
    ) -> Path:

        pattern = re.compile(r"(\d+)")

        image_number = "".join(
            pattern.findall(image_path.stem)
        )

        for gt in sorted(
            self.ground_truth_dir.glob("*.mat")
        ):

            gt_number = "".join(
                pattern.findall(gt.stem)
            )

            if image_number and gt_number == image_number:
                return gt

        raise FileNotFoundError(
            f"Could not find matching ground-truth "
            f"file for {image_path}"
        )

    # -------------------------------------------------------------
    # Horizontal flip
    # -------------------------------------------------------------

    def _apply_horizontal_flip(
        self,
        image: np.ndarray,
        points: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:

        image = cv2.flip(image, 1)

        if points.size > 0:

            points = points.copy()

            width = image.shape[1]

            # x' = W - 1 - x
            points[:, 0] = (
                width - 1 - points[:, 0]
            )

        return image, points

    # -------------------------------------------------------------
    # Random crop
    # -------------------------------------------------------------

    def _random_crop(
        self,
        image: np.ndarray,
        points: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:

        height, width = image.shape[:2]

        crop_size = min(
            self.image_size,
            height,
            width,
        )

        if crop_size <= 0:
            return image, points

        if height > crop_size:
            top = np.random.randint(
                0,
                height - crop_size + 1,
            )
        else:
            top = 0

        if width > crop_size:
            left = np.random.randint(
                0,
                width - crop_size + 1,
            )
        else:
            left = 0

        bottom = top + crop_size
        right = left + crop_size

        cropped_image = image[
            top:bottom,
            left:right,
        ]

        if points.size == 0:
            cropped_points = np.empty(
                (0, 2),
                dtype=np.float32,
            )
        else:

            points = points.copy()

            inside = (
                (points[:, 0] >= left)
                & (points[:, 0] < right)
                & (points[:, 1] >= top)
                & (points[:, 1] < bottom)
            )

            cropped_points = points[inside]

            cropped_points[:, 0] -= left
            cropped_points[:, 1] -= top

        return cropped_image, cropped_points

    # -------------------------------------------------------------
    # Complete preprocessing
    # -------------------------------------------------------------

    def _prepare_image_and_density(
        self,
        image_path: Path,
    ) -> tuple[np.ndarray, np.ndarray]:

        image = cv2.imread(
            str(image_path),
            cv2.IMREAD_COLOR,
        )

        if image is None:
            raise FileNotFoundError(
                f"Could not read image: {image_path}"
            )

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        gt_path = self._resolve_gt_path(
            image_path
        )

        points = _extract_locations(
            gt_path
        )

        # ---------------------------------------------------------
        # Apply geometric augmentation to image + points FIRST.
        #
        # Density map is generated AFTER augmentation so that
        # annotations remain perfectly aligned.
        # ---------------------------------------------------------

        if self.augment:

            if np.random.rand() < 0.5:
                image, points = self._apply_horizontal_flip(
                    image,
                    points,
                )

            image, points = self._random_crop(
                image,
                points,
            )

        # ---------------------------------------------------------
        # Generate density map from the FINAL point locations.
        # ---------------------------------------------------------

        height, width = image.shape[:2]

        density = _build_density_map(
            points,
            (height, width),
            part=self.part,
        )

        # ---------------------------------------------------------
        # Resize image and density separately.
        # ---------------------------------------------------------

        image_resized = resize_and_pad_image(
            image,
            image_size=self.image_size,
        )

        density_resized = resize_and_pad_density(
            density,
            image_size=self.image_size,
        )

        return (
            image_resized,
            density_resized,
        )

    # -------------------------------------------------------------
    # PyTorch output
    # -------------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:

        image_path = self.image_paths[index]

        image, density = (
            self._prepare_image_and_density(
                image_path
            )
        )

        image = (
            image.astype(np.float32) / 255.0
        )

        density = density.astype(
            np.float32
        )

        image_tensor = torch.from_numpy(
            image.transpose(2, 0, 1)
        ).float()

        density_tensor = torch.from_numpy(
            density
        ).float().unsqueeze(0)

        mean = torch.tensor(
            MEAN,
            dtype=torch.float32,
        ).view(3, 1, 1)

        std = torch.tensor(
            STD,
            dtype=torch.float32,
        ).view(3, 1, 1)

        image_tensor = (
            image_tensor - mean
        ) / std

        return (
            image_tensor,
            density_tensor,
        )