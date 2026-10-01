import torch

from models.mcnn import MCNN


print("=" * 70)
print("MCNN FORWARD PASS TEST")
print("=" * 70)

# ---------------------------------------------------------
# 1. Select device
# ---------------------------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

# ---------------------------------------------------------
# 2. Create the model
# ---------------------------------------------------------

print("\nCreating MCNN model...")

model = MCNN(
    pretrained=True,
    freeze_backbone=False
).to(device)

print("Model created successfully.")

# ---------------------------------------------------------
# 3. Create a dummy image
# ---------------------------------------------------------

x = torch.randn(
    1,      # batch size
    3,      # RGB channels
    512,    # height
    512     # width
).to(device)

print("\nInput shape:")
print(x.shape)

# ---------------------------------------------------------
# 4. Forward pass
# ---------------------------------------------------------

print("\nRunning forward pass...")

model.eval()

with torch.no_grad():

    density_map, attention_weights = model(x)

# ---------------------------------------------------------
# 5. Display outputs
# ---------------------------------------------------------

print("\nDensity map shape:")
print(density_map.shape)

print("\nAttention weights shape:")
print(attention_weights.shape)

print("\nAttention weights:")
print(attention_weights)

# ---------------------------------------------------------
# 6. Verify attention weights
# ---------------------------------------------------------

attention_sum = attention_weights.sum(
    dim=1
)

print("\nAttention weight sum:")
print(attention_sum)

# ---------------------------------------------------------
# 7. Verify density map
# ---------------------------------------------------------

print("\nDensity map minimum:")
print(float(density_map.min()))

print("Density map maximum:")
print(float(density_map.max()))

print("Predicted count from untrained model:")
print(float(density_map.sum()))

# ---------------------------------------------------------
# 8. Final checks
# ---------------------------------------------------------

assert density_map.shape == (
    1,
    1,
    512,
    512
), "Unexpected density map shape!"

assert attention_weights.shape == (
    1,
    3
), "Unexpected attention shape!"

print("\n" + "=" * 70)
print("MCNN FORWARD PASS TEST PASSED")
print("=" * 70)