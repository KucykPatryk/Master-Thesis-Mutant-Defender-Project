#!/bin/bash

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program range --save_bandits
