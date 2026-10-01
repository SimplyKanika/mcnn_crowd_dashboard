import torch
from pathlib import Path
from models.mcnn import MCNN
from utils.data_loader import CrowdDataset
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
CHECKPOINT_PATH = CHECKPOINT_DIR / "part_a_mcnn.pth"

def load_model(device):
    model = MCNN(pretrained=True).to(device)
    if CHECKPOINT_PATH.exists():
        ckpt = torch.load(CHECKPOINT_PATH, map_location=device)
        model.load_state_dict(ckpt["model_state"], strict=False)
        print(f"Loaded checkpoint: {CHECKPOINT_PATH}")
    else:
        print("No checkpoint found; using randomly initialized model")
    model.eval()
    return model


def run_diagnostics(device_name='cuda'):
    device = torch.device(device_name if torch.cuda.is_available() and device_name == 'cuda' else 'cpu')
    model = load_model(device)
    dataset = CrowdDataset(root=PROJECT_ROOT / 'data' / 'ShanghaiTech', part='A', split='test', image_size=256, augment=False)

    errors = []
    true_counts = []
    pred_counts = []
    density_sum_ratios = []
    paths = []

    loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)
    with torch.no_grad():
        for idx, (image, target) in enumerate(loader):
            image = image.to(device)
            target = target.to(device)
            pred, _ = model(image)
            true_count = float(target.sum().item())
            pred_count = float(pred.sum().item())
            err = abs(true_count - pred_count)
            errors.append(err)
            true_counts.append(true_count)
            pred_counts.append(pred_count)
            # compute density resized sum directly from dataset prepared density to see preservation
            # call internal helper to get resized density
            img_path = dataset.image_paths[idx]
            _, density_resized = dataset._prepare_image_and_density(img_path)
            density_sum = float(density_resized.sum())
            ratio = density_sum / true_count if true_count > 0 else 0.0
            density_sum_ratios.append(ratio)
            paths.append(str(img_path))

    errors = np.array(errors)
    true_counts = np.array(true_counts)
    pred_counts = np.array(pred_counts)
    density_sum_ratios = np.array(density_sum_ratios)

    def print_stat(name, arr):
        print(f"{name}: mean={arr.mean():.4f}, median={np.median(arr):.4f}, std={arr.std():.4f}, min={arr.min():.4f}, max={arr.max():.4f}")

    print_stat('abs_error', errors)
    print_stat('true_counts', true_counts)
    print_stat('pred_counts', pred_counts)
    print_stat('density_sum_ratio', density_sum_ratios)

    # show top 10 worst
    worst_idx = np.argsort(-errors)[:10]
    print('\nTop 10 worst predictions:')
    for i in worst_idx:
        print(f"{paths[i]} | true={true_counts[i]:.1f} pred={pred_counts[i]:.1f} err={errors[i]:.1f} density_sum_ratio={density_sum_ratios[i]:.3f}")

if __name__ == '__main__':
    run_diagnostics('cuda')
