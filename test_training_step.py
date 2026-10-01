import torch
import torch.nn.functional as F

from models.mcnn import MCNN
from utils.data_loader import CrowdDataset


print("=" * 70)
print("ONE-STEP TRAINING TEST")
print("=" * 70)

# ---------------------------------------------------------
# 1. Device
# ---------------------------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

# ---------------------------------------------------------
# 2. Dataset
# ---------------------------------------------------------

dataset = CrowdDataset(
    root="data/ShanghaiTech",
    part="B",
    split="train",
    image_size=512,
    augment=True,
)

print("Dataset size:", len(dataset))

# ---------------------------------------------------------
# 3. Get ONE training sample
# ---------------------------------------------------------

image, target = dataset[0]

print("\nOriginal image tensor:")
print(image.shape)

print("Original density tensor:")
print(target.shape)

print("Ground-truth count:")
print(float(target.sum()))

# Add batch dimension
image = image.unsqueeze(0).to(device)
target = target.unsqueeze(0).to(device)

print("\nBatch image:")
print(image.shape)

print("Batch target:")
print(target.shape)

# ---------------------------------------------------------
# 4. Create model
# ---------------------------------------------------------

print("\nCreating MCNN...")

model = MCNN(
    pretrained=True,
    freeze_backbone=False
).to(device)

model.train()

print("MCNN ready.")

# ---------------------------------------------------------
# 5. Optimizer
# ---------------------------------------------------------

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-5,
    weight_decay=1e-4,
)

# ---------------------------------------------------------
# 6. Forward pass
# ---------------------------------------------------------

print("\nRunning forward pass...")

optimizer.zero_grad()

prediction, attention = model(image)

print("Prediction shape:")
print(prediction.shape)

# ---------------------------------------------------------
# 7. Density loss
# ---------------------------------------------------------

density_loss = F.mse_loss(
    prediction,
    target
)

# ---------------------------------------------------------
# 8. Count loss
# ---------------------------------------------------------

target_count = target.sum(
    dim=(1, 2, 3)
)

predicted_count = prediction.sum(
    dim=(1, 2, 3)
)

count_loss = F.l1_loss(
    predicted_count,
    target_count
)

# ---------------------------------------------------------
# 9. Combined loss
# ---------------------------------------------------------

loss = density_loss + 0.001 * count_loss

print("\nDensity loss:")
print(float(density_loss))

print("Count loss:")
print(float(count_loss))

print("Total loss:")
print(float(loss))

# ---------------------------------------------------------
# 10. Backpropagation
# ---------------------------------------------------------

print("\nRunning backward pass...")

loss.backward()

print("Backward pass completed.")

# ---------------------------------------------------------
# 11. Optimizer step
# ---------------------------------------------------------

print("\nRunning optimizer step...")

optimizer.step()

print("Optimizer step completed.")

# ---------------------------------------------------------
# 12. Final
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ONE-STEP TRAINING TEST PASSED")
print("=" * 70)