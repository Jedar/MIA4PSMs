import argparse
import json
import tqdm

from Model import *
from Evaluator import *
from Dataset import *
from Arguments import *


device = torch.device("cuda:0")

def main():
    args = init_evaluate_cli()

    config = EvaluatorConfig(
        args.batch_size,
        args.model_load,
        args.dict_size,
        args.max_len
    )

    data = optimized_dataset(
        args.query_data, 
        args.target_data, 
        args.dict_size+1, 
        args.max_len
    )
    
    data = direct_dataloader_wrapper(data, args.batch_size, False)

    evaluator = BatchEvaluator(config, device)

    y_pred = []
    y_true = []
        
    for (pwd, x, y) in tqdm.tqdm(data):
        pred = evaluator(x)
        n = len(x)
        for i in range(n):
            y_pred.append(int(pred[i]))
            y_true.append(int(y[i]))

    print(validate(y_pred, y_true))


if __name__ == '__main__':
    main()


