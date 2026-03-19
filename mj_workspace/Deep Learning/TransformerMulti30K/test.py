import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import spacy
import math
from nltk.translate.bleu_score import corpus_bleu

# 프로젝트 모듈 임포트
from config import TransformerConfig
from dataset import Multi30KDataset, collate_fn
from model import Transformer, Encoder, Decoder

def translate_sentence(sentence, src_vocab, tgt_vocab, model, device, max_len=50):
    """한 문장을 입력받아 번역을 수행 (Greedy Search)"""
    model.eval()
    
    # 1. 토큰화 및 수치화
    if isinstance(sentence, str):
        nlp = spacy.load('de_core_news_sm')
        tokens = [tok.text.lower() for tok in nlp.tokenizer(sentence)]
    else: # 이미 인덱스 텐서인 경우 (Dataset에서 바로 꺼낼 때)
        rev_src_vocab = {v: k for k, v in src_vocab.items()}
        tokens = [rev_src_vocab.get(idx.item(), '<unk>') for idx in sentence if idx.item() not in [1, 2, 0]]

    src_indices = [src_vocab.get('<sos>', 1)] + \
                  [src_vocab.get(token, 3) for token in tokens] + \
                  [src_vocab.get('<eos>', 2)]
    
    src_tensor = torch.LongTensor(src_indices).unsqueeze(1).to(device)

    # 2. 인코더 통과
    src_mask = model.make_src_mask(src_tensor)
    with torch.no_grad():
        enc_src = model.encoder(src_tensor, src_mask)

    # 3. 디코더 루프
    trg_indices = [tgt_vocab.get('<sos>', 1)]
    for _ in range(max_len):
        trg_tensor = torch.LongTensor(trg_indices).unsqueeze(1).to(device)
        trg_mask = model.make_trg_mask(trg_tensor)
        
        with torch.no_grad():
            output, _ = model.decoder(trg_tensor, enc_src, trg_mask, src_mask)
        
        pred_token = output.argmax(2)[-1, :].item()
        trg_indices.append(pred_token)
        
        if pred_token == tgt_vocab.get('<eos>', 2):
            break
    
    rev_tgt_vocab = {v: k for k, v in tgt_vocab.items()}
    return [rev_tgt_vocab.get(i, '<unk>') for i in trg_indices[1:-1]] # <sos>, <eos> 제외

def run_evaluation(model, test_loader, criterion, test_dataset, src_vocab, tgt_vocab, device):
    """전체 테스트셋에 대해 Loss, PPL, BLEU 계산"""
    model.eval()
    epoch_loss = 0
    
    # Quantitative: Loss & PPL
    with torch.no_grad():
        for batch in test_loader:
            src, trg = batch
            src, trg = src.to(device), trg.to(device)
            output, _ = model(src, trg[:-1, :])
            loss = criterion(output.view(-1, output.shape[-1]), trg[1:, :].view(-1))
            epoch_loss += loss.item()
    
    avg_loss = epoch_loss / len(test_loader)
    
    # BLEU Score Calculation (NLTK)
    targets = []
    outputs = []
    rev_tgt_vocab = {v: k for k, v in tgt_vocab.items()}
    
    print("Calculating BLEU score...")
    for i in range(min(300, len(test_dataset))): # 시간 관계상 300개 샘플링 평가
        src_tensor, trg_tensor = test_dataset[i]
        
        prediction = translate_sentence(src_tensor, src_vocab, tgt_vocab, model, device)
        
        # 정답 문장 복원 (특수 토큰 제외)
        actual_target = [rev_tgt_vocab.get(idx.item(), '<unk>') for idx in trg_tensor 
                         if idx.item() not in [0, 1, 2]]
        
        outputs.append(prediction)
        targets.append([actual_target])
    
    bleu = corpus_bleu(targets, outputs) * 100
    return avg_loss, bleu

if __name__ == "__main__":
    config = TransformerConfig()
    
    # 1. 데이터셋 준비 (사전 공유 필수)
    train_dataset = Multi30KDataset(config, split='train')
    # test_dataset = Multi30KDataset(config, split='test_2016_flickr', 
    #                               src_vocab=train_dataset.src_vocab, 
    #                               tgt_vocab=train_dataset.tgt_vocab)
    test_dataset = Multi30KDataset(config, split='train', 
                                   src_vocab=train_dataset.src_vocab, 
                                   tgt_vocab=train_dataset.tgt_vocab)


    test_loader = DataLoader(test_dataset, batch_size=config.batch_size, 
                             shuffle=False, collate_fn=collate_fn)

    # 2. 모델 복원
    enc = Encoder(len(train_dataset.src_vocab), config.d_model, config.num_encoder_layers, 
                  config.n_head, config.dim_feedforward, config.dropout, 5000)
    dec = Decoder(len(train_dataset.tgt_vocab), config.d_model, config.num_decoder_layers, 
                  config.n_head, config.dim_feedforward, config.dropout, 5000)
    model = Transformer(enc, dec, config.PAD_IDX, config.PAD_IDX, config.device).to(config.device)

    # 가장 최근에 저장된 체크포인트 경로로 수정하세요
    model_path = "/workspace/ToyProject-transformer/checkpoints2/transformer_ep012_loss0.7687.pt" 
    model.load_state_dict(torch.load(model_path, map_location=config.device))
    print(f"Loaded: {model_path}")

    # 3. 평가 실행
    criterion = nn.CrossEntropyLoss(ignore_index=config.PAD_IDX)
    loss, bleu = run_evaluation(model, test_loader, criterion, test_dataset, 
                               train_dataset.src_vocab, train_dataset.tgt_vocab, config.device)

    print("\n" + "="*30)
    print(f"Test Loss: {loss:.3f}")
    print(f"Test PPL : {math.exp(loss):.3f}") # PPL = e^loss
    print(f"BLEU Score: {bleu:.2f}")
    print("="*30 + "\n")

    # 4. 샘플 확인 (Qualitative)
    print("[ Sample Translations ]")
    for i in range(3):
        src_tensor, trg_tensor = test_dataset[i]
        translation = translate_sentence(src_tensor, train_dataset.src_vocab, 
                                       train_dataset.tgt_vocab, model, config.device)
        print(f"Sample {i+1}")
        print(f" > Result: {' '.join(translation)}")