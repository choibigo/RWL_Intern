import torch.nn as nn
import torch
from .layers import MultiHeadAttention, PositionwiseFeedForward, TransformerEmbedding

class EncoderLayer(nn.Module):
    def __init__(self, d_model, n_head, d_ff, dropout):
        super().__init__()

        # multi-head attention 부분
        self.self_attn = MultiHeadAttention(d_model, n_head, dropout) # Multi head attention
        self.self_attn_layer_norm = nn.LayerNorm(d_model)   # MHA Layer Norm
        
        # FFN 부분
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout) # FFN
        self.ffn_layer_norm = nn.LayerNorm(d_model) # FFN layernorm
        
        self.dropout = nn.Dropout(dropout)

    def forward(self, src, src_mask):
        # --- Step 1: Self-Attention Block ---
        # Residual Connection: x + Sublayer(x)
        _src, _ = self.self_attn(src, src, src, src_mask)
        src = self.self_attn_layer_norm(src + self.dropout(_src))
        
        # --- Step 2: Feed-Forward Block ---
        # Residual Connection: x + Sublayer(x)
        _src = self.ffn(src)
        src = self.ffn_layer_norm(src + self.dropout(_src))
        
        return src

class Encoder(nn.Module):
    def __init__(self, vocab_size, d_model, n_layers, n_head, d_ff, dropout, max_len):
        super().__init__()
        self.embedding = TransformerEmbedding(vocab_size, d_model, dropout, max_len)
        
        # EncoderLayer를 n_layers번 반복해서 쌓습니다.
        self.layers = nn.ModuleList([
            EncoderLayer(d_model, n_head, d_ff, dropout) 
            for _ in range(n_layers)
        ])

    def forward(self, src, src_mask):
        x = self.embedding(src)
        for layer in self.layers:
            x = layer(x, src_mask)
        return x
    
class DecoderLayer(nn.Module):
    def __init__(self, d_model, n_head, d_ff, dropout):
        super().__init__()
        
        # 1. Self-Attention (미래 단어를 못 보게 마스킹함-> Decoder QKV)
        self.self_attn = MultiHeadAttention(d_model, n_head, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        
        # 2. Encoder-Decoder Attention (인코더 KV를 받아옴)
        self.cross_attn = MultiHeadAttention(d_model, n_head, dropout)
        self.norm2 = nn.LayerNorm(d_model)
        
        # 3. FFN
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)
        self.norm3 = nn.LayerNorm(d_model)
        
        self.dropout = nn.Dropout(dropout)

    def forward(self, trg, enc_src, trg_mask, src_mask):
        # Step 1: Masked Self-Attention
        # trg: 디코더 입력 (지금까지 생성한 단어들)
        _trg, _ = self.self_attn(trg, trg, trg, trg_mask)
        trg = self.norm1(trg + self.dropout(_trg))
        
        # Step 2: Cross-Attention (핵심!)
        # Query는 디코더(trg)에서, Key와 Value는 인코더(enc_src)에서 가져옵니다.
        # "내(디코더)가 지금 이 단어를 쓰려는데, 인코더 정보 중 어디를 봐야 할까?"
        _trg, attention = self.cross_attn(trg, enc_src, enc_src, src_mask)
        trg = self.norm2(trg + self.dropout(_trg))
        
        # Step 3: Feed Forward
        _trg = self.ffn(trg)
        trg = self.norm3(trg + self.dropout(_trg))
        
        return trg, attention

class Decoder(nn.Module):
    def __init__(self, vocab_size, d_model, n_layers, n_head, d_ff, dropout, max_len):
        super().__init__()
        # 1. 타겟 언어(예: 영어)를 위한 임베딩 + 위치 정보
        self.embedding = TransformerEmbedding(vocab_size, d_model, dropout, max_len)
        
        # 2. DecoderLayer를 n_layers번 쌓음
        self.layers = nn.ModuleList([
            DecoderLayer(d_model, n_head, d_ff, dropout)
            for _ in range(n_layers)
        ])

    def forward(self, trg, enc_src, trg_mask, src_mask):
        # trg: [Seq_len_trg, Batch_size]
        # enc_src: [Seq_len_src, Batch_size, d_model] (인코더의 최종 출력)
        
        x = self.embedding(trg)
        
        # 층층이 통과하며 Cross-Attention 수행
        for layer in self.layers:
            # attention 결과값도 필요하면 저장해서 시각화할 수 있습니다.
            x, attention = layer(x, enc_src, trg_mask, src_mask)
            
        return x, attention
    
class Transformer(nn.Module):
    def __init__(self, encoder, decoder, src_pad_idx, trg_pad_idx, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_pad_idx = src_pad_idx
        self.trg_pad_idx = trg_pad_idx
        self.device = device
        
        # 최종 출력: d_model 차원을 단어 사전 크기(tgt_vocab_size)로 투영
        self.fc_out = nn.Linear(encoder.embedding.token_emb.embedding_dim, 
                                decoder.embedding.token_emb.num_embeddings)

    def make_src_mask(self, src):
        # src: [Seq_len, Batch] -> [Batch, 1, 1, Seq_len]
        # 패딩(0)인 부분은 False, 실제 단어는 True인 마스크 생성
        src_mask = (src != self.src_pad_idx).transpose(0, 1).unsqueeze(1).unsqueeze(2)
        return src_mask

    def make_trg_mask(self, trg):
        # 1. 패딩 마스크 (인코더와 동일)
        trg_pad_mask = (trg != self.trg_pad_idx).transpose(0, 1).unsqueeze(1).unsqueeze(2)
        
        # 2. Look-ahead 마스크 (미래 단어 가리기)
        trg_len = trg.shape[0]
        # 상삼각형 행렬을 만들어 미래 단어 위치를 0으로 가림
        trg_sub_mask = torch.tril(torch.ones((trg_len, trg_len), device=self.device)).bool()
        
        # 두 마스크를 합침 (둘 다 만족해야 함)
        trg_mask = trg_pad_mask & trg_sub_mask
        return trg_mask

    def forward(self, src, trg):
        # 마스크 생성
        src_mask = self.make_src_mask(src)
        trg_mask = self.make_trg_mask(trg)
        
        # 인코더 통과
        enc_src = self.encoder(src, src_mask)
        
        # 디코더 통과 (인코더 결과 enc_src를 함께 넣음)
        out, attention = self.decoder(trg, enc_src, trg_mask, src_mask)
        
        # 최종 단어 예측
        return self.fc_out(out), attention