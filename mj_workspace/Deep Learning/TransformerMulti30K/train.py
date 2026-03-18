import os
import wandb
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from config import TransformerConfig
from dataset import Multi30KDataset, collate_fn
from model import Transformer, Encoder, Decoder

def train(model, iterator, optimizer, criterion, clip, epoch):
    model.train()
    epoch_loss = 0
    
    for i, batch in enumerate(iterator):
        src, trg = batch
        src, trg = src.to(model.device), trg.to(model.device)
        
        optimizer.zero_grad()
        
        trg_input = trg[:-1, :]
        trg_output = trg[1:, :]
        
        output, _ = model(src, trg_input)
        
        output_dim = output.shape[-1]
        loss = criterion(output.view(-1, output_dim), trg_output.view(-1))
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()
        
        epoch_loss += loss.item()
        
        # --- WandB 로깅 (Step 단위) ---
        wandb.log({
            "batch_loss": loss.item(),
            "iter": epoch * len(iterator) + i
        })
            
    return epoch_loss / len(iterator)

if __name__ == "__main__":
    config = TransformerConfig()
    
    # 1. WandB 초기화 (epochs를 config 기반으로 수정)
    wandb.init(
        project="ToyProject-Transformer Multi 30K",
        name=f"d_model_{config.d_model}_head_{config.n_head}",
        config={
            "learning_rate": 0.0001,
            "epochs": 200,
            "batch_size": config.batch_size,
            "d_model": config.d_model,
            "n_layers": config.num_encoder_layers,
            "n_heads": config.n_head
        }
    )

    # 2. 데이터 및 모델 세팅
    train_dataset = Multi30KDataset(config, split='train')
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, 
                              shuffle=True, collate_fn=collate_fn)
    
    enc = Encoder(len(train_dataset.src_vocab), config.d_model, config.num_encoder_layers, 
                  config.n_head, config.dim_feedforward, config.dropout, 5000)
    dec = Decoder(len(train_dataset.tgt_vocab), config.d_model, config.num_decoder_layers, 
                  config.n_head, config.dim_feedforward, config.dropout, 5000)
    
    model = Transformer(enc, dec, config.PAD_IDX, config.PAD_IDX, config.device).to(config.device)
    
    def initialize_weights(m):
        if hasattr(m, 'weight') and m.weight.dim() > 1:
            nn.init.xavier_uniform_(m.weight.data)
    
    wandb.watch(model, log="all")

    criterion = nn.CrossEntropyLoss(ignore_index=config.PAD_IDX)
    optimizer = optim.Adam(model.parameters(), lr=0.0005)
    
    # --- Noam Scheduler 적용 (선택 사항이나 권장) ---
    # step_num에 따라 lr을 조절하려면 scheduler.step()을 train 함수 안에 넣어야 합니다.

    # 3. 루프 실행
    for epoch in range(100): # 100 epoch 기준
        train_loss = train(model, train_loader, optimizer, criterion, 1, epoch)
        
        # --- WandB 로깅 (Epoch 단위) ---
        wandb.log({"epoch": epoch + 1, "train_loss": train_loss})
        print(f"Epoch: {epoch+1:03d} | Loss: {train_loss:.4f}")

        # --- 모델 저장 로직 (5 에포크마다) ---
        if (epoch + 1) % 1 == 0:
            # 1. 저장할 폴더 이름 설정
            folder_name = "checkpoints2"
            
            # 2. 폴더가 없으면 생성
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                print(f"Created directory: {folder_name}")

            # 3. 경로 결합
            file_name = f"transformer_ep{epoch+1:03d}_loss{train_loss:.4f}.pt"
            save_path = os.path.join(folder_name, file_name)
            
            torch.save(model.state_dict(), save_path)
            print(f">>> Model saved: {save_path}")

    wandb.finish()