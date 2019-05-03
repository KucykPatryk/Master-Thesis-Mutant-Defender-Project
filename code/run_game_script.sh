#!/bin/bash

python game_main.py --iterations 2 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --winning_threshold 0.5 --output_run_dir rlrun1 --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program triangle --save_bandits True --load_bandits True --bandit_load_dir triangle/run0_gis:3_mss:10_tss:10_mplm:0.3_wt:0.5_am:scikit_dm:scikit_ba:EpsilonGreedy

#python game_main.py --iterations 1000 --mutants_subset_size 5 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --#winning_threshold 0.5 --output_run_dir 'run2'

#python game_main.py --iterations 1000 --mutants_subset_size 20 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --#winning_threshold 0.5 --output_run_dir 'run3'

#python game_main.py --iterations 1000 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.5 --#winning_threshold 0.5 --output_run_dir 'run4'

#python game_main.py --iterations 1000 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.7 --#winning_threshold 0.5 --output_run_dir 'run5'

#python game_main.py --iterations 1000 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --#winning_threshold 0.2 --output_run_dir 'run6'

#python game_main.py --iterations 1000 --mutants_subset_size 10 --tests_subset_size 10 --model_pick_limit_multiplier 0.3 --#winning_threshold 0.8 --output_run_dir 'run7'
