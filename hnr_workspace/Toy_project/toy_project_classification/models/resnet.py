# models/resnet.py

import torch
import torch.nn as nn


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()

        self.conv1 = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False
        )
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(
            out_channels,
            out_channels,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False
        )
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()

        # 입력과 출력 shape가 다르면 shortcut에서 맞춰줘야 함
        if stride != 1 or in_channels != out_channels * self.expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_channels,
                    out_channels * self.expansion,
                    kernel_size=1,
                    stride=stride,
                    bias=False
                ),
                nn.BatchNorm2d(out_channels * self.expansion)
            )

    def forward(self, x):
        identity = x

        out = self.conv1(x)      # [B, in_c, H, W] -> [B, out_c, H/stride, W/stride]
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)    # [B, out_c, H', W'] -> [B, out_c, H', W']
        out = self.bn2(out)

        identity = self.shortcut(identity)

        out = out + identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=100):
        super().__init__()

        self.in_channels = 64

        # CIFAR용 stem: 32x32 입력에 맞게 가볍게 시작
        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=64,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False
        )
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)

        # stage1 ~ stage4
        self.layer1 = self._make_layer(block, out_channels=64,  blocks=layers[0], stride=1)
        self.layer2 = self._make_layer(block, out_channels=128, blocks=layers[1], stride=2)
        self.layer3 = self._make_layer(block, out_channels=256, blocks=layers[2], stride=2)
        self.layer4 = self._make_layer(block, out_channels=512, blocks=layers[3], stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

    def _make_layer(self, block, out_channels, blocks, stride):
        layers = []

        # 첫 블록은 stride가 들어갈 수 있음 (해상도 줄이는 역할)
        layers.append(block(self.in_channels, out_channels, stride))
        self.in_channels = out_channels * block.expansion

        # 나머지 블록은 stride=1
        for _ in range(1, blocks):
            layers.append(block(self.in_channels, out_channels, stride=1))

        return nn.Sequential(*layers)

    def forward(self, x):
        # 입력 x shape: [B, 3, 32, 32]

        x = self.conv1(x)   # [B, 64, 32, 32]
        x = self.bn1(x)
        x = self.relu(x)

        x = self.layer1(x)  # [B, 64, 32, 32]
        x = self.layer2(x)  # [B, 128, 16, 16]
        x = self.layer3(x)  # [B, 256, 8, 8]
        x = self.layer4(x)  # [B, 512, 4, 4]

        x = self.avgpool(x) # [B, 512, 1, 1]
        x = torch.flatten(x, 1)  # [B, 512]
        x = self.fc(x)      # [B, num_classes]

        return x


def resnet18(num_classes=100):
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes=num_classes)


def resnet34(num_classes=100):
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes)


def get_model(model_name="resnet18", num_classes=100):
    if model_name == "resnet18":
        return resnet18(num_classes=num_classes)
    elif model_name == "resnet34":
        return resnet34(num_classes=num_classes)
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")