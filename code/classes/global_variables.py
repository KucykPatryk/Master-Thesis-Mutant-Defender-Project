from os import walk
import math


GAME_ITERATIONS = 2

MUTANTS_SUBSET_SIZE = 10
TESTS_SUBSET_SIZE = 10
MODEL_PICK_LIMIT_MULTIPLIER = 0.3
MODEL_PICK_LIMIT_M = math.ceil(MUTANTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
MODEL_PICK_LIMIT_T = math.ceil(TESTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
WINNING_THRESHOLD = 0.5  # Percentage for winning by killing mutants
ATTACKER_MODE = 'scikit'
DEFENDER_MODE = 'scikit'
BANDIT_ALGORITHM = 'EpsilonGreedy'
OUTPUT_RUN_DIR = 'run0'

SHOW_PLOTS = True

SRC_FILE_NAME = next(walk('../generation/src/'))[2][0][:-5]  # Name without the extension
SRC_FOLDER_NAME = SRC_FILE_NAME.lower()


def test_map_array(file_path='../generation/testMap.csv'):
    """ Returns an array of test ids with their actual method ids
    Array ID is TestNo and Array value is TestName number """
    tests = [0]

    with open(file_path) as tm:
        tm.readline()
        for line in tm:
            line = line.split(',')
            tests.append(line[1][29:-2])

    return tests
