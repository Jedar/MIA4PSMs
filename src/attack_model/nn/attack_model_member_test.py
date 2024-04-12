import argparse
import json
import tqdm

from Model import *
from Evaluator import *
from Dataset import *
from Arguments import *

device = torch.device("cuda:0")

def output(pwds, path):
    with open(path, "w") as f:
        pwdsize = len(pwds)
        for i in tqdm.tqdm(range(pwdsize)):
            line = pwds[i]
            f.write(f"{line[0]}\t{line[1]}\t{line[2]}\n")
    print(f">>> Result saved in {path}")

def main():
    args = init_member_test_cli()
    print("a=",args.output_data)
    config = EvaluatorConfig(
        args.batch_size,
        args.model_load,
        args.dict_size,
        args.max_len
    )

    evaluator = BatchEvaluator(config, device)

    data = optimized_dataset(
        args.query_data, 
        args.target_data, 
        args.dict_size+1, 
        args.max_len
    )

    data = direct_dataloader_wrapper(data, args.batch_size, False)

    ans = []

    for step, (pwd, x, y) in tqdm.tqdm(enumerate(data)):
        pred = evaluator(x)
        n = len(x)
        for i in range(n):
            ans.append((pwd[i], int(pred[i]), int(y[i])))

    print(ans[:5])

    output(ans, args.output_data)

    X = [x[1] for x in ans]
    Y = [x[2] for x in ans]

    print(validate(X, Y))


if __name__ == '__main__':
    main()


