# train.py

import os
import torch
import torch.nn as nn
import torch.optim as optim

from configs.config import CFG
from src.utils import set_seed, save_model
from src.dataset import get_dataloader
from src.engine import train_one_epoch, valid_one_epoch
from models.resnet import get_model
from torch.utils.tensorboard import SummaryWriter


def main():
    set_seed(CFG.SEED)
    writer = SummaryWriter(log_dir="runs/resnet_experiment")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_loader, valid_loader = get_dataloader(
        root=CFG.DATA_ROOT,
        batch_size=CFG.BATCH_SIZE,
        num_workers=CFG.NUM_WORKERS
    )

    model = get_model(model_name=CFG.MODEL_NAME, num_classes=CFG.NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=CFG.LR, weight_decay=0.01)

    best_acc = 0.0

    for epoch in range(CFG.EPOCHS):
        print(f"\nEpoch [{epoch+1}/{CFG.EPOCHS}]")

        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device
        )
        valid_loss, valid_acc = valid_one_epoch(
            model, valid_loader, criterion, device
        )

        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
        print(f"Valid Loss: {valid_loss:.4f} | Valid Acc: {valid_acc:.4f}")

        writer.add_scalar("Loss/train", train_loss, epoch)
        writer.add_scalar("Loss/valid", valid_loss, epoch)
        writer.add_scalar("Accuracy/train", train_acc, epoch)
        writer.add_scalar("Accuracy/valid", valid_acc, epoch)
        writer.add_scalar("LR", optimizer.param_groups[0]["lr"], epoch)

        if valid_acc > best_acc:
            best_acc = valid_acc
            save_model(model, os.path.join(CFG.SAVE_DIR, "best_model.pth"))
            print("Best model saved.")

    print(f"\nTraining finished. Best Valid Acc: {best_acc:.4f}")
    writer.close()


if __name__ == "__main__":
    main()