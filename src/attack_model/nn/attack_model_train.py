import argparse
import json
import torch

from Model import *
from Trainer import *
from Dataset import *
from Arguments import *

device = torch.device("cuda:0")

def main():
    args = init_train_cli()
    model = LSTMClassifier(args.dict_size, args.hidden_size, args.num_layers, 1).to(device)
    print(model)
    data = dataset(args.train_data, args.target_data, args.dict_size, args.max_len)
    config = TrainerConfig(
        args.batch_size,
        args.lr, 
        args.num_worker,
        args.epochs,
        args.model_save
    )

    trainer = FocusLossTrainer(model, data, config, device)

    trainer.train()

    trainer.eval()

if __name__ == '__main__':
    main()


