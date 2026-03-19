# src/train_eval.py
import math
import torch
import torch.nn as nn

def train_one_epoch(model, dataloader, optimizer, criterion, clip, device):
    model.train()
    epoch_loss = 0

    for src, tgt in dataloader:
        src = src.to(device)
        tgt = tgt.to(device)

        # decoder input / target shift
        tgt_input = tgt[:, :-1]
        tgt_label = tgt[:, 1:]

        optimizer.zero_grad()

        output, _ = model(src, tgt_input)
        # output: (B, tgt_len-1, vocab_size)

        output_dim = output.shape[-1]

        output = output.contiguous().view(-1, output_dim)
        tgt_label = tgt_label.contiguous().view(-1)

        loss = criterion(output, tgt_label)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()

        epoch_loss += loss.item()

    return epoch_loss / len(dataloader)


@torch.no_grad()
def evaluate(model, dataloader, criterion, device):
    model.eval()
    epoch_loss = 0

    for src, tgt in dataloader:
        src = src.to(device)
        tgt = tgt.to(device)

        tgt_input = tgt[:, :-1]
        tgt_label = tgt[:, 1:]

        output, _ = model(src, tgt_input)
        output_dim = output.shape[-1]

        output = output.contiguous().view(-1, output_dim)
        tgt_label = tgt_label.contiguous().view(-1)

        loss = criterion(output, tgt_label)
        epoch_loss += loss.item()

    return epoch_loss / len(dataloader)


@torch.no_grad()
def greedy_decode(model, src_tensor, tgt_vocab, max_len, device):
    model.eval()

    bos_idx = tgt_vocab['<bos>']
    eos_idx = tgt_vocab['<eos>']

    src_tensor = src_tensor.to(device)

    generated = torch.tensor([[bos_idx]], dtype=torch.long, device=device)

    for _ in range(max_len):
        output, _ = model(src_tensor, generated)
        next_token = output[:, -1, :].argmax(-1).unsqueeze(1)
        generated = torch.cat([generated, next_token], dim=1)

        if next_token.item() == eos_idx:
            break

    return generated.squeeze(0).tolist()