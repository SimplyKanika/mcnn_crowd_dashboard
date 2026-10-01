import torch
import torch.nn.functional as F

from models.mcnn import MCNN
from utils.data_loader import CrowdDataset


print("=" * 70)
print("MCNN SINGLE-IMAGE OVERFIT TEST")
print("=" * 70)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# ---------------------------------------------------------
# Load ONE training sample
# ---------------------------------------------------------

dataset = CrowdDataset(
    root="data/ShanghaiTech",
    part="B",
    split="train",
    image_size=512,
    augment=False,
)

image, target = dataset[0]

print("\nImage shape:")
print(image.shape)

print("Target shape:")
print(target.shape)

print("Ground-truth count:")
print(float(target.sum()))

image = image.unsqueeze(0).to(device)
target = target.unsqueeze(0).to(device)

# ---------------------------------------------------------
# Create model
# ---------------------------------------------------------

print("\nCreating MCNN...")

model = MCNN(
    pretrained=True,
    freeze_backbone=False
).to(device)

model.train()

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=5e-6,
    weight_decay=1e-4,
)

print("MCNN ready.")

# ---------------------------------------------------------
# Train repeatedly on SAME image
# ---------------------------------------------------------

print("\nStarting single-image training...")
print("-" * 70)

for step in range(100):

    optimizer.zero_grad()

    prediction, attention = model(image)

    density_loss = F.mse_loss(
        prediction,
        target
    )

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

    loss = density_loss + 0.01 * count_loss

    loss.backward()

    optimizer.step()

    print(
        f"Step {step + 1:02d}/100 | "
        f"Density Loss: {density_loss.item():.6f} | "
        f"Count Loss: {count_loss.item():.2f} | "
        f"Total Loss: {loss.item():.6f}"
    )

# ---------------------------------------------------------
# Final prediction
# ---------------------------------------------------------

model.eval()

with torch.no_grad():

    prediction, attention = model(image)

    predicted_count = prediction.sum().item()
    actual_count = target.sum().item()

print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)

print("Actual count:")
print(actual_count)

print("Predicted count:")
print(predicted_count)

print("\nAttention weights:")
print(attention)

print("\n" + "=" * 70)
print("SINGLE-IMAGE OVERFIT TEST COMPLETED")
print("=" * 70)