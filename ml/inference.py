import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from .mcnn import MCNN


BASE_DIR = Path(__file__).resolve().parent
CHECKPOINT_PATH = BASE_DIR / "part_b_mcnn.pth"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL = None


def load_model():
    global MODEL

    if MODEL is None:
        model = MCNN(pretrained=False)

        checkpoint = torch.load(
            CHECKPOINT_PATH,
            map_location=DEVICE,
        )

        model.load_state_dict(checkpoint["model_state"])
        model.to(DEVICE)
        model.eval()

        MODEL = model

    return MODEL


def preprocess_image(image: Image.Image):
    """Preprocess input using the exact same OpenCV pipeline as training."""

    import cv2

    image = np.asarray(image.convert("RGB"))

    original_height, original_width = image.shape[:2]
    target_size = 512

    scale = min(
        target_size / float(max(original_height, original_width)),
        1.0,
    )

    new_height = max(
        1,
        int(round(original_height * scale)),
    )

    new_width = max(
        1,
        int(round(original_width * scale)),
    )

    # EXACTLY the same interpolation used during training.
    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR,
    ).astype(np.float32)

    # EXACTLY the same 8-pixel alignment used during training.
    target_height = min(
        target_size,
        int(np.ceil(new_height / 8.0) * 8),
    )

    target_width = min(
        target_size,
        int(np.ceil(new_width / 8.0) * 8),
    )

    pad_height = target_size - target_height
    pad_width = target_size - target_width

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

    # Same safety check as training.
    if padded.shape[0] != target_size or padded.shape[1] != target_size:
        padded = cv2.resize(
            padded,
            (target_size, target_size),
            interpolation=cv2.INTER_LINEAR,
        )

    # EXACTLY the same normalization as training.
    padded = padded.astype(np.float32) / 255.0

    mean = np.array(
        [0.485, 0.456, 0.406],
        dtype=np.float32,
    ).reshape(1, 1, 3)

    std = np.array(
        [0.229, 0.224, 0.225],
        dtype=np.float32,
    ).reshape(1, 1, 3)

    padded = (padded - mean) / std

    tensor = torch.from_numpy(
        padded.transpose(2, 0, 1)
    ).float().unsqueeze(0)

    return tensor, (original_width, original_height)


@torch.inference_mode()
def predict(image: Image.Image):
    model = load_model()

    input_tensor, original_size = preprocess_image(image)

    input_tensor = input_tensor.to(DEVICE)

    start_time = time.perf_counter()

    density_map, attention_weights = model(input_tensor)

    inference_time = time.perf_counter() - start_time

    # crowd_count = float(density_map.sum().item())

    # if crowd_count < 50:
    #     density_level = "Low"
    # elif crowd_count < 150:
    #     density_level = "Medium"
    # elif crowd_count < 300:
    #     density_level = "High"
    # else:
    #     density_level = "Very High"

    # attention = attention_weights[0].detach().cpu().numpy()

    # density_map_np = density_map[0, 0].detach().cpu().numpy()
   # The trained MCNN checkpoint outputs a 512x512 density map.
    # Use the raw density map directly for the crowd count.
    density_map_np = density_map[0, 0].detach().cpu().numpy()

    crowd_count = float(density_map_np.sum())

    attention = attention_weights[0].detach().cpu().numpy()

    # Normalize ONLY for visualization, matching the dashboard's
    # dummy density-map structure. The raw density values are
    # never modified for counting.
    max_density = float(density_map_np.max())

    if max_density > 0:
        density_map_np = (
            density_map_np / max_density
        ).astype(np.float32)
    else:
        density_map_np = np.zeros_like(
            density_map_np,
            dtype=np.float32,
        )

    if crowd_count < 50:
        density_level = "Low"
    elif crowd_count < 150:
        density_level = "Medium"
    elif crowd_count < 300:
        density_level = "High"
    else:
        density_level = "Very High"

    return {
        "crowd_count": max(0, round(crowd_count)),
        "model_version": "Enhanced MCNN — Part B",
        "density_level": density_level,
        "raw_count": crowd_count,
        "density_map": density_map_np,
        "attention_weights": attention.tolist(),
        "inference_time": inference_time,
        "device": str(DEVICE),
        "input_resolution": f"{original_size[0]} × {original_size[1]}",
        "density_map_resolution": (
            f"{density_map_np.shape[1]} × {density_map_np.shape[0]}"
        ),
    }
