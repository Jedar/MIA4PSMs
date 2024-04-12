# Membership Inference Attack for Password Strength Meters

We build a membership inference attack library for password strength meters (PSM, for short) to evaluate the password leakage problem of PSMs.

## 1. How to Use

In our library, we consider a probability based membership inference attack and a neural network based membership inference attack.

### 1.1 Preparing

Before starting membership inference attack, you should have two password datasets, one for PSM training and one for testing.

+ Step 1. Use the training dataset to train PSMs. We summarize some popular PSMs in `src/psms`. Most PSMs support inputing a password file (one password per line) to train a password model.

+ Step 2. Use the testing dataset to obtain evaluation results. After the training, you can obtain the strength evaluated by target PSMs. The codes `src/psms` also include evaluation phase.

> The evaluation results always include a triplet of (password, probability, guess_number), the guess_number is not necessary.

### 1.2 Probability Based Attack

The codes of probability based attack are `src/attack_model/prob_threshold/threshold_based_attack_xato.py`.
Configuring above evaluation result in the Python code.
This file will calculate the precision/recall/accuracy of a probability threshold.

### 1.3 Neural Network Based Attack

The codes of neural network based attack are `src/attack_model/nn`.
You can use a evaluation result combined with the training set to build a RNN attack model in `Trainer`.
After that, you can check whether a password is a member password by `Evaluator`.

## 2. PSMs in This Library

We mainly consider probabilistic password strength meters including markov based model, PCFG based model and neural based model.
Here is the list:


| PSM | Year | Codes |
| --------| ------ | -------- |
| Markov | 2007 | `src/psms/nwords` |
| Adaptive PSM| 2013 | `src/psms/adaptive_markov` |
| Backoff | 2014 | `src/psms/backoff` |
| CKL_PSM | 2021 | `src/psms/CKL_PCFG` |
| FuzzyPSM | 2016 | `src/psms/FuzzyPSM` |
| LSTM | 2016 | `src/psms/LSTM/lstm.py` |
| PCFG v4.1 |  2019| `src/psms/PCFG` |
