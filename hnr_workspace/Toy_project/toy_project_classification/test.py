import torch
from models.resnet import resnet18, resnet34

x = torch.randn(4, 3, 32, 32)

model18 = resnet18(num_classes=100)
y18 = model18(x)
print("ResNet18 output shape:", y18.shape)

model34 = resnet34(num_classes=100)
y34 = model34(x)
print("ResNet34 output shape:", y34.shape)