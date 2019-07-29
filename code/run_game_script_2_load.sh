#!/bin/bash

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_fl --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program range --save_bandits --load_bandits --bandit_load_dir hierarchypropertyparser/rlrundef_f_gis:500_mss:10_tss:25_mplm:0.30_wt:0.25_am:scikit_dm:scikit_ba:EpsilonGreedy

python game_main.py --iterations 500 --mutants_subset_size 10 --tests_subset_size 25 --model_pick_limit_multiplier 0.3 --winning_threshold 0.25 --output_run_dir rlrundef_fl --attacker_mode scikit --defender_mode scikit --bandit_algorithm EpsilonGreedy --program fontinfo --save_bandits --load_bandits --bandit_load_dir hierarchypropertyparser/rlrundef_f_gis:500_mss:10_tss:25_mplm:0.30_wt:0.25_am:scikit_dm:scikit_ba:EpsilonGreedy
