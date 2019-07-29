#!/bin/bash

#python game_main.py --iterations 2 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --winning_threshold 0.5 --output_run_dir rlrun1 --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program triangle --save_bandits True --load_bandits True --bandit_load_dir triangle/run0_gis:3_mss:10_tss:10_mplm:0.3_wt:0.5_am:scikit_dm:scikit_ba:EpsilonGreedy

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode scikit --bandit_algorithm EpsilonGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm AdaptiveGreedy --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm ActiveExplorer --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm SoftmaxExplorer --program inflection --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode scikit --bandit_algorithm EpsilonGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm AdaptiveGreedy --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm ActiveExplorer --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm SoftmaxExplorer --program hierarchypropertyparser --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode scikit --bandit_algorithm EpsilonGreedy --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm AdaptiveGreedy --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm ActiveExplorer --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm SoftmaxExplorer --program fontinfo --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode random --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode random --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode random --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm AdaptiveGreedy --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm ActiveExplorer --program range --save_bandits

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_f --attacker_mode scikit --defender_mode scikit --bandit_algorithm SoftmaxExplorer --program range --save_bandits
