from pathlib import Path

import numpy as np

from utils.data_loader import (
    CrowdDataset,
    _extract_locations,
    _build_density_map,
)


PROJECT_ROOT = Path(__file__).resolve().parent

DATA_ROOT = (
    PROJECT_ROOT
    / "data"
    / "ShanghaiTech"
)


dataset = CrowdDataset(
    root=DATA_ROOT,
    part="A",
    split="test",
    image_size=256,
    augment=False,
)


print("=" * 70)
print("DENSITY MAP COUNT PRESERVATION TEST")
print("=" * 70)


num_samples = min(20, len(dataset))

ratios = []


for index in range(num_samples):

    image_path = dataset.image_paths[index]

    gt_path = dataset._resolve_gt_path(
        image_path
    )

    points = _extract_locations(
        gt_path
    )

    original_count = float(
        len(points)
    )

    # Get processed target.
    _, processed_density = (
        dataset._prepare_image_and_density(
            image_path
        )
    )

    processed_count = float(
        processed_density.sum()
    )

    if original_count > 0:
        ratio = (
            processed_count
            / original_count
        )
    else:
        ratio = 1.0

    ratios.append(ratio)

    print(
        f"{index + 1:02d}. "
        f"{image_path.name:20s} | "
        f"GT={original_count:8.2f} | "
        f"Processed={processed_count:8.2f} | "
        f"Ratio={ratio:.4f}"
    )


ratios = np.asarray(
    ratios,
    dtype=np.float32,
)


print("\n" + "=" * 70)

print(
    f"Mean ratio   : {ratios.mean():.4f}"
)

print(
    f"Min ratio    : {ratios.min():.4f}"
)

print(
    f"Max ratio    : {ratios.max():.4f}"
)

print("=" * 70)


if (
    ratios.mean() >= 0.98
    and ratios.mean() <= 1.02
):
    print(
        "\nPASS: Density-map count is being preserved."
    )
else:
    print(
        "\nWARNING: Density-map count is still not "
        "being preserved correctly."
    )