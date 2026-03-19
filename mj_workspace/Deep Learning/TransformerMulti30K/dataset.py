import os
import torch
from torch.utils.data import Dataset
import spacy
from collections import Counter
from config import TransformerConfig

class Multi30KDataset(Dataset):
    def __init__(self, config: TransformerConfig, split='train', src_vocab=None, tgt_vocab=None):
        self.config = config
        self.split = split
        
        # 1. 토크나이저 설정 (spacy 모델 : 문장을 단어 단위로 쪼개는 도구)
        #self.src_tokenizer = get_tokenizer('spacy', language='de_core_news_sm')
        #self.tgt_tokenizer = get_tokenizer('spacy', language='en_core_web_sm')
        self.de_nlp = spacy.load('de_core_news_sm')
        self.en_nlp = spacy.load('en_core_web_sm')
        # 토크나이저 함수 정의
        self.src_tokenizer = lambda text: [tok.text for tok in self.de_nlp.tokenizer(text)]
        self.tgt_tokenizer = lambda text: [tok.text for tok in self.en_nlp.tokenizer(text)]

        # 2. 로컬 파일 읽기
        # train.de, train.en 열어서 가져오기
        src_file = os.path.join(config.data_path, f"{split}.{config.src_lang}")
        tgt_file = os.path.join(config.data_path, f"{split}.{config.tgt_lang}")
        
        with open(src_file, 'r', encoding='utf-8') as f:
            self.src_data = [line.strip() for line in f] # "한 줄씩 담아서 가져옴"
        with open(tgt_file, 'r', encoding='utf-8') as f:
            self.tgt_data = [line.strip() for line in f]
            
        assert len(self.src_data) == len(self.tgt_data), "Source와 Target 데이터 개수가 다릅니다!"

        # 3. 단어 사전(Vocab) 처리 (test, infernce 차이)
        # train이면 직접 vocab을 만들고, val/test면 train에서 학습하며 만든 만든 vocab을 받아옵니다.
        if split == 'train':
            self.src_vocab = self._build_vocab(self.src_data, self.src_tokenizer)
            self.tgt_vocab = self._build_vocab(self.tgt_data, self.tgt_tokenizer)
        else:
            self.src_vocab = src_vocab
            self.tgt_vocab = tgt_vocab

    # 단어 사전 (vocab) 만들기용
    def _build_vocab(self, data_list, tokenizer): # data와 torkenizer 도구를 받음.
        counter = Counter()
        for text in data_list: # data에 있는 text를 lower case로 변환하고 단어별로 중복되는 개수를 센다
            counter.update(tokenizer(text.lower()))
        
        # 특수 토큰 먼저 할당 (pad, sos, eos, unk 순서로 vocab에 담음 0, 1, 2, 3)
        vocab = {token: i for i, token in enumerate(self.config.special_symbols)}
        # 빈도수 2 이상인 단어만 추가 (min_freq 조절 가능)
        for word, freq in counter.items(): # 즉, 빈도가 2번 이상인 단어만 vocab에 담음!
            if freq >= 1 and word not in vocab:
                vocab[word] = len(vocab) # 순서대로 vocab에 담기 시작 -> 특수토큰 다음인 index 4부터 시작.
        return vocab

    def __len__(self):
        # enumerate와 DataLoader가 멈출 시점을 결정합니다.
        return len(self.src_data)

    def __getitem__(self, idx):
        # 1. idx에 해당하는 en, de 문장 가져오기
        src_text = self.src_data[idx]
        tgt_text = self.tgt_data[idx]
        
        # 2. 토큰화 및 수치화
        src_tokens = self.src_tokenizer(src_text.lower())
        tgt_tokens = self.tgt_tokenizer(tgt_text.lower())
        
        # 3. tokenizer를 통해 쪼개진 단어들을 vocab에 등록된 번호로 바꿈.
        #     빈도수가 1 이하인 사전에 등록되지 않은 단어는 3번(Unk) 특수토큰으로 바꿔줌.
        src_indices = [self.src_vocab.get(token, self.config.UNK_IDX) for token in src_tokens]
        tgt_indices = [self.tgt_vocab.get(token, self.config.UNK_IDX) for token in tgt_tokens]
        
        # 4. SOS, EOS 추가 및 텐서 변환
        src_indices = [self.config.SOS_IDX] + src_indices + [self.config.EOS_IDX]
        tgt_indices = [self.config.SOS_IDX] + tgt_indices + [self.config.EOS_IDX]
        
        return torch.tensor(src_indices), torch.tensor(tgt_indices)


from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

# batch안에 채울때 길이를 맞추기 위해 사용
def collate_fn(batch):
    src_batch, tgt_batch = [], []
    for src_sample, tgt_sample in batch:
        src_batch.append(src_sample)
        tgt_batch.append(tgt_sample)

    # padding_value는 Config에 정의한 PAD_IDX(0)를 사용
    src_batch = pad_sequence(src_batch, padding_value=0) # pad_sequence : 가장 긴 문장을 기준으로 짧은 문장들의 빈칸을 padding_value=0 로 채워줌.
    tgt_batch = pad_sequence(tgt_batch, padding_value=0)
    
    return src_batch, tgt_batch

# Dataloader 작동 방식.
# 1. Dataset의 getitem을 배치크기만큼 호출해서 sample을 리스트로 모아옴
# 2. 이 리스트를 collate_fn에 줌
# 3. collate_fn은 이 샘플들을 하나로 묶어서 큰 텐서로 만듬
config = TransformerConfig()
train_dataset = Multi30KDataset(config, split='train')
train_loader = DataLoader(train_dataset, batch_size=config.batch_size, 
                          shuffle=True, collate_fn=collate_fn)
# test_dataset = Multi30KDataset(
#     config, 
#     split='test_2016_flickr', 
#     src_vocab=train_dataset.src_vocab, 
#     tgt_vocab=train_dataset.tgt_vocab,
# )
# test_loader = DataLoader(test_dataset, batch_size=config.batch_size, 
#                           shuffle=False, collate_fn=collate_fn)
print(f"독일어 사전 크기: {len(train_dataset.src_vocab)}")
print(f"영어 사전 크기: {len(train_dataset.tgt_vocab)}")
