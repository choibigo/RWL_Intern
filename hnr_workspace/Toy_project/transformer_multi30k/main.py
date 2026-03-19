# main.py
import time
import math
import torch
import torch.nn as nn
import torch.optim as optim

from config import CFG
from src.dataset import get_dataloaders
from src.train_eval import train_one_epoch, evaluate
from src.utils import set_seed, epoch_time
from models.transformer import Transformer

def main():
    set_seed(CFG.SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("device:", device)

    train_loader, valid_loader, test_loader, src_vocab, tgt_vocab = get_dataloaders(
        batch_size=CFG.BATCH_SIZE,
        min_freq=CFG.MIN_FREQ
    )

    src_pad_idx = src_vocab['<pad>']
    tgt_pad_idx = tgt_vocab['<pad>']

    model = Transformer(
        input_dim=len(src_vocab),
        output_dim=len(tgt_vocab),
        src_pad_idx=src_pad_idx,
        tgt_pad_idx=tgt_pad_idx,
        d_model=CFG.D_MODEL,
        n_heads=CFG.N_HEADS,
        num_encoder_layers=CFG.NUM_ENCODER_LAYERS,
        num_decoder_layers=CFG.NUM_DECODER_LAYERS,
        d_ff=CFG.D_FF,
        dropout=CFG.DROPOUT,
        max_len=CFG.MAX_LEN
    ).to(device)

    optimizer = optim.Adam(model.parameters(), lr=CFG.LR)
    criterion = nn.CrossEntropyLoss(ignore_index=tgt_pad_idx)

    best_valid_loss = float('inf')

    for epoch in range(CFG.N_EPOCHS):
        start_time = time.time()

        train_loss = train_one_epoch(
            model, train_loader, optimizer, criterion, CFG.CLIP, device
        )
        valid_loss = evaluate(model, valid_loader, criterion, device)

        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), "best_transformer.pt")

        print(f"Epoch: {epoch+1:02}")
        print(f"Time: {epoch_mins}m {epoch_secs}s")
        print(f"Train Loss: {train_loss:.4f} | Train PPL: {math.exp(train_loss):7.3f}")
        print(f" Val. Loss: {valid_loss:.4f} |  Val. PPL: {math.exp(valid_loss):7.3f}")

        model.load_state_dict(torch.load("best_transformer.pt"))
        test_loss = evaluate(model, test_loader, criterion, device)
        print(f"Test Loss: {test_loss:.4f} | Test PPL: {math.exp(test_loss):7.3f}")


if __name__ == "__main__":
    main()