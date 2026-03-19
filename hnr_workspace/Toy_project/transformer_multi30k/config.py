class CFG:
    SEED = 42

    # data
    SRC_LANGUAGE = "de"
    TGT_LANGUAGE = "en"
    BATCH_SIZE = 64
    MAX_LEN = 100
    MIN_FREQ = 2

    # model
    D_MODEL = 256
    N_HEADS = 4
    NUM_ENCODER_LAYERS = 3
    NUM_DECODER_LAYERS = 3
    D_FF = 512
    DROPOUT = 0.1

    # train
    LR = 1e-4
    N_EPOCHS = 15
    CLIP = 1.0

    DEVICE = "cuda"