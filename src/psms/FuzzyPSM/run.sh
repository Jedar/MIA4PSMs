#!/usr/bin/env bash

dict_file_path="/disk/yjt/InferAttack/src/psm/FuzzyPSM/test/D.txt"
training_set_path="/disk/yjt/InferAttack/src/psm/FuzzyPSM/test/B.txt"
test_set_path="/disk/yjt/InferAttack/src/psm/FuzzyPSM/test/Q.txt"
score_file_path="/disk/yjt/InferAttack/src/psm/FuzzyPSM/test/R.txt"

EXE=/disk/yjt/InferAttack/src/psm/FuzzyPSM/fuzzypcfg_all_pw_score

${EXE} ${dict_file_path} $training_set_path $test_set_path $score_file_path



