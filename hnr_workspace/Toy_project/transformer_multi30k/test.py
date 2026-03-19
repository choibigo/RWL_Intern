from Toy_project.transformer_multi30k.src.dataset_ver import get_dataloaders

train_loader, valid_loader, test_loader, src_vocab, tgt_vocab = get_dataloaders(batch_size=4, min_freq=2)

src, tgt = next(iter(train_loader))
print(src.shape)
print(tgt.shape)
print(len(src_vocab), len(tgt_vocab))
print(src[0])
print(tgt[0])