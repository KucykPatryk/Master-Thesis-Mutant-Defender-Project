#!/bin/bash

#python game_main.py --iterations 2 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --winning_threshold 0.5 --output_run_dir rlrun1 --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program triangle --save_bandits True --load_bandits True --bandit_load_dir triangle/run0_gis:3_mss:10_tss:10_mplm:0.3_wt:0.5_am:scikit_dm:scikit_ba:EpsilonGreedy

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --winning_threshold 0.1 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --winning_threshold 0.2 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --winning_threshold 0.4 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 4 --tests_subset_size 12 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 12 --tests_subset_size 4 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.25 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.75 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

#python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 7 --tests_subset_size 14 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 14 --tests_subset_size 7 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.25 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.75 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 7 --tests_subset_size 14 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 14 --tests_subset_size 7 --model_pick_limit_multiplier 0.5 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.25 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.75 --winning_threshold 0.3 --output_run_dir rlrundef --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits
